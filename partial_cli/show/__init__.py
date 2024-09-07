import asyncio
import json
import rich_click as click

from chia.wallet.trading.offer import Offer

from partial_cli.puzzles.partial import (
    MOD_HASH,
    display_partial_info,
    is_coin_spent,
    get_launcher_coin_spend,
    get_partial_coin_spend,
    get_partial_info,
)


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

    partial_cs = get_partial_coin_spend(sb.coin_spends)
    partial_coin = partial_cs.coin
    is_partial_coin_spent = asyncio.run(is_coin_spent(partial_coin.name()))
    assert partial_cs is not None

    launcher_cs = get_launcher_coin_spend(
        partial_cs.coin.parent_coin_info, sb.coin_spends
    )

    partial_info = get_partial_info(partial_cs)
    if partial_info is None:
        print("Partial offer is not valid.")
        return
    else:
        if as_json:
            ret = {
                "is_valid": not is_partial_coin_spent,
                "MOD_HASH": MOD_HASH.hex(),
                "partial_info": partial_info.to_json_dict(),
                "partial_coin": partial_coin.to_json_dict(),
            }
            if launcher_cs is not None:
                ret["launcher_coin"] = launcher_cs.coin.to_json_dict()
            print(json.dumps(ret, indent=2))
        else:
            display_partial_info(
                partial_info, partial_coin.name(), is_valid=not is_partial_coin_spent
            )
