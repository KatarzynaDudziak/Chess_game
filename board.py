from typing import List
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from point import Point
from pawns import *

EMPTY_SQUARE = " "


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[EMPTY_SQUARE for _ in range(width)] for _ in range(height)]
        self.white_pawns = [
            (WhiteRook, Point(0,0)), (WhiteKnight, Point(1,0)), (WhiteBishop, Point(2,0)), (WhiteQueen, Point(3,0)),
            (WhiteKing, Point(4,0)), (WhiteBishop, Point(5,0)), (WhiteKnight, Point(6,0)), (WhiteRook, Point(7,0)),
            (WhitePawn, Point(0,1)), (WhitePawn, Point(1,1)), (WhitePawn, Point(2,1)), (WhitePawn, Point(3,1)),
            (WhitePawn, Point(4,1)), (WhitePawn, Point(5,1)), (WhitePawn, Point(6,1)), (WhitePawn, Point(7,1))
            ]
            
        self.black_pawns = [
            (BlackRook, Point(0,7)), (BlackKnight, Point(1,7)), (BlackBishop, Point(2,7)), (BlackQueen, Point(4,7)),
            (BlackKing, Point(3,7)), (BlackBishop, Point(5,7)), (BlackKnight, Point(6,7)), (BlackRook, Point(7,7)),
            (BlackPawn, Point(0,6)), (BlackPawn, Point(1,6)), (BlackPawn, Point(2,6)), (BlackPawn, Point(3,6)),
            (BlackPawn, Point(4,6)), (BlackPawn, Point(5,6)), (BlackPawn, Point(6,6)), (BlackPawn, Point(7,6))
            ]
        
        self.movements_history: list[tuple[Point, Point]] = []
        self.captured_pawns: list[Pawn] = []
        self.available_moves: list[tuple[tuple[Point, Pawn], Point]] = []
        self.available_captures: list[tuple[tuple[Point, Pawn], Point]] = []        
    
    def __str__(self):
        board_str = ""
        for row in reversed(self.board):
            board_str += "".join([f"|{pawn.__str__()}|" if isinstance(pawn, Pawn) else "|__ |" for pawn in row]) + "\n"
        return board_str

    def move_piece(self, current_pos: Point, new_pos: Point):
        pawn = self.board[current_pos.y][current_pos.x]
        if isinstance(pawn, Pawn):
            if pawn.color != self.check_whose_turn():
                logger.info("It's not your turn!")
                return
            if self.is_capture_valid(pawn, current_pos, new_pos):
                self.capture(pawn, current_pos, new_pos)
            elif self.is_move_valid(pawn, current_pos, new_pos):
                self.execute_move(pawn, current_pos, new_pos) 
                if self.is_check():
                    logger.info("Check!")
                    self.switch_turn()
        else:
            logger.info("Invalid move or pawn type")

    def execute_move(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_pawn_at_the_position(pawn, new_pos)
        self.set_empty_position(current_pos)
        self.movements_history.append((current_pos, new_pos))
            
    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        target_pawn = self.get_opponent(pawn, new_pos)
        if target_pawn:
            target_pawn, pos = target_pawn
            if pawn.can_capture(current_pos, new_pos) and self.simulate_action(pawn, current_pos, new_pos) != False:
                if self.is_path_clear(current_pos, new_pos):
                    return True
        return False
    
    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        print(self.get_opponent(pawn, new_pos))
        target_pawn, target_pawn_pos = self.get_opponent(pawn, new_pos)
        self.captured_pawns.append(target_pawn)
        if self.check_whose_turn() == Color.WHITE:
            self.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif self.check_whose_turn() == Color.BLACK:
            self.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.movements_history.append((current_pos, target_pawn_pos))
        self.set_empty_position(current_pos)

    def get_opponent(self, pawn: Pawn, new_pos: Point):
        if not self.is_out_of_bounds(new_pos):
            opponent = self.board[new_pos.y][new_pos.x]
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        return None
    
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if isinstance(pawn, Knight):
            if pawn.can_move(current_pos, new_pos):
                if isinstance(self.board[new_pos.y][new_pos.x], str):
                    return self.simulate_action(pawn, current_pos, new_pos)
        elif pawn.can_move(current_pos, new_pos) and self.is_path_clear(current_pos, new_pos):
            if isinstance(self.board[new_pos.y][new_pos.x], str):
                return self.simulate_action(pawn, current_pos, new_pos)
        logger.info("Move is not valid")
        return False
    
    def simulate_action(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        original_target = self.board[new_pos.y][new_pos.x]
        self.set_pawn_at_the_position(pawn, new_pos)
        self.set_empty_position(current_pos)
        if not self.is_check():
            self.set_pawn_at_the_position(pawn, current_pos)
            self.set_pawn_at_the_position(original_target, new_pos)
            return True
        else:
            self.set_pawn_at_the_position(pawn, current_pos)
            self.set_pawn_at_the_position(original_target, new_pos)
        return False

    def add_pawn_to_the_list(self, pawn: Pawn, current_pos: Point, position: Point):
        if pawn.color == Color.WHITE:
            self.white_pawns.remove((type(pawn), current_pos))
            self.white_pawns.append((type(pawn), position))
        elif pawn.color == Color.BLACK:
            self.black_pawns.remove((type(pawn), current_pos))
            self.black_pawns.append((type(pawn), position))
    
    def set_pawn_at_the_position(self, pawn: Pawn, position: Point):
        self.board[position.y][position.x] = pawn
    
    def set_pawns(self, pawns: List[tuple]):
        for pawn_type, position in pawns:
            pawn = pawn_type()
            self.board[position.y][position.x] = pawn

    def set_white_pawns(self):
        self.set_pawns(self.white_pawns)

    def set_black_pawns(self):
        self.set_pawns(self.black_pawns)
    
    def set_empty_position(self, position: Point):
        self.board[position.y][position.x] = EMPTY_SQUARE

    def is_path_clear(self, current_pos: Point, new_pos: Point):  
        distance_x = new_pos.x - current_pos.x
        distance_y = new_pos.y - current_pos.y

        step_x = (distance_x // abs(distance_x)) if distance_x != 0 else 0
        step_y = (distance_y // abs(distance_y)) if distance_y != 0 else 0

        x, y = current_pos.x + step_x, current_pos.y + step_y

        while(x, y) != (new_pos.x, new_pos.y):
            if self.board[y][x] != EMPTY_SQUARE:
                return False
            x += step_x
            y += step_y
        return True

    def is_out_of_bounds(self, position: Point):
        return not (0 <= position.x < self.width and 0 <= position.y < self.height)

    def check_whose_turn(self):
        if len(self.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def switch_turn(self):
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE

    def is_check(self):
        if self.check_whose_turn() == Color.WHITE:
            return self.can_make_a_check(self.black_pawns)
        if self.check_whose_turn() == Color.BLACK:
            return self.can_make_a_check(self.white_pawns)
        return False
    
    def can_make_a_check(self, pawns_list: list[tuple]):
        for pawn_type, position in pawns_list:
            pawn = self.board[position.y][position.x]
            king_pos = self.get_king_position(pawn)
            if isinstance(pawn, Knight):
                if pawn.can_capture(position, king_pos):
                    return True
            elif pawn.can_capture(position, king_pos) and self.is_path_clear(position, king_pos):
                return True
        return False

    def get_king_position(self, opponent: Pawn):
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color != opponent.color:
                    return Point(x, y)
        return None

    def is_checkmate(self):
        pass


def main():
    board = Board(8, 8)
    board.set_white_pawns()
    board.set_black_pawns()
    while True:
        try:
            print(f"{board.check_whose_turn()} turn")
            print(board)
            move = input("Enter move: ")
            current_pos, new_pos = move.split(" ")
            current_pos = Point(int(current_pos[0]), int(current_pos[1]))
            new_pos = Point(int(new_pos[0]), int(new_pos[1]))
            board.move_piece(current_pos, new_pos)
        except (ValueError, IndexError):
            print("You have to provide the correct data")


if __name__ == "__main__":
    main()
