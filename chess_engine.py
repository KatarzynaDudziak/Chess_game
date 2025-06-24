import pygame

import utils
from board import Board
from point import Point
from pawns import *
from move_handler import MoveHandler
from check_handler import CheckHandler
from capture_handler import CaptureHandler
from game_over_exception import GameOverException
from check_exception import CheckException

logger = utils.get_logger(__name__)


class ChessEngine:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        self.move_handler = MoveHandler(self.board)
        self.capture_handler = CaptureHandler(self.board)
        self.check_handler = CheckHandler(self.board, self.move_handler, self.capture_handler)

    def get_board(self) -> Board:
        return self.board.get_board()

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        turn = self.check_whose_turn()
        if not self.move_handler.move_piece(current_pos, new_pos, turn, self.check_handler):
            logger.debug("move_handler.move_piece() is not valid, is it capture?")
            piece = self.board.get_piece(current_pos)
            if self.capture_handler.capture(piece, current_pos, new_pos, turn, self.check_handler):
                if self.check_handler.get_checked_king_color(turn) != None:
                    self.__handle_checkmate_or_check(turn, self.check_handler)
            else:
                logger.debug("move is not valid and there is no check")
        elif self.check_handler.get_checked_king_color(turn) != None:
            self.__handle_checkmate_or_check(turn, self.check_handler)
        else:
            logger.debug("move_handler.move_piece is valid")
        return True
    
    def __handle_checkmate_or_check(self, turn, check_handler) -> bool:
        if self.__is_checkmate(turn, check_handler):
            raise GameOverException("Checkmate! Game over!")
        logger.debug("The king is under check")
        self.current_turn = self.__switch_turn()
        raise CheckException("Check!")
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def __is_checkmate(self, turn, check_handler) -> bool:
        turn = self.check_whose_turn()
        if turn == Color.WHITE:
            if self.check_handler.is_checkmate(self.board.get_white_pawns(), turn, check_handler):
                logger.info(f"The white king is in checkmate! current turn: {turn}")                
                return True
            else:
                logger.info(f"The white king is not in checkmate! current turn: {turn}")                
                return False
        elif turn == Color.BLACK:
            if self.check_handler.is_checkmate(self.board.get_black_pawns(), turn, check_handler):
                logger.info(f"The black king is in checkmate! current turn: {turn}")                
                return True
            else:
                logger.info(f"The black king is not in checkmate! current turn: {turn}")
                return False
            
    def __switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
