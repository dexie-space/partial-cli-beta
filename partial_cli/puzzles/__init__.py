from typing import List, Optional

from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.wallet.trading.offer import ZERO_32

from chia_rs import G2Element

from partial_cli.utils.rpc import is_coin_spent

# partial.clsp
MOD = Program.fromhex(
    "0xff02ffff01ff04ffff04ffff0149ffff04ff8205ffff808080ffff02ffff03ffff15ff822fffff8080ffff01ff02ff14ffff04ff02ffff04ffff04ffff04ffff0146ffff04ff820bffff808080ffff04ffff02ff1affff04ff02ffff04ff2fffff04ff82017fffff04ff820bffffff04ffff02ff1cffff04ff02ffff04ff8202ffffff04ff822fffff8080808080ff80808080808080ffff04ffff02ff16ffff04ff02ffff04ffff11ff822fffffff02ff12ffff04ff02ffff04ff17ffff04ff822fffff808080808080ff80808080ffff04ffff04ffff0133ffff04ff0bffff04ffff02ff12ffff04ff02ffff04ff17ffff04ff822fffff8080808080ff80808080ff8080808080ffff04ffff02ffff03ffff15ffff11ff8205ffff822fff80ff8080ffff01ff04ffff04ffff0148ffff04ff8217ffff808080ffff04ffff04ffff0133ffff04ff8217ffffff04ffff11ff8205ffff822fff80ff80808080ff808080ffff01ff018080ff0180ff8080808080ffff01ff02ff1effff04ff02ffff04ff2fffff04ff5fffff04ff8205ffffff04ff825fffff8080808080808080ff018080ffff04ffff01ffffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff08ffff04ff02ffff04ff09ff80808080ffff02ff08ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff02ffff03ff0bffff01ff02ff14ffff04ff02ffff04ffff02ffff03ff13ffff01ff04ff13ff0580ffff010580ff0180ffff04ff1bff8080808080ffff010580ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff05ffff14ffff12ff05ff0b80ffff018227108080ff04ffff013fffff04ffff0bff0bffff02ff08ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ffff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ff04ffff02ffff03ffff15ff2fff8080ffff01ff04ffff0134ffff04ff2fff808080ffff01ff04ffff0101ff808080ff0180ffff04ffff04ffff0133ffff04ff05ffff04ffff11ff17ff2f80ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ff80808080ff018080"
)
MOD_HASH = MOD.get_tree_hash()

# fee.clsp
FEE_MOD = Program.fromhex(
    "0xff02ffff01ff02ff02ffff04ff02ffff04ff05ffff04ff0bff8080808080ffff04ffff01ff05ffff14ffff12ff05ff0b80ffff018227108080ff018080"
)

# rate.clsp
RATE_MOD = Program.fromhex(
    "0xff02ffff01ff02ff02ffff04ff02ffff04ff05ffff04ff0bff8080808080ffff04ffff01ff05ffff14ffff12ff0bffff018600e8d4a5100080ff058080ff018080"
)


def get_partial_coin_spend(coin_spends: List[CoinSpend]) -> Optional[CoinSpend]:
    return next(
        (
            cs
            for cs in coin_spends
            if cs.solution.to_program() == Program.to(["dexie_partial"])
        ),
        None,
    )


def get_non_partial_coin_spends(coin_spends: List[CoinSpend]) -> List[CoinSpend]:
    return list(
        filter(
            lambda cs: (
                cs.solution.to_program() != Program.to(["dexie_partial"])
                and cs.coin.parent_coin_info != ZERO_32
            ),
            coin_spends,
        )
    )


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
