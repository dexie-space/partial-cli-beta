import rich_click as click

from partial_cli.puzzles import create_cmd, get_cmd
from partial_cli.show import show_cmd


@click.group("partial")
@click.pass_context
def partial_cmd(ctx):
    pass


partial_cmd.add_command(get_cmd)
partial_cmd.add_command(create_cmd)
partial_cmd.add_command(show_cmd)
