import asyncio
import json
import rich_click as click

from chia.wallet.trading.offer import Offer

from partial_cli.puzzles.partial import (
    display_partial_info,
    get_launcher_or_partial_cs,
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

    cs, is_spent = asyncio.run(get_launcher_or_partial_cs(sb.coin_spends))
    partial_coin, partial_info, launcher_coin = get_partial_info(cs)

    if partial_info is None:
        print("Partial offer is not valid.")
        return
    else:
        if as_json:
            ret = {
                "is_valid": not is_spent,
                "partial_info": partial_info.to_json_dict(),
                "partial_coin": partial_coin.to_json_dict(),
            }
            if launcher_coin is not None:
                ret["launcher_coin"] = launcher_coin.to_json_dict()
            print(json.dumps(ret, indent=2))
        else:
            display_partial_info(partial_info)
