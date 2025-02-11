from typing import List

from point import Point
from pawns import Pawn, Rook, Bishop, Knight, Queen, King


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [["|__|" for _ in range(width)] for _ in range(height)]
        self.white_pawns = [
            (Rook("white"), Point(0,0)), (Knight("white"), Point(1,0)), (Bishop("white"), Point(2,0)), (Queen("white"), Point(3,0)),
            (King("white"), Point(4,0)), (Bishop("white"), Point(5,0)), (Knight("white"), Point(6,0)), (Rook("white"), Point(7,0)),
            (Pawn("white"), Point(0,1)), (Pawn("white"), Point(1,1)), (Pawn("white"), Point(2,1)), (Pawn("white"), Point(3,1)),
            (Pawn("white"), Point(4,1)), (Pawn("white"), Point(5,1)), (Pawn("white"), Point(6,1)), (Pawn("white"), Point(7,1))
            ]
            
        self.black_pawns = [
            (Rook("black"), Point(0,7)), (Knight("black"), Point(1,7)), (Bishop("black"), Point(2,7)), (Queen("black"), Point(4,7)),
            (King("black"), Point(3,7)), (Bishop("black"), Point(5,7)), (Knight("black"), Point(6,7)), (Rook("black"), Point(7,7)),
            (Pawn("black"), Point(0,6)), (Pawn("black"), Point(1,6)), (Pawn("black"), Point(2,6)), (Pawn("black"), Point(3,6)),
            (Pawn("black"), Point(4,6)), (Pawn("black"), Point(5,6)), (Pawn("black"), Point(6,6)), (Pawn("black"), Point(7,6))
            ]
        
        self.movements_history: list[tuple[Point, Point]] = []
        self.captured_pawns: list[Pawn] = []
        self.available_moves: list[tuple[tuple[Point, Pawn], Point]] = []
        self.available_captures: list[tuple[tuple[Point, Pawn], Point]] = []        

    def __str__(self):
        board_str = ""
        for row in reversed(self.board):
            board_str += "".join([f"|{pawn.__str__()}|" if isinstance(pawn, Pawn) else "|__|" for pawn in row]) + "\n"
        return board_str

    def set_pawns(self, pawns: List[tuple]):
        for pawn, position in pawns:
            self.set_pawn_at_the_position(pawn, position)

    def set_pawn_at_the_position(self, pawn: Pawn, position: Point):
        self.board[position.y][position.x] = pawn

    def set_white_pawns(self):
        self.set_pawns(self.white_pawns)

    def set_black_pawns(self):
        self.set_pawns(self.black_pawns)
    
    def set_empty_position(self, position: Point):
        self.board[position.y][position.x] = " "

    def move_pawn(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if self.board[current_pos.y][current_pos.x] == pawn and self.is_move_valid(pawn, current_pos, new_pos):
            self.set_empty_position(current_pos)
            self.set_pawn_at_the_position(pawn, new_pos)
            self.movements_history.append((current_pos, new_pos))

    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if pawn.can_move(current_pos, new_pos):
            if self.board[new_pos.y][new_pos.x] == "|__|":
                return True
        return False
    
    def capture_pawn(self, current_pos: Point, new_pos: Point):
        pass

    def is_out_of_bounds(self, position: Point):
        pass

    def check_whose_turn(self):
        pass

    def is_check(self):
        pass

    def is_checkmate(self):
        pass

    def get_movements_history(self):
        pass

    def get_available_pawns(self):
        pass

    def get_available_moves(self):
        pass

    def get_available_captures(self):
        pass


board = Board(8, 8)
board.set_white_pawns()
board.set_black_pawns()
board.move_pawn(Pawn("white"), Point(0, 1), Point(0, 2))
board.move_pawn(Pawn("black"), Point(0, 6), Point(0, 4))
print(board)
