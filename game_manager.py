import pygame  # type: ignore

from pawns import *
from board import Board
from point import Point

class GameManager:
    def __init__(self, board: Board, game_renderer) -> None:
        self.game_renderer = game_renderer
        self.board = board
   
    def convert_to_point(self, x: int, y: int) -> Point:
        return Point(abs((x - self.game_renderer.frame_width)) // self.game_renderer.square_width, \
                     abs((self.game_renderer.board_height - self.game_renderer.frame_width - y)) // self.game_renderer.square_height)

    def update_board_and_pieces(self) -> None:
        self.game_renderer.draw_board_and_pieces()

    def handle_check_exception(self, ex: Exception) -> None:
        self.update_board_and_pieces()
        self.game_renderer.show_check_message(ex)

    def handle_checkmate_exception(self, ex: Exception) -> None:
        self.update_board_and_pieces()
        self.game_renderer.show_checkmate_message(ex)

    def get_pixel_piece_position(self) -> tuple[int, int]:
        piece_pos = pygame.mouse.get_pos()
        x, y = piece_pos
        return x, y
    
    def convert_pixel_point_to_board_point(self) -> Point:
        x, y = self.get_pixel_piece_position()
        return self.convert_to_point(x, y)
