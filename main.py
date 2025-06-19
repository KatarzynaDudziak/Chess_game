from point import Point
from chess_engine import *


def main():
    game  = ChessEngine()
    board = game.board
    while True:
        try:
            print(f"{game.__check_whose_turn()} turn")
            print(board)
            move = input("Enter move (e.g., '12 34'): ")
            current_pos, new_pos = move.split(" ")
            current_pos = Point(int(current_pos[0]), int(current_pos[1]))
            new_pos = Point(int(new_pos[0]), int(new_pos[1]))
            if game.move_piece(current_pos, new_pos):
                print("Correct move")
        except GameOverException as e:
            print(e)
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter the move in the format '12 34'.")
        except Exception as e:
            print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()
