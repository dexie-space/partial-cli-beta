import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend

from chia.util.ints import uint64
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
from clvm.casts import int_to_bytes

from partial_cli.utils.shared import get_cat_puzzle_hash

MOD = Program.fromhex(
    "0xff02ffff01ff04ffff04ffff0149ffff04ff8200bfff808080ffff02ffff03ffff15ff8202ffff8080ffff01ff04ffff04ffff0146ffff04ff82017fff808080ffff04ffff02ff12ffff04ff02ffff04ff0bffff04ff2fffff04ff82017fffff04ffff02ff1cffff04ff02ffff04ff5fffff04ff8202ffff8080808080ff80808080808080ffff04ffff02ff1affff04ff02ffff04ff8202ffff80808080ffff02ffff03ffff15ffff11ff8200bfff8202ff80ff8080ffff01ff04ffff02ff16ffff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fffff04ff5fffff04ffff11ff8200bfff8202ff80ff808080808080808080ff8080ffff01ff018080ff0180808080ffff01ff02ff1effff04ff02ffff04ff0bffff04ff17ffff04ff8200bfff80808080808080ff018080ffff04ffff01ffffffff02ffff03ff05ffff01ff02ff10ffff04ff02ffff04ff0dffff04ffff0bffff0102ffff0bffff0101ffff010480ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0980ffff0bffff0102ff0bffff0bffff0101ff8080808080ff8080808080ffff010b80ff0180ff0bffff0102ffff0bffff0101ffff010280ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0580ffff0bffff0102ffff02ff10ffff04ff02ffff04ff07ffff04ffff0bffff0101ffff010180ff8080808080ffff0bffff0101ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff14ffff04ff02ffff04ff09ff80808080ffff02ff14ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff04ffff013fffff04ffff0bff0bffff02ff14ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ffff04ffff0133ffff04ffff02ff18ffff04ff02ffff04ff05ffff04ffff0bffff0101ff8200bf80ffff04ffff0bffff0101ff5f80ffff04ffff0bffff0101ff2f80ffff04ffff0bffff0101ff1780ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ff0580ff80808080808080808080ffff04ff8200bfff80808080ff04ffff04ffff0133ffff04ff05ffff04ff17ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ff808080ff018080"
)
MOD_HASH = MOD.get_tree_hash()


@dataclass
class PartialInfo:
    maker_puzzle_hash: bytes32
    public_key: G1Element
    tail_hash: bytes32
    rate: uint64
    offer_mojos: uint64

    def to_memos(self):
        return ["dexie_partial", json.dumps(self.to_json_dict())]

    def to_json_dict(self):
        return {
            "maker_puzzle_hash": self.maker_puzzle_hash.hex(),
            "public_key": str(self.public_key),
            "tail_hash": self.tail_hash.hex(),
            "rate": self.rate,
            "offer_mojos": self.offer_mojos,
        }

    @staticmethod
    def from_json_dict(data):
        return PartialInfo(
            bytes32.from_hexstr(data["maker_puzzle_hash"]),
            G1Element.from_bytes(bytes.fromhex(data["public_key"])),
            bytes32.from_hexstr(data["tail_hash"]),
            uint64(data["rate"]),
            uint64(data["offer_mojos"]),
        )


def get_partial_info(coin_spends) -> Optional[Tuple[Coin, PartialInfo]]:
    for cs in coin_spends:
        p = cs.puzzle_reveal.to_program()
        s = cs.solution.to_program()
        conditions = conditions_lib.parse_conditions_non_consensus(
            conditions=p.run(s).as_iter(), abstractions=False
        )
        for c in conditions:
            if type(c) is conditions_lib.CreateCoin:
                # check 1st memo
                if len(c.memos) == 2 and c.memos[0] == "dexie_partial".encode("utf-8"):
                    partial_info: PartialInfo = PartialInfo.from_json_dict(
                        json.loads(c.memos[1].decode("utf-8"))
                    )
                    eph_partial_coin = Coin(
                        cs.coin.name(),
                        c.puzzle_hash,
                        partial_info.offer_mojos,
                    )
                    return (eph_partial_coin, partial_info)
    return None


def get_puzzle(
    puzzle_hash: bytes32,
    public_key: G1Element,
    tail_hash: bytes32,
    rate: uint64,
    offer_mojos: uint64,
):
    cat_offer_mod_hash = get_cat_puzzle_hash(tail_hash, OFFER_MOD_HASH)

    p = MOD.curry(
        MOD_HASH,
        puzzle_hash,
        public_key,
        cat_offer_mod_hash,
        uint64(rate * 1e3),
        offer_mojos,
    )
    return p


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
