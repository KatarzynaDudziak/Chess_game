import unittest
from unittest.mock import MagicMock
from pawns import *
from point import Point
from move_handler import MoveHandler
from board import EMPTY_SQUARE


class TestMoveHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.board = MagicMock()
        self.move_handler = MoveHandler(self.board)
        
    def test_pawn_should_not_move_if_it_is_not_players_turn(self):
        self.board.get_piece_at_the_position = MagicMock(return_value=BlackPawn())
        self.board.execute_move = MagicMock()
    
        self.assertFalse(self.move_handler.move_piece(Point(0, 0), Point(1, 1), MagicMock(return_value=Color.WHITE), MagicMock(), MagicMock()))
        self.board.execute_move.assert_not_called()

    def test_pawn_should_not_move_if_it_is_not_valid(self):
        self.board.get_piece_at_the_position = MagicMock(return_value=BlackPawn())
        self.board.execute_move = MagicMock()
        self.move_handler.is_move_valid = MagicMock(return_value=False)

        self.assertFalse(self.move_handler.move_piece(Point(0, 0), Point(1, 1), MagicMock(return_value=Color.BLACK), MagicMock(), MagicMock()))
        self.board.execute_move.assert_not_called()

    def test_pawn_should_move_if_it_is_valid(self):
        self.board.get_piece_at_the_position = MagicMock(return_value=BlackPawn())
        self.board.execute_move = MagicMock()
        self.move_handler.is_move_valid = MagicMock(return_value=True)

        self.assertTrue(self.move_handler.move_piece(Point(0, 0), Point(1, 1), MagicMock(return_value=Color.BLACK), MagicMock(), MagicMock()))
        self.board.execute_move.assert_called_once_with(BlackPawn(), Point(0, 0), Point(1, 1))

    def test_pawn_should_not_move_if_cannot(self):
        pawn = BlackPawn()
        pawn.can_move = MagicMock(return_value=False)
        self.move_handler.is_piece_move_valid = MagicMock()

        self.assertFalse(self.move_handler.is_move_valid(pawn, Point(0, 0), Point(1, 1), MagicMock(), MagicMock(return_value=Color.BLACK)))
        self.move_handler.is_piece_move_valid.assert_not_called()

    def test_pawn_should_not_move_if_target_is_not_empty(self):
        pawn = BlackPawn()
        pawn.can_move = MagicMock(return_value=True)
        self.board.board = [[EMPTY_SQUARE, EMPTY_SQUARE], [EMPTY_SQUARE, BlackPawn()]]
        self.move_handler.is_piece_move_valid = MagicMock()

        self.assertFalse(self.move_handler.is_move_valid(pawn, Point(0, 0), Point(1, 1), MagicMock(), MagicMock(return_value=Color.BLACK)))
        self.move_handler.is_piece_move_valid.assert_not_called()

    def test_should_return_true_if_move_is_valid(self):
        pawn = BlackPawn()
        pawn.can_move = MagicMock(return_value=True)
        self.board.board = [[EMPTY_SQUARE, EMPTY_SQUARE], [EMPTY_SQUARE, EMPTY_SQUARE]]
        self.move_handler.is_piece_move_valid = MagicMock(return_value=True)

        self.assertTrue(self.move_handler.is_move_valid(pawn, Point(0, 0), Point(1, 1), MagicMock(), MagicMock(return_value=Color.BLACK)))

    def test_piece_move_should_be_valid_if_is_knight(self):
        pawn = BlackKnight()
        self.board.is_simulated_action_valid = MagicMock(return_value=True)
        self.assertTrue(self.move_handler.is_piece_move_valid(pawn, Point(0, 0), Point(2, 1), MagicMock(), MagicMock()))

    def test_piece_move_should_be_valid_if_path_is_clear(self):
        pawn = Pawn()
        self.board.is_path_clear = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=True)
        self.assertTrue(self.move_handler.is_piece_move_valid(pawn, Point(0, 0), Point(2, 1), MagicMock(), MagicMock()))

    def test_piece_move_should_not_be_valid_if_path_is_not_clear(self):
        pawn = Pawn()
        self.board.is_path_clear = MagicMock(return_value=False)
        self.assertFalse(self.move_handler.is_piece_move_valid(pawn, Point(0, 0), Point(2, 1), MagicMock(), MagicMock()))

    def test_should_return_false_if_simulated_move_is_not_valid(self):
        pawn = Pawn()
        self.board.is_path_clear = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=False)
        self.assertFalse(self.move_handler.is_piece_move_valid(pawn, Point(0, 0), Point(2, 1), MagicMock(), MagicMock()))

    def test_should_not_be_valid_if_pawn_is_none(self):
        self.assertFalse(self.move_handler.is_piece_move_valid(None, Point(0, 0), Point(2, 1), MagicMock(), MagicMock()))
