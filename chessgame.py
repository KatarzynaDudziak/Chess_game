from typing import Optional
import logging, coloredlogs
coloredlogs.install()
logger = logging.getLogger(__name__)
logger.info("Information: ")
logger.debug("That happened: ")
logger.warning("Watch out: ")

from board import Board
from point import Point
from pawns import *
from move_handler import MoveHandler
from check_handler import CheckHandler
from capture_handler import CaptureHandler
from game_over_exception import GameOverException


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        self.move_handler = MoveHandler(self.board)
        self.check_handler = CheckHandler(self.board)
        self.capture_handler = CaptureHandler(self.board)

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        if not self.move_handler.move_piece(current_pos, new_pos, self.check_whose_turn, self.check_handler.is_check):
            logger.debug("move_handler.move_piece() is not valid, is it capture?")
            if self.capture_handler.is_capture_valid(self.board.get_piece_at_the_position(current_pos),
                                                        current_pos, new_pos, self.check_handler.is_check,
                                                        self.check_whose_turn):
                logger.debug("yes, it is capture")
                self.capture_handler.capture(self.board.get_piece_at_the_position(current_pos),
                                                current_pos, new_pos, self.check_whose_turn)
            elif self.check_handler.is_check(self.check_whose_turn):
                logger.info("Check!")
                logger.debug("switching turn because there is a check")
                self.switch_turn()
            else:
                logger.debug("move is not valid and there is no check")
        else:
            logger.debug("move_handler.move_piece is valid")

        if self.is_checkmate(self.board.white_pawns if self.check_whose_turn() == Color.WHITE else self.board.black_pawns):
            raise GameOverException("Checkmate! Game over!")
        return True   
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def is_checkmate(self, pawns_list: list[tuple]) -> bool:
        current_turn =  self.check_whose_turn()
        if current_turn == Color.WHITE:
            if self.check_handler.is_checkmate(self.board.white_pawns, self.check_whose_turn):
                logger.info("The white king is in checkmate!")                
                return True
            else:
                logger.info("The white king is not in checkmate, you can go on your turn!")                
                return False
        elif current_turn == Color.BLACK:
            if self.check_handler.is_checkmate(self.board.black_pawns, self.check_whose_turn):
                logger.info("The black king is in checkmate!")                
                return True
            else:
                logger.info("The black king is not in checkmate, you can go on your turn!")
                return False
            
    def switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
