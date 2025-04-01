from typing import Optional
import logging
logger = logging.getLogger(__name__)

from point import Point
from pawns import *
from board import EMPTY_SQUARE


class Move:
    def __init__(self, board) -> None:
        self.board = board

    def move_piece(self, current_pos: Point, new_pos: Point, check_whose_turn, is_check, switch_turn) -> bool:
        logger.info(f"Moving piece from {current_pos} to {new_pos}")
        pawn = self.board.get_piece_at_the_position(current_pos)
        if isinstance(pawn, Pawn):
            if pawn.color != check_whose_turn():
                logger.info("It's not your turn!")
                return False
            if self.is_capture_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                logger.info("Capture is valid")
                self.capture(pawn, current_pos, new_pos, check_whose_turn)
            elif self.is_move_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                self.board.execute_move(pawn, current_pos, new_pos)
                logger.info("Move is valid")
            else:
                logger.info("Move is not valid")
                return False
            if is_check(check_whose_turn):
                logger.info("Check!")
            switch_turn()
            return True
        return False

    def is_capture_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        target_pawn = self.get_opponent(pawn, new_pos)
        if target_pawn:
            pos = target_pawn[1]
            if pawn.can_capture(current_pos, new_pos) and \
                self.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn):
                if isinstance(pawn, Knight):
                    return True
                elif self.board.is_path_clear(current_pos, new_pos):
                    return True 
        return False
        
    def capture(self, pawn: Pawn, current_pos: Point, new_pos: Point, check_whose_turn) -> None:
        opponent = self.get_opponent(pawn, new_pos)
        if opponent is None:
            return
        target_pawn, target_pawn_pos = opponent
        self.board.captured_pawns.append(target_pawn)
        if check_whose_turn() == Color.WHITE:
            self.board.black_pawns.remove((type(target_pawn), target_pawn_pos))
        elif check_whose_turn() == Color.BLACK:
            self.board.white_pawns.remove((type(target_pawn), target_pawn_pos))
        self.board.add_pawn_to_the_list(pawn, current_pos, new_pos)
        self.board.set_pawn_at_the_position(pawn, target_pawn_pos)
        self.board.movements_history.append((current_pos, target_pawn_pos))
        self.board.set_empty_position(current_pos)

    def get_opponent(self, pawn: Pawn, new_pos: Point) -> Optional[tuple[Pawn, Point]]:
        if not self.board.is_out_of_bounds(new_pos):
            opponent = self.board.board[new_pos.y][new_pos.x]
            if isinstance(opponent, Pawn) and opponent.color != pawn.color:
                return opponent, new_pos
        return None
        
    def is_move_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        if isinstance(pawn, Knight):
            if pawn.can_move(current_pos, new_pos):
                if self.board.board[new_pos.y][new_pos.x] == EMPTY_SQUARE:
                    return self.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
        elif pawn.can_move(current_pos, new_pos) and self.board.is_path_clear(current_pos, new_pos):
            if self.board.board[new_pos.y][new_pos.x] == EMPTY_SQUARE:
                return self.is_simulated_action_valid(pawn, current_pos, new_pos, is_check, check_whose_turn)
        logger.info("Move is not valid")
        return False
        
    def is_simulated_action_valid(self, pawn: Pawn, current_pos: Point, new_pos: Point, is_check, check_whose_turn) -> bool:
        original_target = self.board.board[new_pos.y][new_pos.x]
        logger.info(f"Simulating move: {pawn} from {current_pos} to {new_pos}")
        logger.info(f"Original target at {new_pos}: {original_target}")
        logger.info(f"Board state before simulation:\n{self.board}")
        self.board.set_pawn_at_the_position(pawn, new_pos)
        self.board.set_empty_position(current_pos)
        try:
            if not is_check(check_whose_turn):
                return True
        finally:
            self.board.set_pawn_at_the_position(original_target, new_pos)
            self.board.set_pawn_at_the_position(pawn, current_pos)
            logger.info(f"Board state after restoring:\n{self.board}")
        return False
