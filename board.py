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
    
    def __getitem__(self, index):
        return self.board[index]

    def __str__(self):
        board_str = ""
        for row in reversed(self.board):
            board_str += "".join([f"|{pawn.__str__()}|" if isinstance(pawn, Pawn) else "|__ |" for pawn in row]) + "\n"
            logger.info("Created board string")
        return board_str

    def set_pawns(self, pawns: List[tuple]):
        for pawn_class, position in pawns:
            pawn = pawn_class()
            self.board[position.y][position.x] = pawn
            logger.info("Set pawns on the board")

    def set_pawn_at_the_position(self, pawn: Pawn, current_pos: Point, position: Point):
        if self.check_whose_turn() == Color.WHITE:
            self.white_pawns.remove((type(pawn), current_pos))
            self.white_pawns.append((type(pawn), position))
        elif self.check_whose_turn() == Color.BLACK:
            self.black_pawns.remove((type(pawn), current_pos))
            self.black_pawns.append((type(pawn), position))
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
            elif self.is_move_valid(pawn, current_pos, new_pos):
                self.set_pawn_at_the_position(pawn, current_pos, new_pos)
                self.set_empty_position(current_pos)
                self.movements_history.append((current_pos, new_pos))
                if self.is_check():
                    print("Check")
            
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if isinstance(pawn, Knight):
            if pawn.can_move(current_pos, new_pos):
                if isinstance(self.board[new_pos.y][new_pos.x], str):
                    return True
        elif pawn.can_move(current_pos, new_pos) and self.is_path_clear(current_pos, new_pos):
            if isinstance(self.board[new_pos.y][new_pos.x], str):
                return True
        logger.info("Move is not valid")
        return False
    
    def is_path_clear(self, current_pos: Point, new_pos: Point):  
        dx = new_pos.x - current_pos.x
        dy = new_pos.y - current_pos.y

        step_x = (dx // abs(dx)) if dx != 0 else 0
        step_y = (dy // abs(dy)) if dy != 0 else 0

        x, y = current_pos.x + step_x, current_pos.y + step_y

        while(x, y) != (new_pos.x, new_pos.y):
            if self.board[y][x] != "|__|":
                return False
            x += step_x
            y += step_y
        return True
    
    def get_opponent(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        if not self.is_out_of_bounds(new_pos):
            opponent = self.board[new_pos.y][new_pos.x]
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        logger.info("No opponent found")
        return None
    
    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        target_pawn = self.get_opponent(pawn, current_pos, new_pos)
        if target_pawn:
            target_pawn, pos = target_pawn
            if pawn.can_capture(current_pos, new_pos) and target_pawn:
                if isinstance(pawn, Knight):
                    return True
                elif self.is_path_clear(current_pos, new_pos):
                    return True
        logger.info("Capture is not valid")
        return

    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point):
        target_pawn, target_pawn_pos = self.get_opponent(pawn, current_pos, new_pos)
        self.captured_pawns.append(target_pawn)
        if self.check_whose_turn() == Color.WHITE:
            self.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif self.check_whose_turn() == Color.BLACK:
            self.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.set_pawn_at_the_position(pawn, current_pos, target_pawn_pos)
        self.movements_history.append((current_pos, target_pawn_pos))
        self.set_empty_position(current_pos)

    def is_out_of_bounds(self, position: Point):
        return not (0 <= position.x < self.width and 0 <= position.y < self.height)

    def check_whose_turn(self):
        if len(self.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK

    def is_check(self):
        if self.check_whose_turn() == Color.WHITE:
            return self.can_make_a_check(self.black_pawns)
        if self.check_whose_turn() == Color.BLACK:
            return self.can_make_a_check(self.white_pawns)
        return False
    
    def can_make_a_check(self, pawns_list: list[tuple]):
        for pawn_class, position in pawns_list:
            pawn = self.board[position.y][position.x]
            king_pos = self.get_king_position(pawn)
            if isinstance(pawn, Knight):
                if pawn.can_move(position, king_pos):
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

    def get_movements_history(self):
        return self.movements_history

    def get_available_moves(self):
        pass

    def get_available_captures(self):
        pass


board = Board(8, 8)
board.set_white_pawns()
board.set_black_pawns()
board.move_pawn(Point(0, 1), Point(0, 3))
board.move_pawn(Point(1, 6), Point(1, 4))
board.move_pawn(Point(0, 3), Point(1, 4))
board.move_pawn(Point(3, 6), Point(3, 4))
board.move_pawn(Point(3, 1), Point(3, 3))
board.move_pawn(Point(3, 7), Point(3, 6))
board.move_pawn(Point(1, 0), Point(2, 2))
board.move_pawn(Point(3, 6), Point(3, 5))
board.move_pawn(Point(3, 0), Point(3, 2))

print(board)
