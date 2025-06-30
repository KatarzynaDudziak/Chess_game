import pygame

import utils
from client import ChessClient
from chess_engine import ChessEngine
from game_manager import GameManager
from game_renderer import GameRenderer
from input_handler import InputHandler
from chess_server import MessageType


logger = utils.get_logger(__name__)


class WindowChessGame:
    def __init__(self) -> None:
        pygame.init()
        self.engine = None
        self.__init_game_components()

    def update_board(self) -> None:
        self.game_manager.update_board_and_pieces()
        pygame.display.update()

    def __switch_game_to_solo(self) -> None:
        self.engine = ChessEngine()
        self.__init_game_components()
        logger.info("Switched to solo game mode.")

    def __switch_game_to_online(self) -> None:
        self.engine = ChessClient(self.update_board)
        self.__init_game_components()
        self.engine.connect()
        logger.info("Switched to online game mode.")

    def __init_game_components(self) -> None:
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
                self.game_renderer.solo_rect = None
                self.game_renderer.online_rect = None
                self.game_renderer.screen.fill((0, 0, 0))
                self.game_renderer.screen.blit(self.game_renderer.bg, (0, 0))
                self.game_renderer.draw_board_and_pieces()
                pygame.display.update()
            try:
                for event in pygame.event.get():
                    if event.type == InputHandler.SOLO_GAME_EVENT:
                        self.__switch_game_to_solo()
                        game_started = True
                        self.input_handler.set_game_state(game_started)
                    elif event.type == InputHandler.ONLINE_GAME_EVENT:
                        self.__switch_game_to_online()
                        game_started = True
                        self.input_handler.set_game_state(game_started)
                    elif not self.input_handler.handle_input(event):
                        running = False
            except Exception as ex:
                logger.error(f"An unexpected error occurred: {ex}")
        pygame.quit()
        

def main():
    game = WindowChessGame()
    game.run()


if __name__ == "__main__":
    main()
  