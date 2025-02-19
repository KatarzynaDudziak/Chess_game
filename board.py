from typing import List
import logging
logger = logging.getLogger(__name__) 

from point import Point
from pawns import *


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [["|__|" for _ in range(width)] for _ in range(height)]
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
            logger.info("Created board string")
        return board_str

    def set_pawns(self, pawns: List[tuple]):
        for pawn_class, position in pawns:
            pawn = pawn_class()
            self.set_pawn_at_the_position(pawn, position)
            logger.info("Set pawns on the board")

    def set_pawn_at_the_position(self, pawn: Pawn, position: Point):
        self.board[position.y][position.x] = pawn

    def set_white_pawns(self):
        self.set_pawns(self.white_pawns)

    def set_black_pawns(self):
        self.set_pawns(self.black_pawns)
    
    def set_empty_position(self, position: Point):
        self.board[position.y][position.x] = " "

    def move_pawn(self, current_pos: Point, new_pos: Point):
        pawn = self.board[current_pos.y][current_pos.x]
        if isinstance(pawn, Pawn):
            if self.is_capture_valid(pawn, current_pos, new_pos):
                self.capture(pawn, current_pos, new_pos)
                logger.info("Captured opponent's pawn")
            elif self.is_move_valid(pawn, current_pos, new_pos):
                self.set_pawn_at_the_position(pawn, new_pos)
                self.set_empty_position(current_pos)
                self.movements_history.append((current_pos, new_pos))
                logger.info("Moved pawn")

    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if pawn.can_move(current_pos, new_pos):
            if isinstance(self.board[new_pos.y][new_pos.x], str):
                return True
        logger.info("Move is not valid")
        return False
    
    def get_opponents_positions(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if isinstance(pawn, WhitePawn):
            capture_positions = [
                Point(current_pos.x + 1, current_pos.y + 1),
                Point(current_pos.x - 1, current_pos.y + 1)
            ]
        elif isinstance(pawn, BlackPawn):
            capture_positions = [
                Point(current_pos.x + 1, current_pos.y - 1),
                Point(current_pos.x - 1, current_pos.y - 1)
            ]
        else:
            capture_positions = [new_pos]
        return capture_positions
    
    def get_opponent(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        capture_positions = self.get_opponents_positions(pawn, current_pos, new_pos)
        for pos in capture_positions:
            if self.is_not_out_of_bounds(pos):
                continue
            if isinstance(self.board[pos.y][pos.x], Pawn) and self.board[pos.y][pos.x].color != pawn.color:
                return self.board[pos.y][pos.x], pos
        logger.info("No opponent found")
        return
    
    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        target_pawn = self.get_opponent(pawn, current_pos, new_pos)
        if target_pawn:
            target_pawn, pos = target_pawn
            if pawn.can_capture(current_pos, Point(pos.x, pos.y)) and target_pawn:
                return True
        logger.info("Capture is not valid")
        return

    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        target_pawn, target_pawn_pos = self.get_opponent(pawn, current_pos, new_pos)
        self.captured_pawns.append(target_pawn)
        self.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.movements_history.append((current_pos, target_pawn_pos))
        self.set_empty_position(current_pos)

    def is_not_out_of_bounds(self, position: Point):
        return not (0 <= position.x < self.width and 0 <= position.y < self.height)

    def check_whose_turn(self):
        if len(self.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK

    def is_check(self):
        pass

    def is_checkmate(self):
        pass

    def get_movements_history(self):
        return self.movements_history

    def get_available_moves(self):
        return self.available_moves

    def get_available_captures(self):
        pass


board = Board(8, 8)
board.set_white_pawns()
board.set_black_pawns()
board.move_pawn(Point(0, 1), Point(0, 3))
print(board)
