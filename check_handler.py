from typing import Optional

from point import Point
from pawns import *


class CheckHandler:
    def __init__(self, board) -> None:
        self.board = board

    def is_check(self, check_whose_turn) -> Optional[Color]:
        logger.info(f"checkhandler.ischeck() = Current turn {check_whose_turn()}")
        if check_whose_turn() == Color.BLACK:
            if self.can_make_a_check(self.board.white_pawns):
                return Color.BLACK
            elif self.can_make_a_check(self.board.black_pawns):
                return Color.WHITE
        if check_whose_turn() == Color.WHITE:
            if self.can_make_a_check(self.board.black_pawns):
                return Color.WHITE
            elif self.can_make_a_check(self.board.white_pawns):
                return Color.BLACK
        return None
    
    def can_make_a_check(self, pawns_list: list[tuple]) -> bool:
        for pawn_type, position in pawns_list:
            pawn = self.board.get_piece(position)
            if isinstance(pawn, Pawn):
                king_pos = self.board.get_king_position(pawn)
                if king_pos and self.can_capture_king(pawn, position, king_pos):
                    return True
        return False
    
    def is_checkmate(self, pawns_list: list[tuple], check_whose_turn) -> bool:
        for _, position in pawns_list:
            pawn = self.board.get_piece(position)
            if self.can_escape_check(pawn, position, check_whose_turn):
                return False
        return False #todo

    def can_escape_check(self, pawn, position: Point, check_whose_turn) -> bool:
        for y in range(self.board.height):
            for x in range(self.board.width):
                new_pos = Point(x, y)
                if pawn.can_move(position, new_pos) or pawn.can_capture(position, new_pos):
                    if self.board.is_simulated_action_valid(pawn, position, new_pos, self.is_check, check_whose_turn):
                        return True
        return False

    def can_capture_king(self, pawn, position: Point, king_pos: Point) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_capture(position, king_pos):
                return True
        if pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
            return True
        return False
