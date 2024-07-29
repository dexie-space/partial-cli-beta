import json
import rich_click as click

from chia.wallet.trading.offer import Offer

from partial_cli.puzzles.partial import PartialInfo, get_partial_info


@click.command("show", help="Display the dexie partial offer information.")
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def show_cmd(ctx, offer_file):
    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb = offer.to_spend_bundle()

    partial_info: PartialInfo = get_partial_info(sb.coin_spends)

    if partial_info is None:
        print("No partial information found.")
        return
    else:
        print(json.dumps(partial_info.to_json_dict(), indent=2))
