import pygame

from board import Board
from pawns import *

pygame.init()
board = Board(8, 8)
screen = pygame.display.set_mode((904, 904))

def load_and_scale_image(image_path, size=(104, 104)):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, size)

bg = load_and_scale_image("images/board_images/board.png", (904, 904))
dark_square = load_and_scale_image("images/board_images/squareB.png", (106, 106))
light_square = load_and_scale_image("images/board_images/squareW.png", (106, 106))
white_pawn = load_and_scale_image("images/pawnW2.png")
white_rook = load_and_scale_image("images/rookW2.png")
white_knight = load_and_scale_image("images/knightW2.png")
white_bishop = load_and_scale_image("images/bishopW2.png")
white_queen = load_and_scale_image("images/queenW2.png")
white_king = load_and_scale_image("images/kingW2.png")
black_pawn = load_and_scale_image("images/pawnB2.png")
black_rook = load_and_scale_image("images/rookB2.png")
black_knight = load_and_scale_image("images/knightB2.png")
black_bishop = load_and_scale_image("images/bishopB2.png")
black_queen = load_and_scale_image("images/queenB2.png")
black_king = load_and_scale_image("images/kingB2.png")

pieces = {
    WhitePawn: white_pawn,
    WhiteRook: white_rook,
    WhiteKnight: white_knight,
    WhiteBishop: white_bishop,
    WhiteQueen: white_queen,
    WhiteKing: white_king,
    BlackPawn: black_pawn,
    BlackRook: black_rook,
    BlackKnight: black_knight,
    BlackBishop: black_bishop,
    BlackQueen: black_queen,
    BlackKing: black_king
}


running = True
while running:
    for event in pygame.event.get():
        screen.blit(bg, (0, 0))

        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    screen.blit(dark_square, (28 + row * 106, 770 - column * 106))
                else:
                    screen.blit(light_square, (28 + row * 106, 770 - column * 106))
                    
        for pawn_type, point in board.white_pawns:
            screen.blit(pieces[pawn_type], (28 + point.x * 106, 770 - point.y * 106))
        for pawn_type, point in board.black_pawns:
            screen.blit(pieces[pawn_type], (28 + point.x * 106, 770 - point.y * 106))
            

        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
