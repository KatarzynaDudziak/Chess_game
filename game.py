import pygame  # type: ignore
from typing import Optional
from pathlib import Path

from chessgame import *
from pawns import *
from check_exception import CheckException


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.chessgame = ChessGame()
        self.board = self.chessgame.board
        self.board_width = 904
        self.board_height = 904
        self.square_width = 106
        self.square_height = 106
        self.piece_size = (104, 104)
        self.frame_width = 28
        self.red_text_color = (255, 0, 0)
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        self.font = pygame.font.Font(None, 48)
        self.selected_point = None
        self.selected_piece = None

        self.bg = self.load_and_scale_image("images/board_images/board.png", (self.board_width, self.board_height))
        self.dark_square = self.load_and_scale_image("images/board_images/squareB.png", (self.square_width, self.square_height))
        self.light_square = self.load_and_scale_image("images/board_images/squareW.png", (self.square_width, self.square_height))
    
        self.pieces = {
            WhitePawn: self.load_and_scale_image("images/pawnW2.png"),
            WhiteRook: self.load_and_scale_image("images/rookW2.png"),
            WhiteKnight: self.load_and_scale_image("images/knightW2.png"),
            WhiteBishop: self.load_and_scale_image("images/bishopW2.png"),
            WhiteQueen: self.load_and_scale_image("images/queenW2.png"),
            WhiteKing: self.load_and_scale_image("images/kingW2.png"),
            BlackPawn: self.load_and_scale_image("images/pawnB2.png"),
            BlackRook: self.load_and_scale_image("images/rookB2.png"),
            BlackKnight: self.load_and_scale_image("images/knightB2.png"),
            BlackBishop: self.load_and_scale_image("images/bishopB2.png"),
            BlackQueen: self.load_and_scale_image("images/queenB2.png"),
            BlackKing: self.load_and_scale_image("images/kingB2.png")
        }

    def load_and_scale_image(self, image_path: Path, size=None) -> pygame.Surface:
        if size is None:
            size = self.piece_size
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)

    def draw(self) -> None:
        for row in range(8):
            for column in range(8):
                square = self.dark_square if (row + column) % 2 == 0 else self.light_square
                self.screen.blit(square, (self.frame_width + row * self.square_width, \
                                                         self.board_height - self.frame_width - self.square_height - column * self.square_height))
              
        for pawn_type, point in self.board.white_pawns + self.board.black_pawns:
            self.screen.blit(self.pieces[pawn_type], (self.frame_width + point.x * self.square_width, \
                                                       self.board_height - self.frame_width - self.square_height - point.y * self.square_height))
       
    def convert_to_point(self, x: int, y: int) -> Point:
        return Point(abs((x - self.frame_width)) // self.square_width, abs((self.board_height - self.frame_width - y)) // self.square_height)

    def update_board_and_pieces(self) -> None:
        self.draw()

    def handle_check_exception(self, ex: Exception) -> None:
        self.update_board_and_pieces()
        self.show_check_message(ex)

    def handle_checkmate_exception(self, ex: Exception) -> None:
        self.update_board_and_pieces()
        self.show_checkmate_message(ex)

    def show_checkmate_message(self, ex: Exception) -> None:
        game_over = self.font.render("Checkmate! Game over!", True, self.red_text_color, None)
        game_over_rect = game_over.get_rect(center=(self.board_width//2, self.board_height//2))
        self.screen.blit(game_over, game_over_rect)
        pygame.display.update()
        pygame.time.wait(3000)
        logger.info(f"GameOverException occurred: {ex}")

    def show_check_message(self, ex: Exception) -> None:
        check = self.font.render("Check!", True, self.red_text_color, None)
        check_rect = check.get_rect(center=(self.board_width//2, self.board_height//2))
        self.screen.blit(check, check_rect)
        pygame.display.update()
        pygame.time.wait(1000)
        logger.info(f"CheckException occurred: {ex}")

    def convert_pixel_point_to_board_point(self) -> Point:
        piece_pos = pygame.mouse.get_pos()
        x, y = piece_pos
        return self.convert_to_point(x, y)

    def move_piece(self, piece: Pawn, new_point: Point) -> None:
        if type(piece) in self.pieces:
            self.screen.blit(self.pieces[type(piece)], (self.frame_width + new_point.x * self.square_width, \
                                                         self.board_height - self.frame_width - self.square_height - new_point.y * self.square_height))
        else:
            print(f"Error: Piece type {type(piece)} not found in pieces dictionary.")

    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_point = self.convert_pixel_point_to_board_point()
            self.selected_piece = self.board.get_piece_at_the_position(self.selected_point)
            if self.selected_piece:
                print(f"The piece {self.selected_piece.__class__.__name__} and the position {self.selected_point.x} {self.selected_point.y}")
        elif event.type == pygame.MOUSEBUTTONUP:
            new_point = self.convert_pixel_point_to_board_point()
            try:
                if self.chessgame.move_piece(self.selected_point, new_point):
                    self.move_piece(self.selected_piece, new_point) 
            except GameOverException as ex:
                self.handle_checkmate_exception(ex)
                return False
            except CheckException as ex:
                self.handle_check_exception(ex)
        elif event.type == pygame.QUIT:
            return False
        return True


def main():
    game = Game()
    running = True
    while running:
        game.screen.blit(game.bg, (0, 0))
        game.update_board_and_pieces()
        try:
            for event in pygame.event.get():
                if not game.handle_input(event):
                    running = False
            pygame.display.update()
        except Exception as ex:
            logger.error(f"An unexpected error occurred: {ex}")
    pygame.quit()


if __name__=="__main__":
    main()
