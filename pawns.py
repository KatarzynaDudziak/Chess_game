from typing import Any, Callable
from point import Point
from enum import Enum


class Color(Enum):
    WHITE = "white",
    BLACK = "black"


class Pawn:
    def __init__(self):
        self.color = None

    def __eq__(self, other):
        if isinstance(other, Pawn):
            return self.color == other.color
        return False

    def __hash__(self):
        return hash(self.color)

    def __str__(self):
        return

    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return is_moving_forward_one_square(self.color, current_pos, new_pos) or is_moving_forward_two_squares(self.color, current_pos, new_pos)

    def can_capture(self, current_pos: Point, new_pos: Point) -> bool:
        return False


class WhitePawn(Pawn):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WP "
    
    def can_capture(self, current_pos: Point, new_pos: Point) -> bool:
        return new_pos.y == current_pos.y + 1 and abs(new_pos.x - current_pos.x) == 1


class BlackPawn(Pawn):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BP "
    
    def can_capture(self, current_pos: Point, new_pos: Point) -> bool:
        return new_pos.y == current_pos.y - 1 and abs(new_pos.x - current_pos.x) == 1


class Bishop(Pawn):
    def __init__(self):
        super().__init__()
    
    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return is_moving_diagonally(current_pos, new_pos)

    def can_capture(self, current_pos: Point, new_pos: Point) -> bool:
        return is_moving_diagonally(current_pos, new_pos)


class WhiteBishop(Bishop):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WB "

class BlackBishop(Bishop):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BB "


class Rook(Pawn):
    def __init__(self):
        super().__init__()

    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return is_moving_sideways(current_pos, new_pos) or is_moving_forward(self.color, current_pos, new_pos)

    def can_capture(self, current_pos: Point, new_pos: Point):
        return self.can_move(current_pos, new_pos)


class WhiteRook(Rook):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WR "


class BlackRook(Rook):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BR "


class Knight(Pawn):
    def __init__(self):
        super().__init__()

    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return (abs(new_pos.x - current_pos.x) == 2 and abs(new_pos.y - current_pos.y) == 1) or (abs(new_pos.x - current_pos.x) == 1 and abs(new_pos.y - current_pos.y) == 2)

    def can_capture(self, current_pos: Point, new_pos: Point) -> bool:
        return self.can_move(current_pos, new_pos)


class WhiteKnight(Knight):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WKn"


class BlackKnight(Knight):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BKn"


class Queen(Pawn):
    def __init__(self):
        super().__init__()

    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return is_moving_diagonally(current_pos, new_pos) or is_moving_forward(self.color, current_pos, new_pos) or is_moving_sideways(current_pos, new_pos)

    def can_capture(self, current_pos: Point, new_pos: Point):
        return self.can_move(current_pos, new_pos)


class WhiteQueen(Queen):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WQ "


class BlackQueen(Queen):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BQ "


class King(Pawn):
    def __init__(self):
        super().__init__()
      
    def can_move(self, current_pos: Point, new_pos: Point) -> bool:
        return abs(new_pos.x - current_pos.x) <= 1 and abs(new_pos.y - current_pos.y) <= 1

    def can_capture(self, current_pos: Point, new_pos: Point):
        self.can_move(current_pos, new_pos)


class WhiteKing(King):
    def __init__(self):
        super().__init__()
        self.color = Color.WHITE

    def __str__(self):
        return "WK "


class BlackKing(King):
    def __init__(self):
        super().__init__()
        self.color = Color.BLACK

    def __str__(self):
        return "BK "


def is_moving_diagonally(current_pos: Point, new_pos: Point):
    return abs(new_pos.x - current_pos.x) == abs(new_pos.y - current_pos.y)

def is_moving_forward_one_square(color: Callable[[Enum], Any], current_pos: Point, new_pos: Point) -> bool:
    if color == Color.WHITE:
        return new_pos.y == current_pos.y + 1 and new_pos.x == current_pos.x
    elif color == Color.BLACK:
        return new_pos.y == current_pos.y - 1 and new_pos.x == current_pos.x
    return False


def is_moving_forward_two_squares(color: Callable[[Enum], Any], current_pos: Point, new_pos: Point) -> bool:
    if color == Color.WHITE:
        return current_pos.y == 1 and new_pos.y == current_pos.y + 2 and new_pos.x == current_pos.x
    elif color == Color.BLACK:
        return current_pos.y == 6 and new_pos.y == current_pos.y - 2 and new_pos.x == current_pos.x
    return False


def is_moving_forward(color: str, current_pos: Point, new_pos: Point) -> bool:
    if color == Color.WHITE:
        return new_pos.y > current_pos.y and new_pos.x == current_pos.x
    elif color == Color.BLACK:
        return new_pos.y < current_pos.y and new_pos.x == current_pos.x
    return False


def is_moving_sideways(current_pos: Point, new_pos: Point) -> bool:
    return new_pos.y == current_pos.y and new_pos.x != current_pos.x
