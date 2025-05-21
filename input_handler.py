import pygame

from game_over_exception import GameOverException
from check_exception import CheckException
import utils

logger = utils.get_logger(__name__)

class InputHandler:
    START_EVENT = pygame.USEREVENT + 1

    def __init__(self, board, game_manager, game_renderer, move_piece) -> None:
        self.board = board
        self.game_manager = game_manager
        self.game_renderer = game_renderer
        self.move_piece = move_piece
        self.game_started = False
        self.selected_piece = None
        self.selected_point = None

    def set_game_state(self, game_started: bool) -> None:
        self.game_started = game_started

    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            logger.debug(f"Mouse button down at {self.game_started}")
            if not self.game_started and self.game_renderer.button_rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(InputHandler.START_EVENT))
            else:
                self.selected_point = self.game_manager.convert_pixel_point_to_board_point()
                self.selected_piece = self.board.get_piece_at_the_position(self.selected_point)
                if self.selected_piece:
                    self.game_renderer.highlight_square(self.selected_point)
                    print(f"The piece {self.selected_piece} and the position {self.selected_point.x} {self.selected_point.y}")
        elif event.type == pygame.MOUSEBUTTONUP:
            new_point = self.game_manager.convert_pixel_point_to_board_point()
            self.game_renderer.highlight_square(new_point)
            try:
                if self.move_piece(self.selected_point, new_point):
                    self.game_renderer.render_moved_piece(self.selected_piece, new_point)
            except GameOverException as ex:
                self.game_manager.handle_checkmate_exception(ex)
                return False
            except CheckException as ex:
                self.game_manager.handle_check_exception(ex)
        elif event.type == pygame.QUIT:
            return False
        return True
