from typing import Optional
import logging
logger = logging.getLogger(__name__)

from point import Point
from pawns import *
from board import EMPTY_SQUARE


class MoveHandler:
    def __init__(self, board) -> None:
        self.board = board

    def move_piece(self, current_pos: Point, new_pos: Point, check_whose_turn, is_check) -> bool:
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
        if pawn.can_move(current_pos, new_pos):
            if self.board.get_piece(new_pos) == EMPTY_SQUARE:
                if self.is_piece_move_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                    return True
                else:
                    logger.info(f"Invalid piece move")
            else:
                logger.info(f"Target pos is not empty")
        else:
            logger.info(f"{pawn} cannot move")
        return False
    
    def is_piece_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        if isinstance(pawn, Knight):
            if self.board.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                return True
            else:
                logger.info(f"Simulated action is not valid for Knight")
                return False
        elif isinstance(pawn, Pawn) and self.board.is_path_clear(current_pos, new_pos):
            if self.board.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                return True
            else:
                logger.info(f"Sumulated action not valid for the rest of pawns and path is clear")
        else:
            logger.info(f"Path is not clear")
        