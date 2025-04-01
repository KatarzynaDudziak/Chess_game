from board import Board
from point import Point
from pawns import *
from move_handler import MoveHandler
from check_handler import CheckHandler
from capture_handler import CaptureHandler
from game_over_exception import GameOverException


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        self.move_handler = MoveHandler(self.board)
        self.check_handler = CheckHandler(self.board)
        self.capture_handler = CaptureHandler(self.board)

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        if not self.move_handler.move_piece(current_pos, new_pos, self.check_whose_turn, self.is_check, self.switch_turn):
            if self.capture_handler.is_capture_valid(self.board.get_piece_at_the_position(current_pos),
                                                        current_pos, new_pos, self.is_check,
                                                        self.check_whose_turn):
                self.capture_handler.capture(self.board.get_piece_at_the_position(current_pos),
                                                current_pos, new_pos, self.check_whose_turn)
            elif self.is_check(self.check_whose_turn):
                self.switch_turn()
        return True   
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def is_check(self, check_whose_turn) -> bool:
        if not self.check_handler.is_check(self.check_whose_turn):
            return False
        if self.is_checkmate(self.board.white_pawns if check_whose_turn() == Color.WHITE else self.board.black_pawns):
            raise GameOverException("Checkmate! Game over!")
        return True
        
    def is_checkmate(self, pawns_list: list[tuple]) -> bool:
        if self.check_whose_turn() == Color.WHITE:
            return self.check_handler.is_checkmate(self.board.black_pawns, self.check_whose_turn)
        return self.check_handler.is_checkmate(self.board.white_pawns, self.check_whose_turn)
        
    def switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
