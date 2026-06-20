import unittest
from algorithms.nqueens import solve_nqueens
from algorithms.knights import solve_knights
from algorithms.bishops import solve_bishops
from algorithms.rooks import solve_rooks
from parser.txt_parser import parse_dataset_text, DatasetParseError


class TestSolvers(unittest.TestCase):
    def test_nqueens_4x4(self):
        # 4-Queens on a 4x4 board has exactly 2 solutions
        result = solve_nqueens(board_rows=4, board_cols=4, piece_count=4, max_solutions=None, record_steps=True)
        self.assertEqual(len(result.solutions), 2)
        # Verify the solutions are correct
        for sol in result.solutions:
            self.assertEqual(len(sol), 4)

    def test_rooks_4x4(self):
        # 4-Rooks on a 4x4 board has exactly 4! = 24 solutions
        result = solve_rooks(board_rows=4, board_cols=4, piece_count=4, max_solutions=None, record_steps=True)
        self.assertEqual(len(result.solutions), 24)

    def test_bishops_2x2(self):
        # 2-Bishops on a 2x2 board has exactly 4 solutions
        result = solve_bishops(board_rows=2, board_cols=2, piece_count=2, max_solutions=None, record_steps=True)
        self.assertEqual(len(result.solutions), 4)

    def test_knights_2x2(self):
        # 2-Knights on a 2x2 board has 6 solutions (since they cannot attack each other on a 2x2 board)
        result = solve_knights(board_rows=2, board_cols=2, piece_count=2, max_solutions=None, record_steps=True)
        self.assertEqual(len(result.solutions), 6)


class TestParser(unittest.TestCase):
    def test_valid_parsing(self):
        text = """
        BOARD 8 8
        PIECE QUEEN
        COUNT 8
        CONSTRAINT NO_ATTACK
        """
        dataset = parse_dataset_text(text)
        self.assertEqual(dataset.board_rows, 8)
        self.assertEqual(dataset.board_cols, 8)
        self.assertEqual(dataset.piece_type, "QUEEN")
        self.assertEqual(dataset.piece_count, 8)
        self.assertEqual(dataset.constraint, "NO_ATTACK")

    def test_invalid_parsing_missing_directive(self):
        text = """
        BOARD 8 8
        PIECE QUEEN
        # Missing COUNT and CONSTRAINT
        """
        with self.assertRaises(DatasetParseError):
            parse_dataset_text(text)


if __name__ == "__main__":
    unittest.main()
