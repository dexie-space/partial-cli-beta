import os
import pathlib
import rich_click as click

from rich import box
from rich.console import Console
from rich.table import Column, Table

from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16

chia_root = pathlib.Path(
    os.path.expanduser(os.environ.get("CHIA_ROOT", DEFAULT_ROOT_PATH))
)
chia_config = load_config(chia_root, "config.yaml")
self_hostname = chia_config["self_hostname"]
full_node_rpc_port = chia_config["full_node"]["rpc_port"]
wallet_rpc_port = chia_config["wallet"]["rpc_port"]

selected_network = chia_config["selected_network"]

genesis_challenge = bytes.fromhex(
    os.path.expanduser(
        os.environ.get(
            "CHIA_GENESIS_CHALLENGE",
            chia_config["network_overrides"]["constants"][selected_network][
                "GENESIS_CHALLENGE"
            ],
        )
    )
)


# configurable
# dexie should also check it
FEE_PH = bytes32.from_hexstr(
    os.path.expanduser(
        os.environ.get(
            "DEXIE_PARTIAL_FEE_PH",
            "bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5a",  # sim
        )
    )
)
# represented as an integer from 0 to 10,000
# e.g., 1% is represented as 100
FEE_RATE = uint16(os.path.expanduser(os.environ.get("DEXIE_PARTIAL_FEE_RATE", "100")))


@click.command("config", help="display the cli config")
def config_cmd():
    table = Table(
        Column(justify="left"),
        Column(),
        show_header=False,
        box=box.ROUNDED,
    )

    table.add_row("chia_root:", f"{chia_root}")
    table.add_row("selected_netswork:", selected_network)
    table.add_row("self_hostname:", self_hostname)
    table.add_row("full_node_rpc_port", f"{full_node_rpc_port}")
    table.add_row("wallet_rpc_port", f"{wallet_rpc_port}")
    table.add_row("genesis_challenge", f"0x{genesis_challenge.hex()}")
    table.add_section()
    table.add_row("fee puzzle hash", f"0x{FEE_PH}")
    table.add_row("fee rate", f"{FEE_RATE}")
    Console().print(table)
