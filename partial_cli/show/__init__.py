import json
import rich_click as click

import chia.wallet.conditions as conditions_lib
from chia.wallet.trading.offer import Offer


@click.command("show", help="Display the dexie partial offer information.")
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def show_cmd(ctx, offer_file):
    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb = offer.to_spend_bundle()

    partial_info = None

    for cs in sb.coin_spends:
        p = cs.puzzle_reveal.to_program()
        s = cs.solution.to_program()
        conditions = conditions_lib.parse_conditions_non_consensus(
            conditions=p.run(s).as_iter(), abstractions=False
        )
        for c in conditions:
            if type(c) is conditions_lib.CreateCoin:
                # check 1st memo
                if len(c.memos) == 2 and c.memos[0] == "dexie_partial".encode("utf-8"):
                    partial_info = json.loads(c.memos[1].decode("utf-8"))
                    break

    if partial_info is None:
        print("No partial information found.")
        return
    else:
        print(json.dumps(partial_info, indent=2))
