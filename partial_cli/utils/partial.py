from rich import box
from rich.console import Console
from rich.table import Column, Table
from rich.text import Text
from typing import Optional

from chia.types.blockchain_format.coin import Coin
from chia.util.bech32m import encode_puzzle_hash
from chia.util.ints import uint64

from partial_cli.config import prefix
from partial_cli.puzzles import MOD_HASH
from partial_cli.types.partial_info import PartialInfo


def get_amount_str(
    amount_mojos: uint64, wallet_name: Optional[str] = None, unit: int = 1
):
    if wallet_name is not None:
        return f"{amount_mojos / unit} {wallet_name}"

    return f"{amount_mojos} mojos"


def display_partial_info(
    partial_info: PartialInfo,
    partial_coin: Coin,
    is_valid: bool,
    offer_wallet_name: Optional[str] = None,
    offer_unit: int = 1,
    request_wallet_name: Optional[str] = None,
    request_unit: int = 1,
):
    coin_amount = partial_coin.amount
    request_amount = partial_info.get_output_mojos(coin_amount)

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
    table.add_row(
        "Offer Amount:", get_amount_str(coin_amount, offer_wallet_name, offer_unit)
    )
    table.add_row(
        "Request Amount:",
        get_amount_str(request_amount, request_wallet_name, request_unit),
    )
    table.add_row(
        "Offer Asset Id:",
        (
            "XCH"
            if partial_info.offer_asset_id == bytes(0)
            else f"0x{partial_info.offer_asset_id.hex()}"
        ),
    )
    table.add_row(
        "Initial Offer Mojos:",
        get_amount_str(partial_info.offer_mojos, offer_wallet_name, offer_unit),
    )
    table.add_row(
        "Request Asset Id:",
        (
            "XCH"
            if partial_info.request_asset_id == bytes(0)
            else f"0x{partial_info.request_asset_id.hex()}"
        ),
    )
    table.add_row(
        "Initial Request Mojos:",
        get_amount_str(partial_info.request_mojos, request_wallet_name, request_unit),
    )

    table.add_row("Rate:", f"{partial_info.get_rate():.24f}")

    table.add_row(
        "Fee Recipient:", f"{encode_puzzle_hash(partial_info.fee_puzzle_hash, prefix)}"
    )
    table.add_row("Fee Rate:", f"{partial_info.fee_rate/1e2}%")
    Console().print(table)
