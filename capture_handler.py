from typing import Optional
import logging
logger = logging.getLogger(__name__)

from point import Point
from pawns import Pawn, Knight, Color


class CaptureHandler:
    def __init__(self, board) -> None:
        self.board = board

    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn, is_simulated_action_valid) -> bool:
        target_pawn = self.get_opponent(pawn, new_pos)
        if target_pawn:
            pos = target_pawn[1]
            if pawn.can_capture(current_pos, new_pos):
                if isinstance(pawn, Knight):
                    return is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
                elif self.board.is_path_clear(current_pos, new_pos):
                    return is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
        return False
        
    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_whose_turn) -> None:
        opponent = self.get_opponent(pawn, new_pos)
        if opponent is None:
            return
        target_pawn, target_pawn_pos = opponent
        self.board.captured_pawns.append(target_pawn)
        logger.info(f"Capture piece at {target_pawn_pos}")
        self.update_board_after_capture(pawn, target_pawn_pos, target_pawn, current_pos, new_pos, check_whose_turn)

    def update_board_after_capture(self, pawn: Pawn, target_pawn_pos, target_pawn, current_pos, new_pos, check_whose_turn) -> None:
        if check_whose_turn() == Color.WHITE:
            self.board.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif check_whose_turn() == Color.BLACK:
            self.board.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.board.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.board.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.board.movements_history.append((current_pos, target_pawn_pos))
        self.board.set_empty_position(current_pos)

    def get_opponent(self, pawn: Pawn, new_pos: Point) -> Optional[tuple[Pawn, Point]]:
        if not self.board.is_out_of_bounds(new_pos):
            opponent = self.board.board[new_pos.y][new_pos.x]
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        return None
