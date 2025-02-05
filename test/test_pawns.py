from parameterized import parameterized # type: ignore
import sys
sys.path.append("..")
import unittest
from pawns import Pawn, Bishop, King, Rook, Knight, Queen
from point import Point


class TestPawn(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(1, 1), Point(1, 2)),      # one step forward
        ("white", Point(1, 1), Point(1, 3)),      # two steps forward
        ("black", Point(1, 6), Point(1, 5)),      # one step forward
        ("black", Point(1, 6), Point(1, 4)),      # two steps forward
    ])

    def test_valid_move_for_pawn(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(Pawn(color).can_move(current_pos, new_pos))

    @parameterized.expand([
        ("white", Point(1, 1), Point(1, 0)),     # backward
        ("white", Point(1, 1), Point(2, 1)),     # sideways
        ("white", Point(1, 1), Point(2, 2)),     # diagonal right
        ("white", Point(1, 2), Point(1, 4)),     # two steps forward
        ("white", Point(1, 1), Point(3, 1)),     # sideways
        ("white", Point(1, 1), Point(3, 3)),     # diagonal right
        ("white", Point(1, 1), Point(1, 4)),     # three steps forward
        ("black", Point(1, 6), Point(1, 7)),     # backward
        ("black", Point(1, 6), Point(2, 6)),     # sideways
        ("black", Point(1, 6), Point(2, 5)),     # diagonal right
        ("black", Point(1, 5), Point(1, 3)),     # two steps forward
        ("black", Point(1, 6), Point(3, 6)),     # sideways
        ("black", Point(1, 6), Point(3, 4)),     # diagonal right
        ("black", Point(1, 6), Point(1, 3)),     # three steps forward
    ])

    def test_invalid_move_for_pawn(self, color: str, current_pos: Point, new_pos: Point):
        self.assertFalse(Pawn(color).can_move(current_pos, new_pos))

    def test_white_pawn_cannot_move_forward_two_squares_after_moving(self):
        current_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.assertTrue(Pawn("white").can_move(current_pos, new_pos))
        self.assertFalse(Pawn("white").can_move(new_pos, Point(1, 4)))

    def test_black_pawn_cannot_move_forward_two_squares_after_moving(self):
        current_pos = Point(1, 6)
        new_pos = Point(1, 5)
        self.assertTrue(Pawn("black").can_move(current_pos, new_pos))
        self.assertFalse(Pawn("black").can_move(new_pos, Point(1, 3)))


class TestBishop(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(2, 0), Point(3, 1)),      # diagonally right
        ("white", Point(2, 0), Point(1, 1)),      # diagonally left
        ("white", Point(4, 2), Point(2, 0)),      # backward left diagonal
        ("black", Point(2, 7), Point(3, 6)),      # diagonally right
        ("black", Point(2, 7), Point(1, 6)),      # diagonally left
        ("black", Point(4, 5), Point(2, 7)),      # backward left diagonal
    ])

    def test_valid_move_for_bishop(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(Bishop(color).can_move(current_pos, new_pos))

    @parameterized.expand([
        ("white", Point(2, 0), Point(2, 1)),     # forward
        ("white", Point(2, 0), Point(3, 0)),     # sideways right
        ("white", Point(2, 0), Point(1, 0)),     # sideways left
        ("white", Point(2, 2), Point(2, 0)),     # backward
        ("black", Point(2, 7), Point(2, 6)),     # forward
        ("black", Point(2, 7), Point(3, 7)),     # sideways right
        ("black", Point(2, 7), Point(1, 7)),     # sideways left
        ("black", Point(2, 5), Point(2, 7)),     # backward
    ])

    def test_invalid_move_for_bishop(self, color: str, current_pos: Point, new_pos: Point):
        self.assertFalse(Bishop(color).can_move(current_pos, new_pos))


class TestRook(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(0, 0), Point(0, 1)),      # one step
        ("white", Point(0, 0), Point(0, 7)),      # seven steps forward
        ("white", Point(0, 0), Point(7, 0)),      # seven steps right
        ("black", Point(0, 7), Point(0, 6)),      # one step
        ("black", Point(0, 7), Point(0, 0)),      # seven steps forward
        ("black", Point(0, 7), Point(7, 7)),      # seven steps right
    ])

    def test_valid_move_for_rook(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(Rook(color).can_move(current_pos, new_pos))

    @parameterized.expand([
        ("white", Point(0, 0), Point(1, 1)),     # diagonal
        ("white", Point(4, 0), Point(6, 2)),     # diagonal
        ("black", Point(0, 7), Point(1, 6)),     # diagonal
        ("black", Point(4, 7), Point(6, 5)),     # diagonal
    ])

    def test_invalid_move_for_rook(self, color: str, current_pos: Point, new_pos: Point):
        self.assertFalse(Rook(color).can_move(current_pos, new_pos))


class TestKnight(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(1, 0), Point(2, 2)),      # L shape
        ("white", Point(1, 0), Point(0, 2)),      # L shape
        ("white", Point(3, 1), Point(1, 2)),      # L shape backward
        ("black", Point(1, 7), Point(2, 5)),      # L shape
        ("black", Point(1, 7), Point(0, 5)),      # L shape
        ("black", Point(3, 6), Point(1, 5)),      # L shape backward
    ])

    def test_valid_move_for_knight(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(Knight(color).can_move(current_pos, new_pos))

    @parameterized.expand([
        ("white", Point(1, 0), Point(1, 1)),     # forward one step
        ("white", Point(1, 0), Point(2, 0)),     # sideways one step
        ("white", Point(1, 0), Point(1, 2)),     # forward two steps
        ("white", Point(1, 0), Point(5, 4)),     # diagoanal
        ("black", Point(1, 7), Point(1, 6)),     # forward one step
        ("black", Point(1, 7), Point(2, 7)),     # sideways one step
        ("black", Point(1, 7), Point(1, 5)),     # forward two steps
        ("black", Point(1, 7), Point(5, 3)),     # diagoanal
    ])

    def test_invalid_move_for_knight(self, color: str, current_pos: Point, new_pos: Point):
       self.assertFalse(Knight(color).can_move(current_pos, new_pos))


class TestQueen(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(3, 0), Point(3, 1)),      # one step forward
        ("white", Point(3, 0), Point(4, 1)),      # right diagonal
        ("white", Point(3, 0), Point(3, 7)),      # seven steps forward
        ("white", Point(3, 0), Point(7, 0)),      # seven steps right
        ("black", Point(3, 7), Point(3, 6)),      # one step
        ("black", Point(3, 7), Point(4, 6)),      # right diagonal
        ("black", Point(3, 7), Point(3, 0)),      # seven steps forward
        ("black", Point(7, 7), Point(0, 7)),      # seven steps left
    ])

    def test_valid_move_for_queen(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(Queen(color).can_move(current_pos, new_pos))


class TestKing(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(4, 0), Point(4, 1)),      # one step
        ("white", Point(3, 1), Point(4, 0)),      # backward left diagonal 
        ("black", Point(4, 7), Point(4, 6)),      # one step
        ("black", Point(3, 6), Point(4, 7)),      # backward left diagonal
    ])

    def test_valid_move_for_king(self, color: str, current_pos: Point, new_pos: Point):
        self.assertTrue(King(color).can_move(current_pos, new_pos))

    @parameterized.expand([
        ("white", Point(4, 0), Point(4, 2)),     # two steps
        ("white", Point(4, 0), Point(4, 4)),     # three steps
        ("white", Point(4, 0), Point(4, 7)),     # seven steps
        ("black", Point(4, 7), Point(4, 5)),     # two steps
        ("black", Point(4, 7), Point(4, 3)),     # three steps
        ("black", Point(4, 7), Point(4, 0)),     # seven steps
    ])

    def test_invalid_move_for_king(self, color: str, current_pos: Point, new_pos: Point):
        self.assertFalse(King(color).can_move(current_pos, new_pos))
