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
            if self.__can_make_a_check(self.board.get_white_pawns(), Color.WHITE):
                return Color.BLACK
            elif self.__can_make_a_check(self.board.get_black_pawns(), Color.BLACK):
                return Color.WHITE
        if current_turn == Color.WHITE:
            if self.__can_make_a_check(self.board.get_black_pawns(), Color.BLACK):
                return Color.WHITE
            elif self.__can_make_a_check(self.board.get_white_pawns(), Color.WHITE):
                return Color.BLACK
        return None
    
    def __can_make_a_check(self, pawns_list: list[tuple], pawns_color: Color) -> bool:
        for pawn_type, position in pawns_list:
            pawn = self.board.get_piece(position)
            if isinstance(pawn, Pawn) and pawn.color == pawns_color:
                king_pos = self.board.get_king_position(pawn.color)
                if king_pos and self.__can_capture_king(pawn, position, king_pos):
                    logger.warn(f"Pawn: {pawn} at: {position} is attacking the King at: {king_pos}")
                    return True
        return False
    
    def is_checkmate(self, pawns_list: list[tuple], turn, check_handler) -> bool:
        for _, position in pawns_list:
            pawn = self.board.get_piece(position)
            logger.debug(f"{pawn} at the {position} is checking if can escape check")
            if self.__can_escape_check(pawn, position, turn, check_handler):
                return False
        return True
    
    def __can_move_or_capture(self, pawn, position, new_pos, turn, check_handler) -> bool:
        if self.move_handler.is_move_valid(pawn, position, new_pos, check_handler, turn) or \
        self.capture_handler.is_capture_valid(pawn, position, new_pos, check_handler, turn):
            return True
        return False 

    def __can_escape_check(self, pawn, position: Point, turn, check_handler) -> bool:
        for y in range(self.board.height):
            for x in range(self.board.width):
                new_pos = Point(x, y)
                if new_pos != position:
                    logger.info(f"Checking {pawn}'s escape move from {position} to {new_pos}")
                    if self.__can_move_or_capture(pawn, position, new_pos, turn, check_handler):
                        return True
        return False

    def __can_capture_king(self, pawn, position: Point, king_pos: Point) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_capture(position, king_pos):
                return True
        if pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
            return True
        return False

    def will_the_move_escape_the_check(self, pawn: Pawn, attacked_king_color: Color, current_pos: Point, new_pos: Point, check_handler, turn) -> bool:
        if attacked_king_color == self.get_checked_king_color(turn):
            original_target = self.board[new_pos.y][new_pos.x]
            self.board.make_move(pawn, new_pos, current_pos)
            try:
                attacked_king_color = self.get_checked_king_color(turn)
                if attacked_king_color == None:
                    logger.info("The move can escape the check")
                    return True
                elif attacked_king_color != turn:
                    logger.info("The move can escape the check and will cause the check")
                    return True
                else:
                    logger.info("The move won't escape the check")
                    return False
            finally:
                self.board.undo_move(pawn, current_pos, new_pos, original_target)
        return False
