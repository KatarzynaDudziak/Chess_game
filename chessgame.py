import pygame

import utils
from board import Board
from point import Point
from pawns import *
from move_handler import MoveHandler
from check_handler import CheckHandler
from capture_handler import CaptureHandler
from game_renderer import GameRenderer
from game_over_exception import GameOverException
from check_exception import CheckException
from game_manager import GameManager
from input_handler import InputHandler
from client import ChessClient

logger = utils.get_logger(__name__)


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        pygame.init()
        self.font = pygame.font.Font(None, 48)
        self.chess_client = ChessClient()
        self.move_handler = MoveHandler(self.board)
        self.capture_handler = CaptureHandler(self.board)
        self.check_handler = CheckHandler(self.board, self.move_handler, self.capture_handler)
        
        self.game_renderer = GameRenderer(self.board, self.font)
        self.game_manager = GameManager(self.board, self.game_renderer)
        self.input_handler = InputHandler(self.board, self.game_manager, self.game_renderer, self.move_piece)

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        turn = self.__check_whose_turn()
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
    
    def __check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def __is_checkmate(self, turn, check_handler) -> bool:
        turn = self.__check_whose_turn()
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
        if self.__check_whose_turn() == Color.WHITE:
            return Color.BLACK
        return Color.WHITE
    
    def run(self) -> None:
        running = True
        game_started = False
        while running:
            if not game_started:
                self.game_renderer.draw_start_screen()
                pygame.display.update()
            else:
                self.game_renderer.button_rect = None
                self.game_renderer.screen.fill((0, 0, 0))
                self.game_renderer.screen.blit(self.game_renderer.bg, (0, 0))
                self.game_manager.update_board_and_pieces()
                pygame.display.update()
            try:
                for event in pygame.event.get():
                    if event.type == InputHandler.START_EVENT:
                        game_started = True
                        self.input_handler.set_game_state(game_started)
                    if not self.input_handler.handle_input(event):
                        running = False
                pygame.display.update()
            except Exception as ex:
                logger.error(f"An unexpected error occurred: {ex}")
        pygame.quit()


def main():
    game = ChessGame()
    game.run()
    
    
if __name__=="__main__":
    main()
