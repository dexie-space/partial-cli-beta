from dataclasses import dataclass
from typing import Optional

from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.wallet.cat_wallet.cat_utils import CAT_MOD
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint16, uint64
from chia.wallet.cat_wallet.cat_utils import (
    construct_cat_puzzle,
    match_cat_puzzle,
    get_innerpuzzle_from_puzzle,
)
from chia.wallet.trading.offer import OFFER_MOD_HASH, Offer
from chia.wallet.uncurried_puzzle import uncurry_puzzle

from chia_rs import G2Element

from partial_cli.puzzles import MOD, MOD_HASH, get_partial_coin_solution


@dataclass
class PartialInfo:
    fee_puzzle_hash: bytes32
    fee_rate: uint16  # e.g., 3% is represented as 300
    maker_puzzle_hash: bytes32
    clawback_mod_hash: bytes32
    offer_asset_id: bytes
    offer_mojos: uint64  # initial offer mojos
    request_asset_id: bytes
    request_mojos: uint64  # initial request mojos

    def to_partial_puzzle(self) -> Program:
        request_settlement_hash = (
            OFFER_MOD_HASH
            if self.request_asset_id == bytes(0)
            else construct_cat_puzzle(
                CAT_MOD, self.request_asset_id, inner_puzzle_or_hash=OFFER_MOD_HASH
            ).get_tree_hash_precalc(OFFER_MOD_HASH)
        )
        return MOD.curry(
            MOD_HASH,
            self.fee_puzzle_hash,
            self.fee_rate,
            self.maker_puzzle_hash,
            self.clawback_mod_hash,
            self.offer_asset_id,
            self.offer_mojos,
            self.request_asset_id,
            self.request_mojos,
            request_settlement_hash,
        )

    def get_output_mojos(self, input_mojos: uint64) -> uint64:
        return uint64((input_mojos * self.request_mojos) / self.offer_mojos)

    def to_json_dict(self):
        return {
            "fee_puzzle_hash": self.fee_puzzle_hash.hex(),
            "fee_rate": self.fee_rate,
            "maker_puzzle_hash": self.maker_puzzle_hash.hex(),
            "clawback_mod_hash": self.clawback_mod_hash.hex(),
            "offer_asset_id": self.offer_asset_id.hex(),
            "offer_mojos": self.offer_mojos,
            "request_asset_id": self.request_asset_id.hex(),
            "request_mojos": self.request_mojos,
        }

    def get_next_partial_offer(
        self, partial_coin: Coin, request_mojos: uint64
    ) -> Optional[Offer]:
        new_amount = partial_coin.amount - request_mojos

        # create next offer if there is mojos left
        if new_amount > 0:
            puzzle = self.to_partial_puzzle()
            partial_ph = puzzle.get_tree_hash()
            new_partial_coin_ph = (
                partial_ph
                if self.offer_asset_id == bytes(0)
                else CAT_MOD.curry(
                    CAT_MOD.get_tree_hash(), self.offer_asset_id, partial_ph
                ).get_tree_hash_precalc(partial_ph)
            )
            new_partial_coin = Coin(
                parent_coin_info=partial_coin.name(),
                puzzle_hash=new_partial_coin_ph,
                amount=new_amount,
            )
            next_offer_cs = make_spend(
                coin=new_partial_coin,
                puzzle_reveal=puzzle,
                solution=get_partial_coin_solution(new_amount, new_partial_coin.name()),
            )

            next_offer_sb = SpendBundle([next_offer_cs], G2Element())
            next_offer = Offer.from_spend_bundle(next_offer_sb)
            return next_offer
        else:
            return None

    @staticmethod
    def from_json_dict(data) -> Optional["PartialInfo"]:
        try:
            return PartialInfo(
                bytes32.from_hexstr(data["fee_puzzle_hash"]),
                uint16(data["fee_rate"]),
                bytes32.from_hexstr(data["maker_puzzle_hash"]),
                bytes32.from_hexstr(data["clawback_mod_hash"]),
                bytes.fromhex(data["offer_asset_id"]),
                uint64(data["offer_mojos"]),
                bytes.fromhex(data["request_asset_id"]),
                uint64(data["request_mojos"]),
            )
        except Exception:
            return None

    @staticmethod
    def from_coin_spend(cs: CoinSpend) -> Optional["PartialInfo"]:
        # check if it's CAT spend
        matched_cat_puzzle = match_cat_puzzle(
            uncurry_puzzle(cs.puzzle_reveal.to_program())
        )

        puzzle = (
            cs.puzzle_reveal.to_program()
            if matched_cat_puzzle is None
            else get_innerpuzzle_from_puzzle(cs.puzzle_reveal.to_program())
        )

        uncurried_puzzle = uncurry_puzzle(puzzle)

        # check if the uncurried puzzle is the same as the partial puzzle
        if uncurried_puzzle.mod.get_tree_hash() != MOD_HASH:
            return None

        curried_args = list(uncurried_puzzle.args.as_iter())
        partial_info = PartialInfo(
            fee_puzzle_hash=bytes32.from_bytes(curried_args[1].as_atom()),
            fee_rate=uint16(curried_args[2].as_int()),
            maker_puzzle_hash=bytes32.from_bytes(curried_args[3].as_atom()),
            clawback_mod_hash=bytes32.from_bytes(curried_args[4].as_atom()),
            offer_asset_id=curried_args[5].as_atom(),
            offer_mojos=uint64(curried_args[6].as_int()),
            request_asset_id=curried_args[7].as_atom(),
            request_mojos=uint64(curried_args[8].as_int()),
        )
        return partial_info
