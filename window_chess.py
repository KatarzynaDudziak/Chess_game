import pygame
import traceback

import utils
from game_manager import GameManager
from game_renderer import GameRenderer
from input_handler import InputHandler
from chess_engine import ChessEngine

logger = utils.get_logger(__name__)


class WindowChess:
    def __init__(self) -> None:
        pygame.init()
        self.engine = ChessEngine()
        self.game_renderer = GameRenderer(self.engine)
        self.game_manager = GameManager(self.game_renderer)
        self.input_handler = InputHandler(self.engine, self.game_manager, self.game_renderer)

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
                traceback.print_exc()
        pygame.quit()


def main():
    game = WindowChess()
    game.run()
    
    
if __name__=="__main__":
    main()
