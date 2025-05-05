import pygame
import logging
logger = logging.getLogger(__name__)

from pawns import Pawn, WhitePawn, WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, \
      WhiteKing, BlackPawn, BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing
from board import Board
from point import Point


class GameRenderer:
    def  __init__(self, board: Board, font: pygame.font.Font) -> None:
        self.board = board
        self.font = font
        self.board_width = 904
        self.board_height = 904
        self.square_width = 106
        self.square_height = 106
        self.piece_size = (104, 104)
        self.frame_width = 28
        self.red_text_color = (255, 0, 0)
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        self.bg = self.load_and_scale_image("images/board_images/board.png", (self.board_width, self.board_height))
        self.dark_square = self.load_and_scale_image("images/board_images/squareB.png", (self.square_width, self.square_height))
        self.light_square = self.load_and_scale_image("images/board_images/squareW.png", (self.square_width, self.square_height))
        # self.start_button_rect = pygame.Rect(self.board_width//2 - 100, self.board_height//2, 200, 100)
        # self.start_button_color = (53, 3, 252)
            
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
    
    def load_and_scale_image(self, image_path: str, size=None) -> pygame.Surface:
        if size is None:
            size = self.piece_size
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)
    
    def draw_start_screen(self) -> None:
        self.screen.fill((3, 169, 252))

        title = pygame.font.Font(None, 74).render("Chess Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.board_width//2, self.board_height//2 - 100))
        self.screen.blit(title, title_rect)
        
        text = self.font.render("Start Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.board_width//2, self.board_height//2 + 50))
        self.button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
        pygame.draw.rect(self.screen, (0, 128, 255), self.button_rect)
        self.screen.blit(text, text_rect)

    def draw_board_and_pieces(self) -> None:
        for row in range(8):
            for column in range(8):
                square = self.dark_square if (row + column) % 2 == 0 else self.light_square
                self.screen.blit(square, (self.frame_width + row * self.square_width, \
                                                         self.board_height - self.frame_width - self.square_height - column * self.square_height))
              
        for pawn_type, point in self.board.white_pawns + self.board.black_pawns:
            self.screen.blit(self.pieces[pawn_type], (self.frame_width + point.x * self.square_width, \
                                                       self.board_height - self.frame_width - self.square_height - point.y * self.square_height))

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

    def render_moved_piece(self, piece: Pawn, new_point: Point) -> None:
        if type(piece) in self.pieces:
            self.screen.blit(self.pieces[type(piece)], (self.frame_width + new_point.x * self.square_width, \
                                                         self.board_height - self.frame_width - self.square_height - new_point.y * self.square_height))
        else:
            print(f"Error: Piece type {type(piece)} not found in pieces dictionary.")

    def highlight_square(self, point: Point) -> None:
        highlight = pygame.Rect(self.frame_width + point.x * self.square_width, \
                                 self.board_height - self.frame_width - self.square_height - point.y * self.square_height, \
                                 self.square_width, self.square_height)
        pygame.draw.rect(self.screen, (111, 252, 3), highlight, 5)
        pygame.time.wait(80)
                                     