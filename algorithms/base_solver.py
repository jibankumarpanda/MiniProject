from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import time

Position = Tuple[int, int]


@dataclass
class SolverStats:
    nodes_explored: int = 0
    backtracks: int = 0


@dataclass
class SolverResult:
    solutions: List[List[Position]]
    steps: List[str]
    stats: SolverStats
    execution_time: float


class BaseSolver:
    """
    Base backtracking solver class for Chessboard Placement Puzzles.
    """
    piece_type = None

    def __init__(
        self,
        board_rows: int,
        board_cols: int,
        piece_count: int,
        max_solutions: Optional[int] = None,
        record_steps: bool = True,
    ):
        self.board_rows = board_rows
        self.board_cols = board_cols
        self.piece_count = piece_count
        self.max_solutions = max_solutions
        self.record_steps = record_steps

        self.solutions: List[List[Position]] = []
        self.steps: List[str] = []
        self.stats = SolverStats()

    def candidate_positions(self, row: int) -> List[Position]:
        """
        Get candidate positions for the current row/step.
        Default implementation is one piece per row.
        """
        if row < self.board_rows:
            return [(row, col) for col in range(self.board_cols)]
        return []

    def bound(self, placed_positions: List[Position], row: int) -> bool:
        """
        Branch & Bound pruning logic. Returns True if this branch should be pruned.
        """
        remaining_pieces_needed = self.piece_count - len(placed_positions)
        remaining_rows_available = self.board_rows - row
        return remaining_pieces_needed > remaining_rows_available

    def _log_step(self, message: str) -> None:
        """Log a step in the solver's execution if step recording is enabled."""
        if self.record_steps:
            self.steps.append(message)

    def _format_positions(self, placed: List[Position]) -> str:
        """Format a list of coordinates into a readable string."""
        return str(placed)

    def _backtrack(self, row: int, placed: List[Position]) -> bool:
        """
        Backtracking core logic. Can be overridden by subclasses (e.g. Knights, Bishops).
        Default implementation assumes one piece per row.
        """
        self.stats.nodes_explored += 1

        if len(placed) == self.piece_count:
            self.solutions.append(list(placed))
            self._log_step(f"Solution found: {self._format_positions(placed)}")
            if self.max_solutions is not None and len(self.solutions) >= self.max_solutions:
                return True
            return False

        if row >= self.board_rows:
            return False

        if self.bound(placed, row):
            return False

        from algorithms.constraints import is_valid_placement

        # Branch 1: Try placing a piece in each candidate position in the current row
        candidates = self.candidate_positions(row)
        for pos in candidates:
            if is_valid_placement(pos, placed, self.piece_type, self.board_rows, self.board_cols):
                placed.append(pos)
                self._log_step(f"Place {self.piece_type.value.capitalize()} at {pos}")
                if self._backtrack(row + 1, placed):
                    return True
                placed.pop()
                self.stats.backtracks += 1
                self._log_step("Backtrack")
            else:
                self._log_step(f"Conflict detected at {pos}")

        # Branch 2: skip the current row (allowed if remaining rows are sufficient)
        if len(placed) + (self.board_rows - (row + 1)) >= self.piece_count:
            if self._backtrack(row + 1, placed):
                return True

        return False

    def solve(self) -> SolverResult:
        """
        Solves the puzzle and returns a SolverResult.
        """
        start_time = time.perf_counter()
        self.solutions = []
        self.steps = []
        self.stats = SolverStats()

        self._backtrack(0, [])

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return SolverResult(
            solutions=self.solutions,
            steps=self.steps,
            stats=self.stats,
            execution_time=execution_time,
        )
