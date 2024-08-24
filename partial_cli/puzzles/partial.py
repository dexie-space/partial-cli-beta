import asyncio
import json
from dataclasses import dataclass
from rich import box
from rich.console import Console
from rich.table import Column, Table
from rich.text import Text
from typing import Any, Dict, List, Optional, Tuple

from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend

from chia.util.ints import uint16, uint64
from chia.wallet.cat_wallet.cat_utils import (
    CAT_MOD,
    SpendableCAT,
    match_cat_puzzle,
    unsigned_spend_bundle_for_spendable_cats,
)
import chia.wallet.conditions as conditions_lib

from chia.wallet.lineage_proof import LineageProof
from chia.wallet.trading.offer import OFFER_MOD, OFFER_MOD_HASH, ZERO_32, Offer
from chia.wallet.uncurried_puzzle import uncurry_puzzle

from chia_rs import G1Element

from partial_cli.config import (
    FEE_PH,
    FEE_RATE,
    self_hostname,
    full_node_rpc_port,
    chia_root,
    chia_config,
)
from partial_cli.utils.rpc import with_full_node_rpc_client
from partial_cli.utils.shared import get_cat_puzzle_hash

MOD = Program.fromhex(
    "0xff02ffff01ff04ffff04ffff013cffff04ff2fff808080ffff04ffff04ffff0149ffff04ff8202ffff808080ffff02ffff03ffff15ff820bffff8080ffff01ff04ffff04ffff0146ffff04ff8205ffff808080ffff04ffff02ff12ffff04ff02ffff04ff2fffff04ff8200bfffff04ff8205ffffff04ffff02ff1cffff04ff02ffff04ff82017fffff04ff820bffff8080808080ff80808080808080ffff04ffff02ff1affff04ff02ffff04ff820bffff80808080ffff02ffff03ffff15ffff11ff8202ffff820bff80ff8080ffff01ff04ffff02ff16ffff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fffff04ff5fffff04ff8200bfffff04ff82017fffff04ffff11ff8202ffff820bff80ff8080808080808080808080ff8080ffff01ff018080ff0180808080ffff01ff02ff1effff04ff02ffff04ff2fffff04ff5fffff04ff8202ffff80808080808080ff01808080ffff04ffff01ffffffff02ffff03ff05ffff01ff02ff10ffff04ff02ffff04ff0dffff04ffff0bffff0102ffff0bffff0101ffff010480ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0980ffff0bffff0102ff0bffff0bffff0101ff8080808080ff8080808080ffff010b80ff0180ff0bffff0102ffff0bffff0101ffff010280ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0580ffff0bffff0102ffff02ff10ffff04ff02ffff04ff07ffff04ffff0bffff0101ffff010180ff8080808080ffff0bffff0101ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff14ffff04ff02ffff04ff09ff80808080ffff02ff14ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff04ffff013fffff04ffff0bffff02ff18ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ff80808080808080ffff02ff14ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ffff04ffff0133ffff04ffff02ff18ffff04ff02ffff04ff05ffff04ffff0bffff0101ff8202ff80ffff04ffff0bffff0101ff82017f80ffff04ffff0bffff0101ff8200bf80ffff04ffff0bffff0101ff5f80ffff04ffff0bffff0101ff2f80ffff04ffff0bffff0101ff1780ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ff0580ff808080808080808080808080ffff04ff8202ffff80808080ff04ffff04ffff0133ffff04ff05ffff04ff17ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ff808080ff018080"
)
MOD_HASH = MOD.get_tree_hash()


@dataclass
class PartialInfo:
    fee_puzzle_hash: bytes32
    fee_rate: uint16  # e.g., 3% is represented as 300
    maker_puzzle_hash: bytes32
    public_key: G1Element
    tail_hash: bytes32
    rate: uint64  # e.g., 1 XCH = 100 CATs, rate = 100
    offer_mojos: uint64

    def cat_puzzle_hash(self):
        return get_cat_puzzle_hash(self.tail_hash, OFFER_MOD_HASH)

    def to_partial_puzzle(self):
        return MOD.curry(
            MOD_HASH,
            self.fee_puzzle_hash,
            self.fee_rate,
            self.maker_puzzle_hash,
            self.public_key,
            self.tail_hash,
            self.rate,
            self.offer_mojos,
        )

    def to_memos(self):
        return ["dexie_partial", json.dumps(self.to_json_dict())]

    def to_json_dict(self):
        return {
            "fee_puzzle_hash": self.fee_puzzle_hash.hex(),
            "fee_rate": self.fee_rate,
            "maker_puzzle_hash": self.maker_puzzle_hash.hex(),
            "public_key": str(self.public_key),
            "tail_hash": self.tail_hash.hex(),
            "cat_offer_mod_hash": self.cat_puzzle_hash().hex(),
            "rate": self.rate,
            "offer_mojos": self.offer_mojos,
        }

    @staticmethod
    def from_json_dict(data):
        return PartialInfo(
            bytes32.from_hexstr(data["fee_puzzle_hash"]),
            uint16(data["fee_rate"]),
            bytes32.from_hexstr(data["maker_puzzle_hash"]),
            G1Element.from_bytes(bytes.fromhex(data["public_key"])),
            bytes32.from_hexstr(data["tail_hash"]),
            uint64(data["rate"]),
            uint64(data["offer_mojos"]),
        )


@with_full_node_rpc_client(self_hostname, full_node_rpc_port, chia_root, chia_config)
async def get_partial_info_from_parent_coin_info(
    full_node_rpc_client: FullNodeRpcClient, parent_coin_info: bytes32
):
    coin_record = await full_node_rpc_client.get_coin_record_by_name(parent_coin_info)
    if coin_record is None:
        raise Exception(f"Coin {parent_coin_info} not found.")

    coin_spend = await full_node_rpc_client.get_puzzle_and_solution(
        parent_coin_info, coin_record.spent_block_index
    )

    if coin_spend is None:
        raise Exception(f"Coin {parent_coin_info} not spent.")

    solutions = list(coin_spend.solution.to_program().as_iter())
    uncurried_puzzle = uncurry_puzzle(coin_spend.puzzle_reveal.to_program())
    assert uncurried_puzzle.mod.get_tree_hash() == MOD_HASH
    curried_args = list(uncurried_puzzle.args.as_iter())
    partial_info = PartialInfo(
        fee_puzzle_hash=bytes32.from_bytes(curried_args[1].as_atom()),
        fee_rate=uint16(curried_args[2].as_int()),
        maker_puzzle_hash=bytes32.from_bytes(curried_args[3].as_atom()),
        public_key=G1Element.from_bytes(curried_args[4].as_atom()),
        tail_hash=bytes32.from_bytes(curried_args[5].as_atom()),
        rate=uint64(curried_args[6].as_int()),
        offer_mojos=uint64(curried_args[7].as_int()) - uint64(solutions[1].as_int()),
    )
    return partial_info


@with_full_node_rpc_client(self_hostname, full_node_rpc_port, chia_root, chia_config)
async def get_launcher_or_partial_cs(
    full_node_rpc_client: FullNodeRpcClient, coin_spends
):
    assert len(coin_spends) == 1
    cs = coin_spends[0]
    coin_name = cs.coin.name()
    coin_record = await full_node_rpc_client.get_coin_record_by_name(coin_name)
    return cs, coin_record.spent


def get_partial_info(cs) -> Optional[Tuple[Coin, PartialInfo]]:
    try:
        solution = cs.solution.to_program()
        if len(list(solution.as_iter())) == 0:  # empty solution
            # child partial offer coin
            parent_coin_info = cs.coin.parent_coin_info
            partial_info = asyncio.run(
                get_partial_info_from_parent_coin_info(parent_coin_info)
            )
            return (cs.coin, partial_info, None)
        else:
            # launcher
            p = cs.puzzle_reveal.to_program()
            s = cs.solution.to_program()
            conditions = conditions_lib.parse_conditions_non_consensus(
                conditions=p.run(s).as_iter(), abstractions=False
            )
            for c in conditions:
                if type(c) is conditions_lib.CreateCoin:
                    # check 1st memo
                    if len(c.memos) == 2 and c.memos[0] == "dexie_partial".encode(
                        "utf-8"
                    ):
                        partial_info: PartialInfo = PartialInfo.from_json_dict(
                            json.loads(c.memos[1].decode("utf-8"))
                        )
                        eph_partial_coin = Coin(
                            cs.coin.name(),
                            c.puzzle_hash,
                            partial_info.offer_mojos,
                        )
                        return (eph_partial_coin, partial_info, cs.coin)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def process_taker_offer(taker_offer: Offer, maker_request_payments):
    sb = taker_offer.to_spend_bundle()
    taker_offer_coin_spends = sb.coin_spends
    # partial_taker coin spends & notarized payments
    coin_spends: Dict[str, CoinSpend] = {}  # offer input CAT coins
    notarized_payments_solutions: List[Any] = []  # request XCH payments

    for cs in taker_offer_coin_spends:
        if cs.coin.parent_coin_info != ZERO_32:
            coin_name = cs.coin.name().hex()
            coin_spends[coin_name] = cs
        else:
            solutions = cs.solution.to_program().as_python()
            notarized_payments_solutions.append(solutions)

    settlement_spendable_cats: List[SpendableCAT] = []  # settlement spendable CAT
    for tail_hash, coins in taker_offer.get_offered_coins().items():
        for coin in coins:
            parent_cs = coin_spends[coin.parent_coin_info.hex()]
            matched_cat_puzzle = match_cat_puzzle(
                uncurry_puzzle(parent_cs.puzzle_reveal.to_program())
            )

            if matched_cat_puzzle is None:
                # TODO: raise error?
                continue

            parent_inner_puzzle_hash = list(matched_cat_puzzle)[2].get_tree_hash()
            lineage_proof = LineageProof(
                parent_cs.coin.parent_coin_info,
                parent_inner_puzzle_hash,
                uint64(parent_cs.coin.amount),
            )

            # payment to maker
            intermediary_token_reserve_coin_inner_solution = [maker_request_payments]

            spendable_cat = SpendableCAT(
                coin=coin,
                limitations_program_hash=tail_hash,
                inner_puzzle=OFFER_MOD,
                inner_solution=intermediary_token_reserve_coin_inner_solution,
                lineage_proof=lineage_proof,
            )
            settlement_spendable_cats.append(spendable_cat)

    settlement_coin_spends = unsigned_spend_bundle_for_spendable_cats(
        CAT_MOD, settlement_spendable_cats
    ).coin_spends

    taker_coin_spends = list(coin_spends.values()) + settlement_coin_spends

    return (
        taker_coin_spends,
        Program.to(notarized_payments_solutions[0]),
        sb.aggregated_signature,
    )


def display_partial_info(partial_info: PartialInfo, is_valid: bool):
    total_request_cat_mojos = partial_info.offer_mojos * partial_info.rate * 1e-12

    table = Table(
        Column(justify="left"),
        Column(),
        show_header=False,
        box=box.ROUNDED,
    )
    table.add_row("MOD_HASH:", f"0x{MOD_HASH.hex()}")
    table.add_row("Partial Offer is Valid:", "Yes" if is_valid else "No")
    table.add_row("Total Offer Amount:", f"{partial_info.offer_mojos/1e12} XCH")
    table.add_row("Total Request Amount:", f"{total_request_cat_mojos/1e3} CATs")
    table.add_row("Request Tail Hash:", f"0x{partial_info.tail_hash.hex()}")
    table.add_row("Rate (1 XCH):", f"{partial_info.rate/1e3} CATs")

    table.add_row("Fee Rate:", f"{partial_info.fee_rate/1e2}%")
    Console().print(table)
