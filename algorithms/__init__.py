from __future__ import annotations
from typing import Optional, List, Tuple

from algorithms.base_solver import BaseSolver, SolverResult, SolverStats
from algorithms.nqueens import NQueensSolver, solve_nqueens
from algorithms.knights import KnightSolver, solve_knights
from algorithms.bishops import BishopSolver, solve_bishops
from algorithms.rooks import RookSolver, solve_rooks

def solve_puzzle(
    piece_type: str,
    board_rows: int,
    board_cols: int,
    piece_count: int,
    max_solutions: Optional[int] = None,
    record_steps: bool = True,
):
    p_type = piece_type.upper()
    if p_type == "QUEEN":
        res = solve_nqueens(board_rows, board_cols, piece_count, max_solutions, record_steps)
    elif p_type == "KNIGHT":
        res = solve_knights(board_rows, board_cols, piece_count, max_solutions, record_steps)
    elif p_type == "BISHOP":
        res = solve_bishops(board_rows, board_cols, piece_count, max_solutions, record_steps)
    elif p_type == "ROOK":
        res = solve_rooks(board_rows, board_cols, piece_count, max_solutions, record_steps)
    else:
        raise ValueError(f"Unsupported piece type: {piece_type}")

    class RealStats:
        def __init__(self, nodes_explored: int, backtracks: int, solutions_found: int, execution_time_seconds: float):
            self.nodes_explored = nodes_explored
            self.backtracks = backtracks
            self.solutions_found = solutions_found
            self.execution_time_seconds = execution_time_seconds

    class RealResultWrapper:
        def __init__(self, solutions: List[List[Tuple[int, int]]], steps: List[str], stats: RealStats, piece_type: str, board_rows: int, board_cols: int):
            self.solutions = solutions
            self.steps = steps
            self.stats = stats
            self.piece_type = piece_type
            self.board_rows = board_rows
            self.board_cols = board_cols

    wrapped_stats = RealStats(
        nodes_explored=res.stats.nodes_explored,
        backtracks=res.stats.backtracks,
        solutions_found=len(res.solutions),
        execution_time_seconds=res.execution_time
    )

    return RealResultWrapper(
        solutions=res.solutions,
        steps=res.steps,
        stats=wrapped_stats,
        piece_type=piece_type,
        board_rows=board_rows,
        board_cols=board_cols
    )

