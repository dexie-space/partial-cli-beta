from typing import List, Optional

from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64
from chia.wallet.cat_wallet.cat_utils import SpendableCAT
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle
from chia.wallet.lineage_proof import LineageProof
from chia.wallet.trading.offer import ZERO_32
from chia.wallet.uncurried_puzzle import uncurry_puzzle
from chia_rs import G2Element

from partial_cli.utils.rpc import is_coin_spent, get_coin_spend_from_name

# partial.clsp
MOD = Program.fromhex(
    "0xff02ffff01ff04ffff04ffff0149ffff04ff820bffff808080ffff02ffff03ffff15ff825fffff8080ffff01ff04ffff02ffff03ffff15ffff11ff820bffff825fff80ff8080ffff01ff04ffff0133ffff04ff822fffffff04ffff11ff820bffff825fff80ff80808080ffff01ff04ffff0101ff808080ff0180ffff04ffff04ffff0146ffff04ff8217ffff808080ffff04ffff02ff1affff04ff02ffff04ff8200bfffff04ff822fffff8080808080ffff04ffff02ff16ffff04ff02ffff04ff2fffff04ff8202ffffff04ff8217ffffff04ffff02ff3cffff04ff02ffff04ff82017fffff04ff8205ffffff04ff825fffff808080808080ff80808080808080ffff04ffff02ff2effff04ff02ffff04ffff11ff825fffffff02ff12ffff04ff02ffff04ff17ffff04ff825fffff808080808080ff80808080ffff04ffff04ffff0133ffff04ff0bffff04ffff02ff12ffff04ff02ffff04ff17ffff04ff825fffff8080808080ff80808080ff80808080808080ffff01ff02ff3effff04ff02ffff04ff2fffff04ff5fffff04ff820bffffff04ff8300bfffff8080808080808080ff018080ffff04ffff01ffffffff0bffff0102ffff0bffff0102ffff06ffff05ffff01ffffa04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459aa09dcf97a184f32623d11a73124ceb99a5709b083721e878a16d78f596718ba7b2ffa102a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222a102a8d5dd63fba471ebcb1f3e8f7c1e1879b7152a6e7298a91ce119a63400ade7c58080ff0580ffff0bffff0102ff0bffff05ffff05ffff01ffffa04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459aa09dcf97a184f32623d11a73124ceb99a5709b083721e878a16d78f596718ba7b2ffa102a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222a102a8d5dd63fba471ebcb1f3e8f7c1e1879b7152a6e7298a91ce119a63400ade7c580808080ff02ffff03ff05ffff01ff0bffff06ffff06ffff01ffffa04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459aa09dcf97a184f32623d11a73124ceb99a5709b083721e878a16d78f596718ba7b2ffa102a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222a102a8d5dd63fba471ebcb1f3e8f7c1e1879b7152a6e7298a91ce119a63400ade7c58080ffff02ff10ffff04ff02ffff04ff09ffff04ffff02ff18ffff04ff02ffff04ff0dff80808080ff808080808080ffff01ff06ffff05ffff01ffffa04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459aa09dcf97a184f32623d11a73124ceb99a5709b083721e878a16d78f596718ba7b2ffa102a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222a102a8d5dd63fba471ebcb1f3e8f7c1e1879b7152a6e7298a91ce119a63400ade7c5808080ff0180ffff0bffff05ffff06ffff01ffffa04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459aa09dcf97a184f32623d11a73124ceb99a5709b083721e878a16d78f596718ba7b2ffa102a12871fee210fb8619291eaea194581cbd2531e4b23759d225f6806923f63222a102a8d5dd63fba471ebcb1f3e8f7c1e1879b7152a6e7298a91ce119a63400ade7c58080ffff02ff10ffff04ff02ffff04ff05ffff04ffff02ff18ffff04ff02ffff04ff07ff80808080ff808080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2cffff04ff02ffff04ff09ff80808080ffff02ff2cffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff05ffff14ffff12ff0bff1780ff058080ffffff05ffff14ffff12ff05ff0b80ffff018227108080ff04ffff0148ffff04ffff02ffff03ff05ffff01ff02ff14ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ffff04ffff0bffff0101ff0580ffff04ff0bff80808080808080ffff010b80ff0180ff808080ffff04ffff013fffff04ffff0bffff02ffff03ff0bffff01ff02ff14ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ffff04ffff0bffff0101ff0b80ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ff80808080808080ffff01ff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e780ff0180ffff02ff2cffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ffff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ff04ffff02ffff03ffff15ff2fff8080ffff01ff04ffff0134ffff04ff2fff808080ffff01ff04ffff0101ff808080ff0180ffff04ffff04ffff0133ffff04ff05ffff04ff17ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ff80808080ff018080"
)
MOD_HASH = MOD.get_tree_hash()

# fee.clsp
FEE_MOD = Program.fromhex(
    "0xff02ffff01ff02ff02ffff04ff02ffff04ff05ffff04ff0bff8080808080ffff04ffff01ff05ffff14ffff12ff05ff0b80ffff018227108080ff018080"
)

# rate.clsp
RATE_MOD = Program.fromhex(
    "0xff02ffff01ff02ff02ffff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fff80808080808080ffff04ffff01ff02ffff03ff05ffff01ff02ffff03ff0bffff01ff0880ffff01ff05ffff14ff2fff17808080ff0180ffff01ff05ffff14ffff12ff2fffff018600e8d4a5100080ff17808080ff0180ff018080"
)


def get_partial_coin_solution(my_amount: uint64, my_id: bytes32) -> Program:
    return Program.to(
        [
            my_amount,
            my_id,
            ZERO_32,
            uint64(1),
            uint64(0),
        ]
    )


def get_partial_spendable_cat(
    asset_id: bytes32,
    partial_coin: Coin,
    partial_puzzle: Program,
    parent_coin: Coin,
    parent_inner_puzzle_hash: bytes32,
    partial_solution: Program = None,
) -> SpendableCAT:

    return SpendableCAT(
        coin=partial_coin,
        limitations_program_hash=asset_id,
        inner_puzzle=partial_puzzle,
        inner_solution=(
            get_partial_coin_solution(partial_coin.amount, partial_coin.name())
            if partial_solution is None
            else partial_solution
        ),
        lineage_proof=LineageProof(
            parent_coin.parent_coin_info,
            parent_inner_puzzle_hash,
            parent_coin.amount,
        ),
    )


def is_partial_coin_spend(cs: CoinSpend) -> bool:
    # check if it's CAT spend
    matched_cat_puzzle = match_cat_puzzle(uncurry_puzzle(cs.puzzle_reveal.to_program()))
    solution_python = (
        cs.solution.to_program()
        if matched_cat_puzzle is None
        else cs.solution.to_program().first()
    ).as_python()

    return len(solution_python) == 5 and solution_python == get_partial_coin_solution(
        cs.coin.amount, cs.coin.name()
    )


def get_launcher_coin_spend(
    coin_spends: List[CoinSpend], partial_coin: Optional[Coin] = None
) -> Optional[CoinSpend]:
    if partial_coin is None:
        partial_cs = get_partial_coin_spend(coin_spends)
        partial_coin = partial_cs.coin if partial_cs is not None else None

    if partial_coin is not None:
        for cs in coin_spends:
            name = cs.coin.name()
            if (
                name != partial_coin.name()  # not the same coin
                and name == partial_coin.parent_coin_info  # parent coin
                and cs.coin.puzzle_hash
                != partial_coin.puzzle_hash  # not the same puzzle hash
            ):
                return cs

    return None


def get_partial_coin_spend(coin_spends: List[CoinSpend]) -> Optional[CoinSpend]:
    for cs in coin_spends:
        if is_partial_coin_spend(cs):
            return cs

    return None


def get_non_partial_coin_spends(coin_spends: List[CoinSpend]) -> List[CoinSpend]:
    return list(
        filter(
            lambda cs: (
                not is_partial_coin_spend(cs) and cs.coin.parent_coin_info != ZERO_32
            ),
            coin_spends,
        )
    )


async def get_partial_coin_parent_coin_spend(
    coin_spends: List[CoinSpend], partial_coin: Coin
) -> Optional[CoinSpend]:
    launcher_cs = get_launcher_coin_spend(coin_spends, partial_coin)

    if launcher_cs is not None:
        return launcher_cs
    else:
        # get parent coin spend which is also a partial coin spend
        return await get_coin_spend_from_name(partial_coin.parent_coin_info)


async def get_create_offer_coin_sb(
    coin_spends: List[CoinSpend], aggregated_signature: G2Element
) -> Optional[SpendBundle]:
    non_partial_coin_spends = get_non_partial_coin_spends(coin_spends)
    if len(non_partial_coin_spends) == 0:
        return None

    for cs in non_partial_coin_spends:
        is_spent = await is_coin_spent(cs.coin.name())
        if is_spent:
            return None

    return SpendBundle(non_partial_coin_spends, aggregated_signature)
