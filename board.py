from typing import List
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from point import Point
from pawns import *

EMPTY_SQUARE = " "


class Board:
    def __init__(self, width: int, height: int) -> None:
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
        self.set_white_pawns()
        self.set_black_pawns()
        self.movements_history: list[tuple[Point, Point]] = []
        self.captured_pawns: list[Pawn] = [] 
        
    def __str__(self) -> str:
        board_str = ""
        for row in reversed(self.board):
            board_str += "".join([f"|{pawn.__str__()}|" if isinstance(pawn, Pawn) else "|__ |" for pawn in row]) + "\n"
        return board_str
    
    def get_piece_at_the_position(self, position: Point) -> Pawn:
        return self.board[position.y][position.x]

    def add_pawn_to_the_list(self, pawn: Pawn, current_pos: Point, position: Point) -> None:
        if pawn.color == Color.WHITE:
            self.white_pawns.remove((type(pawn), current_pos))
            self.white_pawns.append((type(pawn), position))
        elif pawn.color == Color.BLACK:
            self.black_pawns.remove((type(pawn), current_pos))
            self.black_pawns.append((type(pawn), position))

    def execute_move(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> None:
        logger.info(f"Execute move piece from {current_pos} to {new_pos}")
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_pawn_at_the_position(pawn, new_pos)
        self.set_empty_position(current_pos)
        self.movements_history.append((current_pos, new_pos))
    
    def set_pawn_at_the_position(self, pawn: Pawn, position: Point) -> None:
        self.board[position.y][position.x] = pawn
    
    def set_pawns(self, pawns: List[tuple]) -> None:
        for pawn, position in pawns:
            self.board[position.y][position.x] = pawn()

    def set_white_pawns(self) -> None:
        self.set_pawns(self.white_pawns)

    def set_black_pawns(self) -> None:
        self.set_pawns(self.black_pawns)
    
    def set_empty_position(self, position: Point) -> None:
        self.board[position.y][position.x] = EMPTY_SQUARE

    def is_out_of_bounds(self, position: Point) -> bool:
        return not (0 <= position.x < self.width and 0 <= position.y < self.height)
    
    def is_path_clear(self, current_pos: Point, new_pos: Point) -> bool:  
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
