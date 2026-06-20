from __future__ import annotations
from typing import List, Tuple, Optional

from algorithms.base_solver import BaseSolver, SolverResult
from algorithms.constraints import PieceType

Position = Tuple[int, int]


class RookSolver(BaseSolver):
    """
    Backtracking solver for the Rook Placement puzzle.
    Since rooks cannot attack each other along the same row/col,
    we can use the default row-by-row solver (one rook per row).
    """
    piece_type = PieceType.ROOK


def solve_rooks(
    board_rows: int,
    board_cols: int,
    piece_count: int,
    max_solutions: Optional[int] = None,
    record_steps: bool = True,
) -> SolverResult:
    """Convenience entry point to solve a Rook Placement puzzle."""
    solver = RookSolver(
        board_rows=board_rows,
        board_cols=board_cols,
        piece_count=piece_count,
        max_solutions=max_solutions,
        record_steps=record_steps,
    )
    return solver.solve()
