from typing import Optional

from board import Board
from point import Point
from pawns import *


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        
    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        pawn = self.board.get_piece_at_the_position(current_pos)
        if isinstance(pawn, Pawn):
            if pawn.color != self.check_whose_turn():
                logger.info("It's not your turn!")
                return False
            if self.is_capture_valid(pawn, current_pos, new_pos):
                logger.info("Capture is valid")
                self.capture(pawn, current_pos, new_pos)
            elif self.is_move_valid(pawn, current_pos, new_pos):
                self.board.execute_move(pawn, current_pos, new_pos)
                logger.info("Move is valid")
                if self.is_check():
                    logger.info("Check!")
                    self.switch_turn()
                return True
            logger.info("Move is not valid")
        return False

    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> bool:
        target_pawn = self.get_opponent(pawn, new_pos)
        if target_pawn:
            pos = target_pawn[1]
            if pawn.can_capture(current_pos, new_pos) and \
                self.is_simulated_action_valid(pawn, current_pos, new_pos):
                if isinstance(pawn, Knight):
                    return True
                elif self.board.is_path_clear(current_pos, new_pos):
                    return True 
        return False
        
    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> None:
        opponent = self.get_opponent(pawn, new_pos)
        if opponent is None:
            return
        target_pawn, target_pawn_pos = opponent
        self.board.captured_pawns.append(target_pawn)
        if self.check_whose_turn() == Color.WHITE:
            self.board.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif self.check_whose_turn() == Color.BLACK:
            self.board.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.board.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.board.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.board.movements_history.append((current_pos, target_pawn_pos))
        self.board.set_empty_position(current_pos)

    def get_opponent(self, pawn: Pawn, new_pos: Point) -> Optional[tuple[Pawn, Point]]:
        if not self.is_out_of_bounds(new_pos):
            opponent = self.board.board[new_pos.y][new_pos.x]
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        return None
        
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_move(current_pos, new_pos):
                if isinstance(self.board.board[new_pos.y][new_pos.x], str):
                    return self.is_simulated_action_valid(pawn, current_pos, new_pos)
        elif pawn.can_move(current_pos, new_pos) and self.board.is_path_clear(current_pos, new_pos):
            if isinstance(self.board.board[new_pos.y][new_pos.x], str):
                return self.is_simulated_action_valid(pawn, current_pos, new_pos)
        logger.info("Move is not valid")
        return False
        
    def is_simulated_action_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point) -> bool:
        original_target = self.board.board[new_pos.y][new_pos.x]
        self.board.set_pawn_at_the_position(pawn, new_pos)
        self.board.set_empty_position(current_pos)
        if not self.is_check():
            self.board.set_pawn_at_the_position(pawn, current_pos)
            self.board.set_pawn_at_the_position(original_target, new_pos)
            return True
        else:
            self.board.set_pawn_at_the_position(pawn, current_pos)
            self.board.set_pawn_at_the_position(original_target, new_pos)
        return False

    def is_out_of_bounds(self, position: Point) -> bool:
        return not (0 <= position.x < self.board.width and 0 <= position.y < self.board.height)
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK

    def is_check(self) -> bool:
        if self.check_whose_turn() == Color.WHITE:
            return self.can_make_a_check(self.board.black_pawns)
        if self.check_whose_turn() == Color.BLACK:
            return self.can_make_a_check(self.board.white_pawns)
        return False
    
    def is_checkmate(self, pawns_list: list[tuple]) -> bool:
        for pawn_type, position in pawns_list:
            pawn = self.board.board[position.y][position.x]
            for y in range(self.board.height):
                for x in range(self.board.width):
                    new_pos = Point(x, y)
                    if isinstance(pawn, Knight):
                        if (pawn.can_move(position, new_pos) or (pawn.can_capture(position, new_pos))):
                            if self.is_simulated_action_valid(pawn, position, new_pos):
                                return False
                    elif (pawn.can_move(position, new_pos) or (pawn.can_capture(position, new_pos))):
                        if self.is_simulated_action_valid(pawn, position, new_pos):
                            return False
        return True

    def can_make_a_check(self, pawns_list: list[tuple]) -> bool:
        for pawn_type, position in pawns_list:
            pawn = self.board.board[position.y][position.x]
            king_pos = self.get_king_position(pawn)
            if king_pos is not None:
                if isinstance(pawn, Knight):
                    if pawn.can_capture(position, king_pos):
                        return True
                elif pawn.can_capture(position, king_pos) and self.board.is_path_clear(position, king_pos):
                    return True
        return False

    def get_king_position(self, opponent: Pawn) -> Optional[Point]:
        for y, row in enumerate(self.board.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color != opponent.color:
                    return Point(x, y)
        return None

    def switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
