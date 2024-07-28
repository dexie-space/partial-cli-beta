import os
import pathlib

from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH


chia_root = pathlib.Path(
    os.path.expanduser(os.environ.get("CHIA_ROOT", DEFAULT_ROOT_PATH))
)
chia_config = load_config(chia_root, "config.yaml")
self_hostname = chia_config["self_hostname"]
full_node_rpc_port = chia_config["full_node"]["rpc_port"]
wallet_rpc_port = chia_config["wallet"]["rpc_port"]
