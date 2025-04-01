from typing import Optional
from point import Point
from pawns import *


class Check:
    def __init__(self, board) -> None:
        self.board = board

    def is_check(self, check_whose_turn) -> bool:
        if check_whose_turn() == Color.WHITE:
            return self.can_make_a_check(self.board.black_pawns)
        if check_whose_turn() == Color.BLACK:
            return self.can_make_a_check(self.board.white_pawns)
        return False
    
    def is_checkmate(self, pawns_list: list[tuple], is_simulated_action_valid, check_whose_turn) -> bool:
        for _, position in pawns_list:
            pawn = self.board.board[position.y][position.x]
            for y in range(self.board.height):
                for x in range(self.board.width):
                    new_pos = Point(x, y)
                    if isinstance(pawn, Knight):
                        if (pawn.can_move(position, new_pos) or (pawn.can_capture(position, new_pos))):
                            if is_simulated_action_valid(pawn, position, new_pos, self.is_check, check_whose_turn):
                                return True
                    elif (pawn.can_move(position, new_pos) or (pawn.can_capture(position, new_pos))):
                        if is_simulated_action_valid(pawn, position, new_pos, self.is_check, check_whose_turn):
                            return True
        return False

    def can_make_a_check(self, pawns_list: list[tuple]) -> bool:
        for _, position in pawns_list:
            pawn = self.board.board[position.y][position.x]
            king_pos = self.get_king_position(pawn)
            if king_pos is not None:
                if isinstance(pawn, Knight):
                    if pawn.can_capture(position, king_pos):
                        return True
                elif pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
                    return True
        return False

    def get_king_position(self, opponent: Pawn) -> Optional[Point]:
        for y, row in enumerate(self.board.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color != opponent.color:
                    return Point(x, y)
        return None
