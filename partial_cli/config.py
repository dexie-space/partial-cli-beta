import os
import pathlib


from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH


chia_root = pathlib.Path(
    os.path.expanduser(os.environ.get("CHIA_ROOT", DEFAULT_ROOT_PATH))
)
chia_config = load_config(chia_root, "config.yaml")
self_hostname = chia_config["self_hostname"]
full_node_rpc_port = chia_config["full_node"]["rpc_port"]
wallet_rpc_port = chia_config["wallet"]["rpc_port"]

# configurable
# dexie should also check it
FEE_PH = bytes32.from_hexstr(
    # "bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5a" # sim
    "da3c6fd192afdb0e3318b0b44ddb102566fea251e74e8135be2317f4e50208a4"  # testnet11
)
# represented as an integer from 0 to 10,000
# e.g., 1% is represented as 100
FEE_RATE = 100
