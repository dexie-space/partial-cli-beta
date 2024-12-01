from dataclasses import dataclass
from typing import Optional

from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint16, uint64
from chia.wallet.cat_wallet.cat_utils import (
    match_cat_puzzle,
    get_innerpuzzle_from_puzzle,
)
from chia.wallet.trading.offer import Offer
from chia.wallet.uncurried_puzzle import uncurry_puzzle

from chia_rs import G1Element, G2Element

from partial_cli.puzzles import MOD, MOD_HASH


@dataclass
class PartialInfo:
    fee_puzzle_hash: bytes32
    fee_rate: uint16  # e.g., 3% is represented as 300
    maker_puzzle_hash: bytes32
    public_key: G1Element
    offer_asset_id: bytes
    offer_mojos: uint64  # initial offer mojos
    request_asset_id: bytes
    request_mojos: uint64  # initial request mojos

    def to_partial_puzzle(self):
        return MOD.curry(
            MOD_HASH,
            self.fee_puzzle_hash,
            self.fee_rate,
            self.maker_puzzle_hash,
            self.public_key,
            self.offer_asset_id,
            self.offer_mojos,
            self.request_asset_id,
            self.request_mojos,
        )

    def get_rate(self):
        return self.request_mojos / self.offer_mojos

    def get_output_mojos(self, input_mojos: uint64) -> uint64:
        return uint64(input_mojos * self.get_rate())

    def to_json_dict(self):
        return {
            "fee_puzzle_hash": self.fee_puzzle_hash.hex(),
            "fee_rate": self.fee_rate,
            "maker_puzzle_hash": self.maker_puzzle_hash.hex(),
            "public_key": str(self.public_key),
            "offer_asset_id": self.offer_asset_id.hex(),
            "offer_mojos": self.offer_mojos,
            "request_asset_id": self.request_asset_id.hex(),
            "request_mojos": self.request_mojos,
            "rate": self.get_rate(),
        }

    def get_next_partial_offer(
        self, partial_coin: Coin, request_mojos: uint64
    ) -> Optional[Offer]:
        new_amount = partial_coin.amount - request_mojos

        # create next offer if there is mojos left
        if new_amount > 0:
            puzzle = self.to_partial_puzzle()
            next_offer_cs = make_spend(
                coin=Coin(
                    parent_coin_info=partial_coin.name(),
                    puzzle_hash=puzzle.get_tree_hash(),
                    amount=new_amount,
                ),
                puzzle_reveal=puzzle,
                solution=Program.to(["dexie_partial"]),
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
                G1Element.from_bytes(bytes.fromhex(data["public_key"])),
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
            public_key=G1Element.from_bytes(curried_args[4].as_atom()),
            offer_asset_id=curried_args[5].as_atom(),
            offer_mojos=uint64(curried_args[6].as_int()),
            request_asset_id=curried_args[7].as_atom(),
            request_mojos=uint64(curried_args[8].as_int()),
        )
        return partial_info
