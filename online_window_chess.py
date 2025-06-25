import pygame

import utils
from client import ChessClient
from game_manager import GameManager
from game_renderer import GameRenderer
from input_handler import InputHandler

logger = utils.get_logger(__name__)


class OnlineWindowChess:
    def __init__(self) -> None:
        pygame.init()
        self.client = ChessClient(self.update_board)
        self.game_renderer = GameRenderer(self.client)
        self.game_manager = GameManager(self.game_renderer)
        self.input_handler = InputHandler(self.client, self.game_manager, self.game_renderer)

    def update_board(self) -> None:
        self.game_manager.update_board_and_pieces()
        pygame.display.update()

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
                pygame.display.update()
            try:
                for event in pygame.event.get():
                    if event.type == InputHandler.SOLO_GAME_EVENT:
                        game_started = True
                        self.input_handler.set_game_state(game_started)
                    elif event.type == InputHandler.ONLINE_GAME_EVENT:
                        self.client.connect()
                        game_started = True
                        self.input_handler.set_game_state(game_started)
                    elif not self.input_handler.handle_input(event):
                        running = False
            except Exception as ex:
                logger.error(f"An unexpected error occurred: {ex}")
        pygame.quit()
        


def main():
    game = OnlineWindowChess()
    game.run()


if __name__ == "__main__":
    main()
  