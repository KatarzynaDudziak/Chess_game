from typing import Optional
import logging
logger = logging.getLogger(__name__)

from point import Point
from pawns import *
from board import EMPTY_SQUARE


class MoveHandler:
    def __init__(self, board) -> None:
        self.board = board

    def move_piece(self, current_pos: Point, new_pos: Point, check_whose_turn, is_check, switch_turn) -> bool:
        logger.info(f"Moving piece from {current_pos} to {new_pos}")
        pawn = self.board.get_piece_at_the_position(current_pos)
        if isinstance(pawn, Pawn):
            if pawn.color != check_whose_turn():
                logger.info("It's not your turn!")
                return False
            elif self.is_move_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                self.board.execute_move(pawn, current_pos, new_pos)
                logger.info("Move is valid")
                return True
        return False
        
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        if pawn.can_move(current_pos, new_pos) and self.board.board[new_pos.y][new_pos.x] == EMPTY_SQUARE:
            return self.is_piece_move_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
        logger.info("Move is not valid")
        return False
    
    def is_piece_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        if isinstance(pawn, Knight):
            return self.board.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
        elif isinstance(pawn, Pawn) and self.board.is_path_clear(current_pos, new_pos):
            return self.board.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
