import unittest
from chess_engine import ChessEngine
from pawns import *
from unittest.mock import MagicMock
from board import EMPTY_SQUARE
from game_over_exception import GameOverException


class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game = ChessEngine()
        self.game.board = MagicMock()
        self.game.move_handler = MagicMock()
        self.game.check_handler = MagicMock()
        self.game.capture_handler = MagicMock()

    def test_move_piece_should_return_true_when_the_move_is_valid(self):
        self.game.move_handler.move_piece = MagicMock(return_value=True)
        self.game.capture_handler.__is_capture_valid = MagicMock()
        self.game.is_check = MagicMock()
        self.game.__check_whose_turn = MagicMock()
        self.game.is_check = MagicMock()
        self.game.__switch_turn = MagicMock()

        self.assertTrue(self.game.move_piece((0, 0), (1, 1)))

        self.game.capture_handler.__is_capture_valid.assert_not_called()
        self.game.is_check.assert_not_called()
        self.game.move_handler.move_piece.assert_called_once_with((0, 0), (1, 1),
                                                                   self.game.__check_whose_turn,
                                                                   self.game.is_check,
                                                                   self.game.__switch_turn)
    
    def test_capture_should_happen_when_move_is_invalid_and_capture_is_valid(self):
        self.game.move_handler.move_piece = MagicMock(return_value=False)
        self.game.capture_handler.__is_capture_valid = MagicMock(return_value=True)
        self.game.is_check = MagicMock()

        self.assertTrue(self.game.move_piece((0, 0), (1, 1)))

        self.game.is_check.assert_not_called()
        self.game.capture_handler.__is_capture_valid.assert_called_once_with(self.game.board.get_piece_at_the_position((0, 0)),
                                                                            (0, 0), (1, 1), self.game.is_check,
                                                                            self.game.__check_whose_turn)
        
    def test_switch_turn_should_be_called_when_move_is_invalid_and_capture_is_invalid(self):
        self.game.move_handler.move_piece = MagicMock(return_value=False)
        self.game.capture_handler.__is_capture_valid = MagicMock(return_value=False)
        self.game.capture_handler.capture = MagicMock()
        self.game.is_check = MagicMock(return_value=True)
        self.game.__switch_turn = MagicMock()

        self.assertTrue(self.game.move_piece((0, 0), (1, 1)))

        self.game.__switch_turn.assert_called_once()
        self.game.capture_handler.capture.assert_not_called()

    def test_check_whose_turn_should_return_WHITE_when_the_number_of_movements_is_even(self):
        self.game.board.movements_history = [(0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertEqual(self.game.__check_whose_turn(), Color.WHITE)

    def test_check_whose_turn_should_return_BLACK_when_the_number_of_movements_is_odd(self):
        self.game.board.movements_history = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(self.game.__check_whose_turn(), Color.BLACK)

    def test_is_check_should_return_false_when_there_is_no_check(self):
        self.game.check_handler.get_checked_king_color = MagicMock(return_value=False)
        self.game.__check_whose_turn = MagicMock()
        self.game.check_handler.is_checkmate = MagicMock()

        self.assertFalse(self.game.is_check(self.game.__check_whose_turn))

        self.game.check_handler.get_checked_king_color.assert_called_once_with(self.game.__check_whose_turn)
        self.game.check_handler.is_checkmate.assert_not_called()

    def test_is_check_should_raise_GameOverException_when_there_is_checkmate(self):
        self.game.check_handler.get_checked_king_color = MagicMock(return_value=True)
        self.game.__check_whose_turn = MagicMock()
        self.game.check_handler.is_checkmate = MagicMock(return_value=True)

        self.assertRaises(GameOverException, self.game.is_check, self.game.__check_whose_turn)

        self.game.check_handler.get_checked_king_color.assert_called_once_with(self.game.__check_whose_turn)
        self.game.check_handler.is_checkmate.assert_called_once_with(self.game.board.white_pawns,
                                                                    self.game.__check_whose_turn)
        
    def test_is_check_should_return_true_when_there_is_check(self):
        self.game.check_handler.get_checked_king_color = MagicMock(return_value=True)
        self.game.__check_whose_turn = MagicMock()
        self.game.check_handler.is_checkmate = MagicMock(return_value=False)

        self.assertTrue(self.game.is_check(self.game.__check_whose_turn))

        self.game.check_handler.get_checked_king_color.assert_called_once_with(self.game.__check_whose_turn)
        self.game.check_handler.is_checkmate.assert_called_once_with(self.game.board.white_pawns,
                                                                    self.game.__check_whose_turn)
        
    def test_is_checkmate_should_return_true_when_the_opponent_is_in_checkmate(self):
        self.game.__check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.check_handler.is_checkmate = MagicMock(return_value=True)

        self.assertTrue(self.game.__is_checkmate(self.game.board.black_pawns))
    
    def test_is_checkmate_should_return_false_when_the_opponent_is_not_in_checkmate(self):
        self.game.__check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.check_handler.is_checkmate = MagicMock(return_value=False)

        self.assertFalse(self.game.__is_checkmate(self.game.board.black_pawns))

    def test_switch_turn_should_return_BLACK_when_the_current_turn_is_WHITE(self):
        self.game.__check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.assertEqual(self.game.__switch_turn(), Color.BLACK)

    def test_switch_turn_should_return_WHITE_when_the_current_turn_is_BLACK(self):
        self.game.__check_whose_turn = MagicMock(return_value=Color.BLACK)
        self.assertEqual(self.game.__switch_turn(), Color.WHITE)
