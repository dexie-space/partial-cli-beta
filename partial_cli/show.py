import asyncio
import json
import rich_click as click

from chia.wallet.trading.offer import Offer

from partial_cli.puzzles import (
    MOD_HASH,
    get_launcher_coin_spend,
    get_partial_coin_spend,
    get_non_partial_coin_spends,
)
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.partial import display_partial_info
from partial_cli.utils.rpc import is_coin_spent, is_coin_valid


@click.command("show", help="display the dexie partial offer information.")
@click.option(
    "-j",
    "--json",
    "as_json",
    help="Display as JSON",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def show_cmd(ctx, as_json, offer_file):
    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb = offer.to_spend_bundle()

    coin_spends = sb.coin_spends

    partial_cs = get_partial_coin_spend(coin_spends)
    assert partial_cs is not None

    partial_coin = partial_cs.coin
    is_partial_coin_spent = asyncio.run(is_coin_spent(partial_coin.name()))
    is_partial_coin_valid = asyncio.run(is_coin_valid(partial_coin.name()))

    non_partial_coin_spends = get_non_partial_coin_spends(coin_spends)

    is_valid = False

    # partial coin exists and is not spent
    if is_partial_coin_valid and not is_partial_coin_spent:
        is_valid = True

    # partial coin does not exist
    # check if launcher coin is valid and not spent
    if not is_partial_coin_valid:
        launcher_cs = get_launcher_coin_spend(coin_spends, partial_coin=partial_coin)
        is_valid = (
            False
            if launcher_cs is None
            else asyncio.run(is_coin_valid(launcher_cs.coin.name()))
        )

    partial_info = PartialInfo.from_coin_spend(partial_cs)
    if partial_info is None:
        print("Partial offer is not valid.")
        return
    else:
        if as_json:
            ret = {
                "is_valid": is_valid,
                "MOD_HASH": MOD_HASH.hex(),
                "partial_info": partial_info.to_json_dict(),
                "partial_coin": partial_coin.to_json_dict(),
            }
            if len(non_partial_coin_spends) > 0:
                launcher_cs = next(
                    cs
                    for cs in non_partial_coin_spends
                    if cs.coin.name() == partial_coin.parent_coin_info
                )
                if launcher_cs is not None:
                    ret["launcher_coin"] = launcher_cs.coin.to_json_dict()
            print(json.dumps(ret, indent=2))
        else:
            display_partial_info(partial_info, partial_coin, is_valid=is_valid)
