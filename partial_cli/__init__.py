import rich_click as click

from partial_cli.puzzles import get_cmd
from partial_cli.puzzles.create import create_cmd
from partial_cli.puzzles.take import take_cmd
from partial_cli.show import show_cmd


@click.group("partial")
@click.pass_context
def partial_cmd(ctx):
    pass


partial_cmd.add_command(get_cmd)
partial_cmd.add_command(create_cmd)
partial_cmd.add_command(show_cmd)
partial_cmd.add_command(take_cmd)
