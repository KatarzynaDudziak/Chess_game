import pygame

from game_over_exception import GameOverException
from check_exception import CheckException
import utils

logger = utils.get_logger(__name__)

class InputHandler:
    START_EVENT = pygame.USEREVENT + 1
    SOLO_GAME_EVENT = pygame.USEREVENT + 1
    ONLINE_GAME_EVENT = pygame.USEREVENT + 2

    def __init__(self, engine, game_manager, game_renderer) -> None:
        self.engine = engine
        self.game_manager = game_manager
        self.game_renderer = game_renderer
        self.game_started = False
        self.selected_piece = None
        self.selected_point = None

    def set_game_state(self, game_started: bool) -> None:
        self.game_started = game_started

    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            logger.debug(f"Mouse button down at {self.game_started}")
            if not self.game_started and self.game_renderer.solo_rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(InputHandler.START_EVENT))
            elif not self.game_started and self.game_renderer.online_rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(InputHandler.ONLINE_GAME_EVENT))
            else:
                self.selected_point = self.game_manager.convert_pixel_point_to_board_point()
        elif event.type == pygame.MOUSEBUTTONUP:
            new_point = self.game_manager.convert_pixel_point_to_board_point()
            self.game_renderer.highlight_square(new_point)
            try:
                if self.engine.move_piece(self.selected_point, new_point):
                    pass
            except GameOverException as ex:
                self.game_manager.handle_checkmate_exception(ex)
                return False
            except CheckException as ex:
                self.game_manager.handle_check_exception(ex)
        elif event.type == pygame.QUIT:
            return False
        return True
