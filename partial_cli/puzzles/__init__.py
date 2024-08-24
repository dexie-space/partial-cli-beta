import json
import rich_click as click


from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint16, uint64

from chia_rs import G1Element

from partial_cli.puzzles.partial import PartialInfo

from partial_cli.utils.shared import Bytes32ParamType, G1ElementParamType


# get
@click.command("get", help="get a serialized curried puzzle of the partial offer coin")
@click.option(
    "-fph",
    "--fee-puzzle-hash",
    required=True,
    default=None,
    help="Fee puzzle hash",
    type=Bytes32ParamType(),
)
@click.option(
    "-fr",
    "--fee-rate",
    required=True,
    default=None,
    help="Represented as an integer from 0 to 10,000 (3% is 300)",
    type=uint16,
)
@click.option(
    "-ph",
    "--puzzle-hash",
    required=True,
    default=None,
    help="puzzle hash",
    type=Bytes32ParamType(),
)
@click.option(
    "-pk",
    "--public-key",
    required=True,
    default=None,
    help="public key",
    type=G1ElementParamType(),
)
@click.option(
    "-t",
    "--tail-hash",
    required=True,
    default=None,
    help="CAT tail hash",
    type=Bytes32ParamType(),
)
@click.option(
    "-r",
    "--rate",
    required=True,
    default=None,
    help="Rate in 1000 (e.g., 1 XCH for 128.68 CAT is 128680)",
    type=uint64,
)
@click.option(
    "-a",
    "--offer-mojos",
    required=True,
    default=None,
    help="Offer amount in mojos",
    type=uint64,
)
@click.pass_context
def get_cmd(
    ctx,
    fee_puzzle_hash: bytes32,
    fee_rate: uint16,
    puzzle_hash: bytes32,
    public_key: G1Element,
    tail_hash: bytes32,
    rate: uint64,
    offer_mojos: uint64,
):
    partial_info = PartialInfo(
        fee_puzzle_hash=fee_puzzle_hash,
        fee_rate=fee_rate,
        maker_puzzle_hash=puzzle_hash,
        public_key=public_key,
        tail_hash=tail_hash,
        rate=rate,
        offer_mojos=offer_mojos,
    )
    p = partial_info.to_partial_puzzle()
    ret = {"puzzle_hash": p.get_tree_hash().hex(), "puzzle": str(p)}
    print(json.dumps(ret, indent=2))
