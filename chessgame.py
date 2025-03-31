from typing import Optional

from board import Board
from point import Point
from pawns import *
from move import Move
from check import Check


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        self.move_handler = Move(self.board)
        self.check_handler = Check(self.board)

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        return self.move_handler.move_piece(current_pos, new_pos, self.check_whose_turn, self.is_check, self.switch_turn)
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def is_check(self, check_whose_turn) -> bool:
        return self.check_handler.is_check(self.check_whose_turn)
    
    #Move checking if is checkmate to game and if is checkmate raise na exception in main.py and decdide what to do
    def is_checkmate(self, pawns_list: list[tuple]) -> bool:
        if self.check_whose_turn() == Color.WHITE:
            return self.check_handler.is_checkmate(self.board.black_pawns, self.move_handler.is_simulated_action_valid, self.check_whose_turn)
        return self.check_handler.is_checkmate(self.board.white_pawns, self.move_handler.is_simulated_action_valid, self.check_whose_turn)
        
    def switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
