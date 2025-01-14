import os
import pathlib
import tempfile

from chia.types.blockchain_format.program import Program

from partial_cli.puzzles import MOD as PARTIAL
from partial_cli.puzzles import FEE_MOD, REQ_MOJOS_MOD, STD_CLAWBACK_MOD

from clvm_tools_rs import compile_clvm as compile_clvm_rust

chia_puzzles_root = f"{os.getcwd()}/partial_cli/puzzles"
partial_clsp = pathlib.Path(f"{chia_puzzles_root}/partial.clsp").read_text()
fee_clsp = pathlib.Path(f"{chia_puzzles_root}/fee.clsp").read_text()
req_mojos_clsp = pathlib.Path(f"{chia_puzzles_root}/request-mojos.clsp").read_text()
standard_partial_clawback_clsp = pathlib.Path(
    f"{chia_puzzles_root}/standard_partial_clawback.clsp"
).read_text()


class TestPuzzleHashes:
    def test_partial_puzzle_hash(self):
        temp_clvm = tempfile.NamedTemporaryFile()
        temp_out = tempfile.NamedTemporaryFile().name
        pathlib.Path(temp_clvm.name).write_text(partial_clsp)
        compile_clvm_rust(temp_clvm.name, temp_out, [chia_puzzles_root, "."])
        output = pathlib.Path(temp_out).read_text()
        puzzle = Program.fromhex(output)
        assert puzzle.get_tree_hash() == PARTIAL.get_tree_hash()

    def test_fee_puzzle_hash(self):
        temp_clvm = tempfile.NamedTemporaryFile()
        temp_out = tempfile.NamedTemporaryFile().name

        pathlib.Path(temp_clvm.name).write_text(fee_clsp)
        compile_clvm_rust(temp_clvm.name, temp_out, [chia_puzzles_root, "."])
        output = pathlib.Path(temp_out).read_text()
        puzzle = Program.fromhex(output)
        assert puzzle.get_tree_hash() == FEE_MOD.get_tree_hash()

    def test_request_mojos_puzzle_hash(self):
        temp_clvm = tempfile.NamedTemporaryFile()
        temp_out = tempfile.NamedTemporaryFile().name

        pathlib.Path(temp_clvm.name).write_text(req_mojos_clsp)
        compile_clvm_rust(temp_clvm.name, temp_out, [chia_puzzles_root, "."])
        output = pathlib.Path(temp_out).read_text()
        puzzle = Program.fromhex(output)
        assert puzzle.get_tree_hash() == REQ_MOJOS_MOD.get_tree_hash()

    def test_standard_clawback_puzzle_hash(self):
        temp_clvm = tempfile.NamedTemporaryFile()
        temp_out = tempfile.NamedTemporaryFile().name
        pathlib.Path(temp_clvm.name).write_text(standard_partial_clawback_clsp)
        compile_clvm_rust(temp_clvm.name, temp_out, [chia_puzzles_root, "."])
        output = pathlib.Path(temp_out).read_text()
        puzzle = Program.fromhex(output)
        assert puzzle.get_tree_hash() == STD_CLAWBACK_MOD.get_tree_hash()
