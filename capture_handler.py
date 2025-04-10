from typing import Optional
import logging
logger = logging.getLogger(__name__)

from point import Point
from pawns import Pawn, Knight, Color


class CaptureHandler:
    def __init__(self, board) -> None:
        self.board = board

    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        target_pawn = self.get_opponent(pawn, new_pos)
        if target_pawn:
            if pawn.can_capture(current_pos, new_pos):
                if isinstance(pawn, Knight):
                    return self.board.is_simulated_action_valid(pawn, current_pos,
                                                                 new_pos, is_check, check_whose_turn)
                elif self.board.is_path_clear(current_pos, new_pos):
                    return self.board.is_simulated_action_valid(pawn, current_pos,
                                                                 new_pos, is_check, check_whose_turn)
        return False
        
    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_whose_turn) -> None:
        opponent = self.get_opponent(pawn, new_pos)
        if opponent is None:
            return
        target_pawn, target_pawn_pos = opponent
        # self.board.captured_pawns.append(target_pawn)
        logger.info(f"Capture piece at {target_pawn_pos}")
        self.board.update_board_after_capture(pawn, target_pawn_pos,
                                         target_pawn, current_pos, new_pos, check_whose_turn)
   
    def get_opponent(self, pawn: Pawn, new_pos: Point) -> Optional[tuple[Pawn, Point]]:
        if not self.board.is_out_of_bounds(new_pos):
            opponent = self.board.get_piece(new_pos)
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        return None
