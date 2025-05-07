import pygame
import logging, coloredlogs
coloredlogs.install(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Information: ")
logger.debug("Debug: ")
logger.warning("Warning: ")

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


class ChessGame:
    def __init__(self) -> None:
        self.board = Board(8, 8)
        pygame.init()
        self.font = pygame.font.Font(None, 48)
        self.chess_client = ChessClient()
        self.move_handler = MoveHandler(self.board)
        self.check_handler = CheckHandler(self.board)
        self.capture_handler = CaptureHandler(self.board)
        self.game_renderer = GameRenderer(self.board, self.font)
        self.game_manager = GameManager(self.board, self.game_renderer)
        self.input_handler = InputHandler(self.board, self.game_manager, self.game_renderer, self.move_piece)

    def move_piece(self, current_pos: Point, new_pos: Point) -> bool:
        if not self.move_handler.move_piece(current_pos, new_pos, self.check_whose_turn, self.check_handler.is_check):
            logger.debug("move_handler.move_piece() is not valid, is it capture?")
            if self.capture_handler.is_capture_valid(self.board.get_piece_at_the_position(current_pos),
                                                        current_pos, new_pos, self.check_handler.is_check,
                                                        self.check_whose_turn):
                logger.debug("yes, it is capture")
                self.capture_handler.capture(self.board.get_piece_at_the_position(current_pos),
                                                current_pos, new_pos, self.check_whose_turn)
                if self.check_handler.is_check(self.check_whose_turn) != None:
                    self.handle_checkmate_or_check()
            else:
                logger.debug("move is not valid and there is no check")
        elif self.check_handler.is_check(self.check_whose_turn) != None:
            self.handle_checkmate_or_check()
        else:
            logger.debug("move_handler.move_piece is valid")
        return True
    
    def handle_checkmate_or_check(self) -> bool:
        if self.is_checkmate():
            raise GameOverException("Checkmate! Game over!")
        logger.debug("The king is under check")
        self.current_turn = self.switch_turn()
        raise CheckException("Check!")
    
    def check_whose_turn(self) -> Color:
        if len(self.board.movements_history) % 2 == 0:
            return Color.WHITE
        return Color.BLACK
    
    def is_checkmate(self) -> bool:
        current_turn =  self.check_whose_turn()
        if current_turn == Color.WHITE:
            if self.check_handler.is_checkmate(self.board.white_pawns, self.check_whose_turn):
                logger.info("The white king is in checkmate!")                
                return True
            else:
                logger.info("The white king is not in checkmate!")                
                return False
        elif current_turn == Color.BLACK:
            if self.check_handler.is_checkmate(self.board.black_pawns, self.check_whose_turn):
                logger.info("The black king is in checkmate!")                
                return True
            else:
                logger.info("The black king is not in checkmate!")
                return False
            
    def switch_turn(self) -> Color:
        if self.check_whose_turn() == Color.WHITE:
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
