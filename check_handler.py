from typing import Optional

from point import Point
from pawns import *


class CheckHandler:
    def __init__(self, board) -> None:
        self.board = board

    def is_check(self, check_whose_turn) -> Optional[Color]:
        current_turn = check_whose_turn()
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
                king_pos = self.board.get_king_position(pawn)
                if king_pos and self.can_capture_king(pawn, position, king_pos):
                    logger.warn(f"Pawn: {pawn} at: {position} is attacking the King at: {king_pos}")
                    return True
        return False
    
    def is_checkmate(self, pawns_list: list[tuple], check_whose_turn) -> bool:
        for _, position in pawns_list:
            pawn = self.board.get_piece(position)
            if self.can_escape_check(pawn, position, check_whose_turn):
                return False
        return True
    
    def is_action_valid(self, pawn, position, new_pos, check_whose_turn):
        if self.board.is_simulated_action_valid(pawn, position, new_pos, self.is_check, check_whose_turn):
            logger.info(f"The {pawn} can move to {new_pos} and can escape check")
            return True
        return False

    def can_move_or_capture(self, pawn, position, new_pos, check_whose_turn):
        if isinstance(pawn, Knight):
            if pawn.can_move(position, new_pos) or pawn.can_capture(position, new_pos):
                if self.is_action_valid(pawn, position, new_pos, check_whose_turn):
                    return True
        elif pawn.can_move(position, new_pos) and self.board.is_path_clear(position, new_pos) or \
                              pawn.can_capture(position, new_pos) and self.board.is_path_clear(position, new_pos):
            if self.is_action_valid(pawn, position, new_pos, check_whose_turn):
                return True
        return False

    def can_escape_check(self, pawn, position: Point, check_whose_turn) -> bool:
        for y in range(self.board.height):
            for x in range(self.board.width):
                new_pos = Point(x, y)
                if new_pos != position:
                    logger.info(f"Checking move from {position} to {new_pos}")
                    if self.can_move_or_capture(pawn, position, new_pos, check_whose_turn):
                        return True
        return False

    def can_capture_king(self, pawn, position: Point, king_pos: Point) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_capture(position, king_pos):
                return True
        if pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
            return True
        return False
