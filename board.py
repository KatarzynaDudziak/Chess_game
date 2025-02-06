from point import Point
from pawns import Pawn

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [["|__| " for _ in range(width)] for _ in range(height)]
        self.white_pawns: list[Pawn] = []
        self.black_pawns: list[Pawn] = []
        self.movements_history: list[tuple[Point, Point]] = []
        self.available_pawns: list[tuple[Point, Pawn]] = []
        self.captured_pawns: list[Pawn] = []
        self.available_moves: list[tuple[tuple[Point, Pawn], Point]] = []
        self.available_captures: list[tuple[tuple[Point, Pawn], Point]] = []        

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += "".join(row) + "\n"
        return board_str

    def set_pawns(self, pawns, position: Point):
        pass

    def move_pawn(self, current_pos: Point, new_pos: Point):
        pass

    def capture_pawn(self, current_pos: Point, new_pos: Point):
        pass

    def is_move_valid(self, current_pos: Point, new_pos: Point):
        pass

    def is_place_occupied(self, position: Point):
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
print(board)
