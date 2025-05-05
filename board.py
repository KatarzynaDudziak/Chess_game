from typing import List, Optional
import logging
logger = logging.getLogger()

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
    
    def get_board(self) -> list[list[Pawn]]:
        return self.board
    
    def get_piece(self, point: Point) -> Pawn:
        return self.board[point.y][point.x]
    
    def get_piece_at_the_position(self, position: Point) -> Pawn:
        return self.board[position.y][position.x]
    
    def get_king_position(self, opponent: Pawn) -> Optional[Point]:
        for y, row in enumerate(self.get_board()):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color != opponent.color:
                    return Point(x, y)
        return None

    def add_pawn_to_the_list(self, pawn: Pawn, current_pos: Point, position: Point) -> None: 
        if pawn.color == Color.WHITE:
            self.white_pawns.remove((type(pawn), current_pos))
            self.white_pawns.append((type(pawn), position))
            print(f"White pawns: {self.white_pawns}")
        elif pawn.color == Color.BLACK:
            self.black_pawns.remove((type(pawn), current_pos))
            self.black_pawns.append((type(pawn), position))

    def update_board_after_capture(self, pawn: Pawn, target_pawn_pos,
                                    target_pawn, current_pos, new_pos, check_whose_turn) -> None:
        if isinstance(target_pawn, King):
            print("Can't capture King!")
            return
        if check_whose_turn() == Color.WHITE:
            self.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif check_whose_turn() == Color.BLACK:
            self.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.movements_history.append((current_pos, target_pawn_pos))
        self.set_empty_position(current_pos)

    def execute_move(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> None:
        logger.info(f"Execute move piece from {current_pos} to {new_pos}")
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_pawn_at_the_position(pawn, new_pos)
        self.set_empty_position(current_pos)
        logger.info(f"Move executed: {pawn} from {current_pos} to {new_pos}")
        self.movements_history.append((current_pos, new_pos))
    
    def set_pawn_at_the_position(self, pawn: Pawn, position: Point) -> None:
        logger.info(f"Setting {pawn} at the {position}")
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
        logger.info(f"Set empty position at {self.board[position.y][position.x] }")

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
    
    def make_move(self, pawn: Pawn, new_pos: Point, current_pos: Point) -> None:
        self.set_pawn_at_the_position(pawn, new_pos)
        self.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.set_empty_position(current_pos)

    def undo_move(self, pawn: Pawn, current_pos: Point, new_pos: Point, original_target: Pawn) -> None:
        self.set_pawn_at_the_position(original_target, new_pos)
        self.add_pawn_to_the_list(pawn, new_pos, current_pos)
        self.set_pawn_at_the_position(pawn, current_pos)

    def will_the_move_escape_the_check(self, pawn: Pawn, attacked_king_color: Color, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        if attacked_king_color == check_whose_turn():
            original_target = self.board[new_pos.y][new_pos.x]
            self.make_move(pawn, new_pos, current_pos)
            try:
                attacked_king_color = is_check(check_whose_turn)
                if not attacked_king_color:
                    logger.info("The move can escape the check")
                    return True
                elif attacked_king_color != check_whose_turn():
                    logger.info("The move can escape the check and will cause the check")
                    return True
                else:
                    logger.info("The move won't escape the check")
                    return False
            finally:
                self.undo_move(pawn, current_pos, new_pos, original_target)
        return False
    
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        original_target = self.board[new_pos.y][new_pos.x]
        self.make_move(pawn, new_pos, current_pos)
        try:
            attacked_king_color = is_check(check_whose_turn)
            if attacked_king_color == check_whose_turn():
                logger.info(f"Your king {attacked_king_color} is under check")
                return False
            elif attacked_king_color != None:
                logger.info(f"{attacked_king_color} is under check. You can attack!")
                return True
            else:
                logger.info(f"There is no check after simulated move, who: {pawn}, from: {current_pos}, to: {new_pos}")
                return True
        finally:
            self.undo_move(pawn, current_pos, new_pos, original_target)

    def is_simulated_action_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        attacked_king_color = is_check(check_whose_turn)
        logger.info(f"Before first move {attacked_king_color}")
        if attacked_king_color != None:
            return self.will_the_move_escape_the_check(pawn, attacked_king_color, current_pos, new_pos, is_check, check_whose_turn) 
        else:
             return self.is_move_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
