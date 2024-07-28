import rich_click as click


@click.command("show", help="Display the dexie partial offer information.")
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def show_cmd(ctx, offer_file):
    offer_bech32 = offer_file.read()
    print(offer_bech32)
