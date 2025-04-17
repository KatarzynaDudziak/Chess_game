import pygame

from game_over_exception import GameOverException
from check_exception import CheckException


class InputHandler:
    def __init__(self, board, game_manager, move_piece) -> None:
        self.board = board
        self.game_manager = game_manager
        self.move_piece = move_piece

    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_point = self.game_manager.convert_pixel_point_to_board_point()
            self.selected_piece = self.board.get_piece_at_the_position(self.selected_point)
            if self.selected_piece:
                print(f"The piece {self.selected_piece} and the position {self.selected_point.x} {self.selected_point.y}")
        elif event.type == pygame.MOUSEBUTTONUP:
            new_point = self.game_manager.convert_pixel_point_to_board_point()
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
