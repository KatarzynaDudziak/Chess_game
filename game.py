import pygame  # type: ignore

from chessgame import *
from pawns import *
from check_exception import CheckException

pygame.init()
chessgame = ChessGame()
board = chessgame.board
width = 904
height = 904
screen = pygame.display.set_mode((904, 904))
font = pygame.font.Font(None, 48)


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


def draw_board():
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                screen.blit(dark_square, (28 + row * 106, 904 - 28 - 106 - column * 106))
            else:
                screen.blit(light_square, (28 + row * 106, 904 - 28 - 106 - column * 106))


def draw_pieces():
    for pawn_type, point in board.white_pawns:
        screen.blit(pieces[pawn_type], (28 + point.x * 106, 904 - 28 - 106 - point.y * 106))
    for pawn_type, point in board.black_pawns:
        screen.blit(pieces[pawn_type], (28 + point.x * 106, 904 - 28 - 106 - point.y * 106))


def convert_to_point(x, y):
    return Point(abs((x - 28)) // 106, abs((904 - 28 - y)) // 106)


def update_board_and_pieces():
    draw_board()
    draw_pieces()


def show_checkmate_message():
    update_board_and_pieces()
    game_over = font.render("Checkmate! Game over!", True, (255, 0, 0), None)
    game_over_rect = game_over.get_rect(center=(width//2, height//2))
    screen.blit(game_over, game_over_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    logger.info(f"GameOverException occurred: {ex}")


def show_check_message():
    update_board_and_pieces()
    check = font.render("Check!", True, (255, 0, 0), None)
    check_rect = check.get_rect(center=(width//2, height//2))
    screen.blit(check, check_rect)
    pygame.display.update()
    pygame.time.wait(1000)
    logger.info(f"CheckException occurred: {ex}")


running = True
while running:
    screen.blit(bg, (0, 0))
    update_board_and_pieces()
    try:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                piece_pos = pygame.mouse.get_pos()
                x, y = piece_pos
                point = convert_to_point(x, y)
                piece = board.get_piece_at_the_position(point)
                if piece:
                    print(f"The piece {piece.__class__.__name__} and the position {point.x} {point.y}")
            elif event.type == pygame.MOUSEBUTTONUP:
                move = pygame.mouse.get_pos()
                x, y = move
                new_point = convert_to_point(x, y)
                try:
                    if chessgame.move_piece(point, new_point):
                        if type(piece) in pieces:
                            screen.blit(pieces[type(piece)], (28 + new_point.x * 106, 904 - 28 - 106 - new_point.y * 106))
                        else:
                            print(f"Error: Piece type {type(piece)} not found in pieces dictionary.")
                except GameOverException as ex:
                    show_checkmate_message()
                    running = False
                except CheckException as ex:
                    show_check_message()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
pygame.quit()
