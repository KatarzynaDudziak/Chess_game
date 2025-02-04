from parameterized import parameterized
import sys
sys.path.append("..")
import unittest
from pawns import *
from point import Point


class TestPawn(unittest.TestCase):
    @parameterized.expand([
        ("white", Point(1, 1), Point(1, 2), True),
        ("black", Point(1, 6), Point(1, 5), True),
        ("white", Point(1, 1), Point(1, 3), True),
        ("black", Point(1, 6), Point(1, 4), True),
    ])

    def test_pawn_can_take_one_or_two_steps_forward(self, color: str, current_pos: Point, new_pos: Point, expected: bool):
        self.assertEqual(Pawn(color).can_move(current_pos, new_pos), expected)

    @parameterized.expand([
        ("white", Point(1, 1), Point(1, 0), False),
        ("black", Point(1, 6), Point(1, 7), False),
        ("white", Point(1, 1), Point(2, 1), False),
        ("black", Point(1, 6), Point(2, 6), False),
        ("white", Point(1, 1), Point(2, 2), False),
        ("black", Point(1, 6), Point(2, 5), False),
        ("white", Point(1, 2), Point(1, 4), False),
        ("black", Point(1, 5), Point(1, 3), False),
        ("white", Point(1, 1), Point(3, 1), False),
        ("black", Point(1, 6), Point(3, 6), False),
        ("white", Point(1, 1), Point(3, 3), False),
        ("black", Point(1, 6), Point(3, 4), False),
        ("white", Point(1, 1), Point(1, 4), False),
        ("black", Point(1, 6), Point(1, 3), False),
    ])

    def test_pawn_cannot_move_diagonally_or_sideways_or_take_more_steps_than_two(
        self, color: str, current_pos: Point, new_pos: Point, expected: bool):
        self.assertEqual(Pawn(color).can_move(current_pos, new_pos), expected)

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
    pass