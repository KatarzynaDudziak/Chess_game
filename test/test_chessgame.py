import unittest
from chessgame import ChessGame
from point import Point
from pawns import *
from unittest.mock import MagicMock
from board import EMPTY_SQUARE


class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.board = MagicMock()

    def test_valid_move_should_cause_check(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.is_capture_valid = MagicMock(return_value=False)
        self.game.is_move_valid = MagicMock(return_value=True)
        self.game.board.execute_move = MagicMock()
        self.game.is_check = MagicMock(return_value=True)
        self.game.switch_turn = MagicMock()
        
        self.assertTrue(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.switch_turn.assert_called_once()
        
    def test_valid_move_should_not_cause_check(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.is_capture_valid = MagicMock(return_value=False)
        self.game.is_move_valid = MagicMock(return_value=True)
        self.game.board.execute_move = MagicMock()
        self.game.is_check = MagicMock(return_value=False)
        self.game.switch_turn = MagicMock()

        self.assertTrue(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.switch_turn.assert_not_called()

    def test_invalid_move_should_not_result_in_move_and_check(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(3, 3)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.is_capture_valid = MagicMock(return_value=False)
        self.game.is_move_valid = MagicMock(return_value=False)
        self.game.board.execute_move = MagicMock()
        self.game.is_check = MagicMock()
        self.game.switch_turn = MagicMock()

        self.assertFalse(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.board.execute_move.assert_not_called()
        self.game.is_check.assert_not_called()
        self.game.switch_turn.assert_not_called()

    def test_is_capture_valid_should_cause_piece_capture(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.is_capture_valid = MagicMock(return_value=True)
        self.game.capture = MagicMock()

        self.assertFalse(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.capture.assert_called_once()

    def test_capturing_attempts_the_same_piece_color_should_not_results_in_capture(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.get_opponent = MagicMock(return_value=(WhitePawn(), new_pos))
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.is_capture_valid = MagicMock(return_value=False)
        self.game.capture = MagicMock()

        self.assertFalse(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.capture.assert_not_called()

    def test_piece_cannot_move_if_it_is_not_its_turn(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=WhitePawn())
        self.game.check_whose_turn = MagicMock(return_value=Color.BLACK)
        self.game.is_capture_valid = MagicMock(return_value=False)
        self.game.is_move_valid = MagicMock(return_value=True)
        self.game.board.execute_move = MagicMock()
        self.game.is_check = MagicMock(return_value=False)
        self.game.switch_turn = MagicMock()

        self.assertFalse(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.board.execute_move.assert_not_called()
        self.game.switch_turn.assert_not_called()

    def test_piece_cannot_move_if_is_not_instance_pawn(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(1, 2)
        self.game.board.get_piece_at_the_position = MagicMock(return_value=EMPTY_SQUARE)
        self.game.check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.game.capture = MagicMock()
        self.game.board.execute_move = MagicMock()
        self.game.switch_turn = MagicMock()

        self.assertFalse(self.game.move_piece(current_white_piece_pos, new_pos))
        self.game.capture.assert_not_called()
        self.game.board.execute_move.assert_not_called()
        self.game.switch_turn.assert_not_called()

    def test_capture_should_happen_if_opponent_pawn_is_in_new_pos(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        pawn = WhitePawn()
        self.game.get_opponent = MagicMock(return_value=(BlackPawn(), new_pos))
        pawn.can_capture = MagicMock(return_value=True)
        self.game.is_simulated_action_valid = MagicMock(return_value=True)
        self.game.board.is_path_clear = MagicMock(return_value=True)

        self.assertTrue(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_called_once()
        self.game.board.is_path_clear.assert_called_once()

    def test_capture_should_not_happen_if_opponent_pawn_is_not_in_new_pos(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        pawn = WhitePawn()
        self.game.get_opponent = MagicMock(return_value=None)
        pawn.can_capture = MagicMock(return_value=True)
        self.game.is_simulated_action_valid = MagicMock(return_value=True)
        self.game.board.is_path_clear = MagicMock(return_value=True)

        self.assertFalse(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_not_called()
        self.game.board.is_path_clear.assert_not_called()

    def test_capture_should_not_happen_if_pawn_cannot_capture(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(1, 3)
        pawn = WhitePawn()
        self.game.get_opponent = MagicMock(return_value=(BlackPawn(), new_pos))
        pawn.can_capture = MagicMock(return_value=False)
        self.game.is_simulated_action_valid = MagicMock(return_value=True)
        self.game.board.is_path_clear = MagicMock(return_value=True)

        self.assertFalse(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_not_called()
        self.game.board.is_path_clear.assert_not_called()
        
    def test_capture_should_not_happen_if_simulated_action_is_not_valid(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        pawn = WhitePawn()
        self.game.get_opponent = MagicMock(return_value=(BlackPawn(), new_pos))
        pawn.can_capture = MagicMock(return_value=True)
        self.game.is_simulated_action_valid = MagicMock(return_value=False)
        self.game.board.is_path_clear = MagicMock(return_value=True)

        self.assertFalse(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_called_once()
        self.game.board.is_path_clear.assert_not_called()

    def test_capture_should_not_happen_if_path_is_not_clear(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        pawn = WhitePawn()
        self.game.get_opponent = MagicMock(return_value=(BlackPawn(), new_pos))
        pawn.can_capture = MagicMock(return_value=True)
        self.game.is_simulated_action_valid = MagicMock(return_value=True)
        self.game.board.is_path_clear = MagicMock(return_value=False)

        self.assertFalse(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_called_once()
        self.game.board.is_path_clear.assert_called_once()

    def test_capture_should_happen_if_piece_isinstance_knight(self):
        current_white_piece_pos = Point(1, 1)
        new_pos = Point(2, 3)
        pawn = Knight()
        self.game.get_opponent = MagicMock(return_value=(BlackPawn(), new_pos))
        pawn.can_capture = MagicMock(return_value=True)
        self.game.is_simulated_action_valid = MagicMock(return_value=True)
        self.game.board.is_path_clear = MagicMock(return_value=True)

        self.assertTrue(self.game.is_capture_valid(pawn, current_white_piece_pos, new_pos))
        self.game.get_opponent.assert_called_once_with(pawn, new_pos)
        self.game.is_simulated_action_valid.assert_called_once()
        self.game.board.is_path_clear.assert_not_called()

