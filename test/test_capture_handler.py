import unittest
from unittest.mock import MagicMock, patch
from capture_handler import CaptureHandler
from pawns import Pawn, Knight, Color


class TestCaptureHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.board = MagicMock()
        self.capture_handler = CaptureHandler(self.board)
        self.pawn = MagicMock()
        self.is_check = MagicMock()
        self.check_whose_turn = MagicMock()
        self.current_pos = (0, 0)
        self.new_pos = (1, 1)  

    def test_should_return_false_if_target_pawn_is_none(self):
        self.capture_handler.get_opponent = MagicMock(return_value=None)
        self.pawn.can_capture= MagicMock()
        self.board.is_simulated_action_valid = MagicMock()

        self.assertFalse(self.capture_handler.is_capture_valid(self.pawn, self.current_pos,
                                                                self.new_pos, self.is_check, self.check_whose_turn))
        
        self.pawn.assert_not_called()
        self.board.is_simulated_action_valid.assert_not_called()

    def test_should_return_false_if_pawn_cannot_capture(self):
        self.capture_handler.get_opponent = MagicMock(return_value=("Pawn", self.new_pos))
        self.pawn.can_capture = MagicMock(return_value=False)
        self.board.is_path_clear = MagicMock()
        self.board.is_simulated_action_valid = MagicMock()

        self.assertFalse(self.capture_handler.is_capture_valid(self.pawn, self.current_pos,
                                                                self.new_pos, self.is_check, self.check_whose_turn))

        self.board.is_path_clear.assert_not_called()
        self.board.is_simulated_action_valid.assert_not_called()

    @patch("capture_handler.isinstance")
    def test_should_return_true_if_pawn_is_instance_knight(self, mock_isinstance):
        knight = MagicMock()
        knight.can_capture = MagicMock(return_value=True)
        self.capture_handler.get_opponent = MagicMock(return_value=("Pawn", self.new_pos))
        self.board.is_simulated_action_valid = MagicMock(return_value=True)

        self.assertTrue(self.capture_handler.is_capture_valid(knight, self.current_pos,
                                                               self.new_pos, self.is_check, self.check_whose_turn))
        
        knight.can_capture.assert_called_once_with(self.current_pos, self.new_pos)
        mock_isinstance.assert_called_once_with(knight, Knight)
        self.board.is_simulated_action_valid.assert_called_once_with(knight, self.current_pos,
                                                                      self.new_pos, self.is_check, self.check_whose_turn)

    @patch("capture_handler.isinstance", return_value=False)
    def test_should_return_true_if_pawn_can_capture_and_path_is_clear(self, mock_isinstance):
        self.capture_handler.get_opponent = MagicMock(return_value=("Pawn", self.new_pos))
        self.pawn.can_capture = MagicMock(return_value=True)
        self.board.is_path_clear = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=True)

        self.assertTrue(self.capture_handler.is_capture_valid(self.pawn, self.current_pos,
                                                               self.new_pos, self.is_check, self.check_whose_turn))

        self.pawn.can_capture.assert_called_once_with(self.current_pos, self.new_pos)
        mock_isinstance.assert_called_once_with(self.pawn, Knight)
        self.board.is_path_clear.assert_called_once_with(self.current_pos, self.new_pos)
        self.board.is_simulated_action_valid.assert_called_once_with(self.pawn, self.current_pos,
                                                                      self.new_pos, self.is_check, self.check_whose_turn)
