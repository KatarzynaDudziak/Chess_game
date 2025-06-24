import utils
from point import Point
from chess_engine import *
from chess_engine import ChessEngine
from game_over_exception import GameOverException

logger = utils.get_logger(__name__)


class ConsoleChess:
    def __init__(self) -> None:
        self.engine = ChessEngine()
        self.board = self.engine.get_board()

    def draw_board(self) -> str:
        board_str = ""
        for row in reversed(self.board):
            board_str += "".join([f"|{pawn.__str__()}|" if isinstance(pawn, Pawn) else "|__ |" for pawn in row]) + "\n"
        return board_str

    def run(self) -> None:
        while True:
            try:
                print(f"{self.engine.check_whose_turn()} turn")
                print(self.draw_board())
                move = input("Enter move (e.g., '12 34'): ")
                current_pos, new_pos = move.split(" ")
                current_pos = Point(int(current_pos[0]), int(current_pos[1]))
                new_pos = Point(int(new_pos[0]), int(new_pos[1]))
                if self.engine.move_piece(current_pos, new_pos):
                    logger.info("Correct move")
            except GameOverException as e:
                print(e)
                break
            except (ValueError, IndexError):
                logger.warning("Invalid input. Please enter the move in the format '12 34'.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")


def main():
    console_chess = ConsoleChess()
    console_chess.run()


if __name__ == "__main__":
    main()
