from rich import box
from rich.console import Console
from rich.table import Column, Table
from rich.text import Text

from chia.types.blockchain_format.coin import Coin
from chia.util.bech32m import encode_puzzle_hash

from partial_cli.config import prefix
from partial_cli.puzzles import MOD_HASH
from partial_cli.types.partial_info import PartialInfo


def display_partial_info(partial_info: PartialInfo, partial_coin: Coin, is_valid: bool):
    coin_amount = partial_coin.amount
    total_request_cat_mojos = coin_amount * partial_info.rate * 1e-12

    table = Table(
        Column(justify="left"),
        Column(),
        show_header=False,
        box=box.ROUNDED,
    )
    table.add_row(
        "Valid:",
        Text("Yes", style="bold green") if is_valid else Text("No", style="bold red"),
    )
    table.add_row("MOD_HASH:", f"0x{MOD_HASH.hex()}")
    table.add_row("Partial Offer Coin Name:", f"0x{partial_coin.name().hex()}")
    table.add_section()
    table.add_row("Total Offer Amount:", f"{coin_amount/1e12} XCH")
    table.add_row("Total Request Amount:", f"{total_request_cat_mojos/1e3} CATs")
    table.add_row(
        "Offer Asset Id:",
        (
            "XCH"
            if partial_info.offer_asset_id == bytes(0)
            else f"0x{partial_info.offer_asset_id.hex()}"
        ),
    )
    table.add_row(
        "Request Asset Id:",
        (
            "XCH"
            if partial_info.request_asset_id == bytes(0)
            else f"0x{partial_info.request_asset_id.hex()}"
        ),
    )
    table.add_row("Rate (1 XCH):", f"{partial_info.rate/1e3} CATs")

    table.add_row(
        "Fee Recipient:", f"{encode_puzzle_hash(partial_info.fee_puzzle_hash, prefix)}"
    )
    table.add_row("Fee Rate:", f"{partial_info.fee_rate/1e2}%")
    Console().print(table)
