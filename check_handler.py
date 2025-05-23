from typing import Optional

from point import Point
from pawns import *
import utils

logger = utils.get_logger(__name__)

class CheckHandler:
    def __init__(self, board, move_handler, capture_handler) -> None:
        self.board = board
        self.move_handler = move_handler
        self.capture_handler = capture_handler

    def get_checked_king_color(self, turn) -> Optional[Color]:
        current_turn = turn
        logger.debug(f"checkhandler.ischeck() = Current turn {current_turn}")
        if current_turn == Color.BLACK:
            if self.can_make_a_check(self.board.white_pawns, Color.WHITE):
                return Color.BLACK
            elif self.can_make_a_check(self.board.black_pawns, Color.BLACK):
                return Color.WHITE
        if current_turn == Color.WHITE:
            if self.can_make_a_check(self.board.black_pawns, Color.BLACK):
                return Color.WHITE
            elif self.can_make_a_check(self.board.white_pawns, Color.WHITE):
                return Color.BLACK
        return None
    
    def can_make_a_check(self, pawns_list: list[tuple], pawns_color: Color) -> bool:
        for pawn_type, position in pawns_list:
            pawn = self.board.get_piece(position)
            if isinstance(pawn, Pawn) and pawn.color == pawns_color:
                king_pos = self.board.get_king_position(pawn.color)
                if king_pos and self.can_capture_king(pawn, position, king_pos):
                    logger.warn(f"Pawn: {pawn} at: {position} is attacking the King at: {king_pos}")
                    return True
        return False
    
    def is_checkmate(self, pawns_list: list[tuple], turn, check_handler) -> bool:
        unique_positions = list(position for _, position in pawns_list)
        for position in unique_positions:
            pawn = self.board.get_piece(position)
            logger.debug(f"{pawn} at the {position} is checking if can escape check")
            if self.can_escape_check(pawn, position, turn, check_handler):
                return False
        return True
    
    def can_move_or_capture(self, pawn, position, new_pos, turn, check_handler) -> bool:
        if self.move_handler.is_move_valid(pawn, position, new_pos, check_handler, turn) or \
        self.capture_handler.is_capture_valid(pawn, position, new_pos, check_handler, turn):
            return True
        return False 

    def can_escape_check(self, pawn, position: Point, turn, check_handler) -> bool:
        for y in range(self.board.height):
            for x in range(self.board.width):
                new_pos = Point(x, y)
                if new_pos != position:
                    logger.info(f"Checking {pawn}'s escape move from {position} to {new_pos}")
                    if self.can_move_or_capture(pawn, position, new_pos, turn, check_handler):
                        return True
        return False

    def can_capture_king(self, pawn, position: Point, king_pos: Point) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_capture(position, king_pos):
                return True
        if pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
            return True
        return False
