from point import Point
from pawns import *
from board import EMPTY_SQUARE
import utils

logger = utils.get_logger(__name__)


class MoveHandler:
    def __init__(self, board) -> None:
        self.board = board

    def move_piece(self, current_pos: Point, new_pos: Point, turn, check_handler) -> bool:
        pawn = self.board.get_piece(current_pos)
        logger.debug(f"Pawn: {pawn} at {current_pos} is moving to {new_pos}")
        if isinstance(pawn, Pawn):
            if pawn.color != turn:
                logger.debug("It's not your turn!")
                return False
            elif self.is_move_valid(pawn, current_pos, new_pos, check_handler, turn):
                self.board.execute_move(pawn, current_pos, new_pos)
                logger.debug("Move is valid")
                return True
        return False
        
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_handler, turn) -> bool:
        if pawn.can_move(current_pos, new_pos):
            if self.board.get_piece(new_pos) == EMPTY_SQUARE:
                if self.__is_piece_move_valid(pawn, current_pos, new_pos, check_handler, turn):
                    return True
                else:
                    logger.debug(f"Invalid piece move")
            else:
                logger.debug(f"Target pos is not empty")
        else:
            logger.debug(f"{pawn} cannot move")
        return False
    
    def __is_piece_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_handler, turn) -> bool:
        if isinstance(pawn, Knight):
            if self.board.is_simulated_action_valid(pawn, current_pos, new_pos, check_handler, turn):
                return True
            else:
                logger.debug(f"Simulated action is not valid for Knight")
                return False
        elif isinstance(pawn, Pawn) and self.board.is_path_clear(current_pos, new_pos):
            logger.debug(f"{pawn} has path clear")
            if self.board.is_simulated_action_valid(pawn, current_pos, new_pos, check_handler, turn):
                logger.debug(f"Simulated action is valid for {pawn}")
                return True
            else:
                logger.debug(f"Simulated action not valid for the rest of pawns")
        else:
            logger.debug(f"Path is not clear")
        