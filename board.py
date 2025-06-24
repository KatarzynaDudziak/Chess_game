from typing import List, Optional

from point import Point
from pawns import *
import utils


EMPTY_SQUARE = " "
logger = utils.get_logger(__name__)


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
            (BlackRook, Point(0,7)), (BlackKnight, Point(1,7)), (BlackBishop, Point(2,7)), (BlackQueen, Point(3,7)),
            (BlackKing, Point(4,7)), (BlackBishop, Point(5,7)), (BlackKnight, Point(6,7)), (BlackRook, Point(7,7)),
            (BlackPawn, Point(0,6)), (BlackPawn, Point(1,6)), (BlackPawn, Point(2,6)), (BlackPawn, Point(3,6)),
            (BlackPawn, Point(4,6)), (BlackPawn, Point(5,6)), (BlackPawn, Point(6,6)), (BlackPawn, Point(7,6))
            ]
        self.__set_white_pawns()
        self.__set_black_pawns()
        self.movements_history: list[tuple[Point, Point]] = []
        self.captured_pawns: list[Pawn] = [] 
    
    def get_white_pawns(self) -> List[tuple]:
        return self.white_pawns.copy()
    
    def get_black_pawns(self) -> List[tuple]:
        return self.black_pawns.copy()
    
    def get_board(self) -> list[list[Pawn]]:
        return self.board
    
    def get_piece(self, point: Point) -> Pawn:
        return self.board[point.y][point.x]
    
    def get_king_position(self, opponent_color: Color) -> Optional[Point]:
        for y, row in enumerate(self.get_board()):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color != opponent_color:
                    return Point(x, y)
        return None

    def __set_pawn(self, pawn: Pawn, position: Point) -> None:
        logger.info(f"Setting {pawn} at the {position}")
        self.board[position.y][position.x] = pawn
    
    def __set_pawns(self, pawns: List[tuple]) -> None:
        for pawn, position in pawns:
            self.__set_pawn(pawn(), position)

    def __set_white_pawns(self) -> None:
        self.__set_pawns(self.white_pawns)

    def __set_black_pawns(self) -> None:
        self.__set_pawns(self.black_pawns)
    
    def __set_empty_position(self, position: Point) -> None:
        self.__set_pawn(EMPTY_SQUARE, position)

    def __add_pawn_to_the_list(self, pawn: Pawn, current_pos: Point, position: Point) -> None: 
        if pawn.color == Color.WHITE:
            self.white_pawns.remove((type(pawn), current_pos))
            self.white_pawns.append((type(pawn), position))
        elif pawn.color == Color.BLACK:
            self.black_pawns.remove((type(pawn), current_pos))
            self.black_pawns.append((type(pawn), position))

    def update_board_after_capture(self, pawn: Pawn, target_pawn_pos,
                                    target_pawn, current_pos, new_pos, turn) -> None:
        if isinstance(target_pawn, King):
            return
        if turn == Color.WHITE:
            self.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif turn == Color.BLACK:
            self.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.execute_move(pawn, current_pos, new_pos)

    def execute_move(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> None:
        self.__add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.__set_pawn(pawn, new_pos)
        self.__set_empty_position(current_pos)
        self.movements_history.append((current_pos, new_pos))
        logger.debug(f"Executed move: {pawn} from {current_pos} to {new_pos}")
    
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
                logger.debug(f"Path is not clear")
                return False
            x += step_x
            y += step_y
        logger.debug(f"Path is clear from {current_pos} to {new_pos}")
        return True
    
    # Methods related to move simulation
    def make_move(self, pawn: Pawn, new_pos: Point, current_pos: Point) -> None:
        self.__set_pawn(pawn, new_pos)
        self.__add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.__set_empty_position(current_pos)

    # Methods related to move simulation
    def undo_move(self, pawn: Pawn, current_pos: Point, new_pos: Point, original_target: Pawn) -> None:
        self.__set_pawn(original_target, new_pos)
        self.__add_pawn_to_the_list(pawn, new_pos, current_pos)
        self.__set_pawn(pawn, current_pos)
    
    # Methods related to move simulation
    def __is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_handler, turn) -> bool:
        original_target = self.board[new_pos.y][new_pos.x]
        self.make_move(pawn, new_pos, current_pos)
        try:
            attacked_king_color = check_handler.get_checked_king_color(turn)
            if attacked_king_color == turn:
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

    # Methods related to move simulation
    def is_simulated_action_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_handler, turn) -> bool:
        attacked_king_color = check_handler.get_checked_king_color(turn)
        logger.info(f"Before first move {attacked_king_color}")
        if attacked_king_color != None:
            return check_handler.will_the_move_escape_the_check(pawn, attacked_king_color, current_pos, new_pos, check_handler, turn) 
        else:
             return self.__is_move_valid(pawn, current_pos, new_pos, check_handler, turn)
