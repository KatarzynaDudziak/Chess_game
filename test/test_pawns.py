from parameterized import parameterized # type: ignore
from typing import Callable, Any
from enum import Enum
import sys
sys.path.append("..")
import unittest
from pawns import *
from point import Point


class TestPawn(unittest.TestCase):
    pawn_valid_moves = [
        (WhitePawn, Point(1, 1), Point(1, 2)),      # one step forward
        (WhitePawn, Point(1, 1), Point(1, 3)),      # two steps forward
        (BlackPawn, Point(1, 6), Point(1, 5)),      # one step forward
        (BlackPawn, Point(1, 6), Point(1, 4)),      # two steps forward
    ]

    @parameterized.expand(pawn_valid_moves)
    def test_valid_move_for_pawn(self, pawn,  current_pos: Point, new_pos: Point):
        self.assertTrue(pawn().can_move(current_pos, new_pos))

    pawn_invalid_moves = [
        (WhitePawn, Point(1, 1), Point(1, 0)),     # backward
        (WhitePawn, Point(1, 1), Point(2, 1)),     # sideways
        (WhitePawn, Point(1, 1), Point(2, 2)),     # diagonal right
        (WhitePawn, Point(1, 2), Point(1, 4)),     # two steps forward
        (WhitePawn, Point(1, 1), Point(3, 1)),     # sideways
        (WhitePawn, Point(1, 1), Point(3, 3)),     # diagonal right
        (WhitePawn, Point(1, 1), Point(1, 4)),     # three steps forward
        (BlackPawn, Point(1, 6), Point(1, 7)),     # backward
        (BlackPawn, Point(1, 6), Point(2, 6)),     # sideways
        (BlackPawn, Point(1, 6), Point(2, 5)),     # diagonal right
        (BlackPawn, Point(1, 5), Point(1, 3)),     # two steps forward
        (BlackPawn, Point(1, 6), Point(3, 6)),     # sideways
        (BlackPawn, Point(1, 6), Point(3, 4)),     # diagonal right
        (BlackPawn, Point(1, 6), Point(1, 3)),     # three steps forward
    ]

    @parameterized.expand(pawn_invalid_moves)
    def test_invalid_move_for_pawn(self, pawn, current_pos: Point, new_pos: Point):
        self.assertFalse(pawn().can_move(current_pos, new_pos))

    def test_white_pawn_cannot_move_forward_two_squares_after_moving(self):
        current_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.assertTrue(WhitePawn().can_move(current_pos, new_pos))
        self.assertFalse(WhitePawn().can_move(new_pos, Point(1, 4)))

    def test_black_pawn_cannot_move_forward_two_squares_after_moving(self):
        current_pos = Point(1, 6)
        new_pos = Point(1, 5)
        self.assertTrue(BlackPawn().can_move(current_pos, new_pos))
        self.assertFalse(BlackPawn().can_move(new_pos, Point(1, 3)))

    pawn_valid_captures = [
        (WhitePawn, Point(1, 1), Point(0, 2)),      # capture left
        (WhitePawn, Point(1, 1), Point(2, 2)),      # capture right
        (BlackPawn, Point(1, 6), Point(0, 5)),      # capture left
        (BlackPawn, Point(1, 6), Point(2, 5)),      # capture right
    ]

    @parameterized.expand(pawn_valid_captures)
    def test_valid_capture_for_pawn(self, pawn, current_pos: Point, new_pos: Point):
        self.assertTrue(pawn().can_capture(current_pos, new_pos))

    pawn_invalid_captures = [
        (WhitePawn, Point(1, 1), Point(0, 1)),     # forward
        (WhitePawn, Point(1, 1), Point(1, 2)),     # forward
        (BlackPawn, Point(1, 6), Point(0, 6)),     # forward
        (BlackPawn, Point(1, 6), Point(1, 5)),     # forward
    ]

    @parameterized.expand(pawn_invalid_captures)
    def test_invalid_capture_for_pawn(self, pawn, current_pos: Point, new_pos: Point):
        self.assertFalse(pawn().can_capture(current_pos, new_pos))


class TestBishop(unittest.TestCase):
    bishop_valid_moves = [
        (WhiteBishop, Point(2, 0), Point(3, 1)),      # diagonally right
        (WhiteBishop, Point(2, 0), Point(1, 1)),      # diagonally left
        (WhiteBishop, Point(4, 2), Point(2, 0)),      # backward left diagonal
        (BlackBishop, Point(2, 7), Point(3, 6)),      # diagonally right
        (BlackBishop, Point(2, 7), Point(1, 6)),      # diagonally left
        (BlackBishop, Point(4, 5), Point(2, 7)),      # backward left diagonal
    ]

    @parameterized.expand(bishop_valid_moves)
    def test_valid_move_for_bishop(self, bishop, current_pos: Point, new_pos: Point):
        self.assertTrue(bishop().can_move(current_pos, new_pos))

    @parameterized.expand(bishop_valid_moves)
    def test_valid_capture_for_bishop(self, bishop, current_pos: Point, new_pos: Point):
        self.assertTrue(bishop().can_capture(current_pos, new_pos))

    bishop_invalid_moves = [
        (WhiteBishop, Point(2, 0), Point(2, 1)),     # forward
        (WhiteBishop, Point(2, 0), Point(3, 0)),     # sideways right
        (WhiteBishop, Point(2, 0), Point(1, 0)),     # sideways left
        (WhiteBishop, Point(2, 2), Point(2, 0)),     # backward
        (BlackBishop, Point(2, 7), Point(2, 6)),     # forward
        (BlackBishop, Point(2, 7), Point(3, 7)),     # sideways right
        (BlackBishop, Point(2, 7), Point(1, 7)),     # sideways left
        (BlackBishop, Point(2, 5), Point(2, 7)),     # backward
    ]

    @parameterized.expand(bishop_invalid_moves)
    def test_invalid_move_for_bishop(self, bishop, current_pos: Point, new_pos: Point):
        self.assertFalse(bishop().can_move(current_pos, new_pos))

    @parameterized.expand(bishop_invalid_moves)
    def test_invalid_capture_for_bishop(self, bishop, current_pos: Point, new_pos: Point):
        self.assertFalse(bishop().can_capture(current_pos, new_pos))


class TestRook(unittest.TestCase):
    rook_valid_moves = [
        (WhiteRook, Point(0, 0), Point(0, 1)),      # one step
        (WhiteRook, Point(0, 0), Point(0, 7)),      # seven steps forward
        (WhiteRook, Point(0, 0), Point(7, 0)),      # seven steps right
        (BlackRook, Point(0, 7), Point(0, 6)),      # one step
        (BlackRook, Point(0, 7), Point(0, 0)),      # seven steps forward
        (BlackRook, Point(0, 7), Point(7, 7)),      # seven steps right
    ]

    @parameterized.expand(rook_valid_moves)
    def test_valid_move_for_rook(self, rook, current_pos: Point, new_pos: Point):
        self.assertTrue(rook().can_move(current_pos, new_pos))

    @parameterized.expand(rook_valid_moves)
    def test_valid_capture_for_rook(self, rook, current_pos: Point, new_pos: Point):
        self.assertTrue(rook().can_capture(current_pos, new_pos))

    rook_invalid_moves = [
        (WhiteRook, Point(0, 0), Point(1, 1)),     # diagonal
        (WhiteRook, Point(4, 0), Point(6, 2)),     # diagonal
        (BlackRook, Point(0, 7), Point(1, 6)),     # diagonal
        (BlackRook, Point(4, 7), Point(6, 5)),     # diagonal
    ]

    @parameterized.expand(rook_invalid_moves)
    def test_invalid_move_for_rook(self, rook, current_pos: Point, new_pos: Point):
        self.assertFalse(rook().can_move(current_pos, new_pos))

    @parameterized.expand(rook_invalid_moves)
    def test_invalid_capture_for_rook(self, rook, current_pos: Point, new_pos: Point):
        self.assertFalse(rook().can_capture(current_pos, new_pos))


class TestKnight(unittest.TestCase):
    knight_valid_moves = [
        (WhiteKnight, Point(1, 0), Point(2, 2)),      # L shape
        (WhiteKnight, Point(1, 0), Point(0, 2)),      # L shape
        (WhiteKnight, Point(3, 1), Point(1, 2)),      # L shape backward
        (BlackKnight, Point(1, 7), Point(2, 5)),      # L shape
        (BlackKnight, Point(1, 7), Point(0, 5)),      # L shape
        (BlackKnight, Point(3, 6), Point(1, 5)),      # L shape backward
    ]

    @parameterized.expand(knight_valid_moves)
    def test_valid_move_for_knight(self, knight, current_pos: Point, new_pos: Point):
        self.assertTrue(knight().can_move(current_pos, new_pos))

    @parameterized.expand(knight_valid_moves)
    def test_valid_capture_for_knight(self, knight, current_pos: Point, new_pos: Point):
        self.assertTrue(knight().can_capture(current_pos, new_pos))

    knight_invalid_moves = [
        (WhiteKnight, Point(1, 0), Point(1, 1)),     # forward one step
        (WhiteKnight, Point(1, 0), Point(2, 0)),     # sideways one step
        (WhiteKnight, Point(1, 0), Point(1, 2)),     # forward two steps
        (WhiteKnight, Point(1, 0), Point(5, 4)),     # diagoanal
        (BlackKnight, Point(1, 7), Point(1, 6)),     # forward one step
        (BlackKnight, Point(1, 7), Point(2, 7)),     # sideways one step
        (BlackKnight, Point(1, 7), Point(1, 5)),     # forward two steps
        (BlackKnight, Point(1, 7), Point(5, 3)),     # diagoanal
    ]

    @parameterized.expand(knight_invalid_moves)
    def test_invalid_move_for_knight(self, knight, current_pos: Point, new_pos: Point):
       self.assertFalse(knight().can_move(current_pos, new_pos))

    @parameterized.expand(knight_invalid_moves)
    def test_invalid_capture_for_knight(self, knight, current_pos: Point, new_pos: Point):
        self.assertFalse(knight().can_capture(current_pos, new_pos))


class TestQueen(unittest.TestCase):
    queen_valid_moves = [
        (WhiteQueen, Point(3, 0), Point(3, 1)),      # one step forward
        (WhiteQueen, Point(3, 0), Point(4, 1)),      # right diagonal
        (WhiteQueen, Point(3, 0), Point(3, 7)),      # seven steps forward
        (WhiteQueen, Point(3, 0), Point(7, 0)),      # seven steps right
        (BlackQueen, Point(3, 7), Point(3, 6)),      # one step
        (BlackQueen, Point(3, 7), Point(4, 6)),      # right diagonal
        (BlackQueen, Point(3, 7), Point(3, 0)),      # seven steps forward
        (BlackQueen, Point(7, 7), Point(0, 7)),      # seven steps left
    ]

    @parameterized.expand(queen_valid_moves)
    def test_valid_move_for_queen(self, queen, current_pos: Point, new_pos: Point):
        self.assertTrue(queen().can_move(current_pos, new_pos))

    @parameterized.expand(queen_valid_moves)
    def test_valid_capture_for_queen(self, queen, current_pos: Point, new_pos: Point):
        self.assertTrue(queen().can_capture(current_pos, new_pos))


class TestKing(unittest.TestCase):
    king_valid_moves = [
        (WhiteKing, Point(4, 0), Point(4, 1)),      # one step
        (WhiteKing, Point(3, 1), Point(4, 0)),      # backward left diagonal 
        (BlackKing, Point(4, 7), Point(4, 6)),      # one step
        (BlackKing, Point(3, 6), Point(4, 7)),      # backward left diagonal
    ]

    @parameterized.expand(king_valid_moves)
    def test_valid_move_for_king(self, king, current_pos: Point, new_pos: Point):
        self.assertTrue(king().can_move(current_pos, new_pos))

    @parameterized.expand(king_valid_moves)
    def test_valid_capture_for_king(self, king, current_pos: Point, new_pos: Point):
        self.assertTrue(king().can_capture(current_pos, new_pos))

    king_invalid_moves = [
        (WhiteKing, Point(4, 0), Point(4, 2)),     # two steps
        (WhiteKing, Point(4, 0), Point(4, 4)),     # three steps
        (WhiteKing, Point(4, 0), Point(4, 7)),     # seven steps
        (BlackKing, Point(4, 7), Point(4, 5)),     # two steps
        (BlackKing, Point(4, 7), Point(4, 3)),     # three steps
        (BlackKing, Point(4, 7), Point(4, 0)),     # seven steps
    ]

    @parameterized.expand(king_invalid_moves)
    def test_invalid_move_for_king(self, king, current_pos: Point, new_pos: Point):
        self.assertFalse(king().can_move(current_pos, new_pos))

    @parameterized.expand(king_invalid_moves)
    def test_invalid_capture_for_king(self, king, current_pos: Point, new_pos: Point):
        self.assertFalse(king().can_capture(current_pos, new_pos))
