from point import Point
from pawns import Color
from chessgame import *


def main():
    game  = ChessGame()
    board = game.board
    checkmate = False
    while not checkmate:
        try:
            print(f"{game.check_whose_turn()} turn")
            print(board)
            move = input("Enter move (e.g., '12 34'): ")
            current_pos, new_pos = move.split(" ")
            current_pos = Point(int(current_pos[0]), int(current_pos[1]))
            new_pos = Point(int(new_pos[0]), int(new_pos[1]))
            if game.move_piece(current_pos, new_pos):
                checkmate = game.is_checkmate(board.white_pawns if Color == Color.WHITE else board.black_pawns)
                if checkmate:
                    logger.info("Checkmate! Game over!")
                    print("Checkmate! Game over!")
                    break
        except (ValueError, IndexError):
            print("Invalid input. Please enter the move in the format '12 34'.")
        except Exception as e:
            print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()
