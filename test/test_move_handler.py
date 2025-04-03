import unittest
from unittest.mock import MagicMock, patch, call
from pawns import Pawn, BlackPawn, Knight, Color
from move_handler import MoveHandler
from point import Point
from board import EMPTY_SQUARE


class TestMoveHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.board = MagicMock()
        self.move_handler = MoveHandler(self.board)
        self.current_pos = (0, 0)
        self.new_pos = (1, 1)
        
    @patch("move_handler.isinstance", return_value=True)
    def test_pawn_should_not_move_if_it_is_not_players_turn(self, mock_isinstance):
        pawn = MagicMock()
        pawn.color = Color.BLACK
        self.board.get_piece_at_the_position.return_value = pawn
        self.board.execute_move = MagicMock()
    
        self.assertFalse(self.move_handler.move_piece(self.current_pos, self.new_pos,
                                                       MagicMock(return_value=Color.WHITE), MagicMock(), MagicMock()))
        mock_isinstance.assert_called_once_with(pawn, Pawn)
        self.board.execute_move.assert_not_called()

    @patch("move_handler.isinstance", return_value=True)
    def test_pawn_should_not_move_if_move_is_not_valid(self, mock_isinstance):
        pawn = MagicMock()
        pawn.color = Color.BLACK
        self.board.get_piece_at_the_position.return_value = pawn
        self.board.execute_move = MagicMock()
        self.move_handler.is_move_valid = MagicMock(return_value=False)

        self.assertFalse(self.move_handler.move_piece(self.current_pos, self.new_pos,
                                                       MagicMock(return_value=Color.BLACK), MagicMock(), MagicMock()))
        mock_isinstance.assert_called_once_with(pawn, Pawn)
        self.board.execute_move.assert_not_called()

    @patch("move_handler.isinstance", return_value=True)
    def test_pawn_should_move_if_it_is_valid(self, mock_isinstance):
        pawn = MagicMock()
        pawn.color = Color.BLACK
        self.board.get_piece_at_the_position.return_value = pawn
        self.board.execute_move = MagicMock()
        self.move_handler.is_move_valid = MagicMock(return_value=True)

        self.assertTrue(self.move_handler.move_piece(self.current_pos, self.new_pos,
                                                      MagicMock(return_value=Color.BLACK), MagicMock(), MagicMock()))
        mock_isinstance.assert_called_once_with(pawn, Pawn)
        self.board.execute_move.assert_called_once_with(pawn, self.current_pos, self.new_pos)

    def test_pawn_should_not_move_if_cannot(self):
        pawn = MagicMock()
        pawn.can_move.return_value = False
        self.move_handler.is_piece_move_valid = MagicMock()

        self.assertFalse(self.move_handler.is_move_valid(pawn, self.current_pos, self.new_pos,
                                                          MagicMock(), MagicMock(return_value=Color.BLACK)))
        self.move_handler.is_piece_move_valid.assert_not_called()

    def test_pawn_should_not_move_if_target_is_not_empty(self):
        pawn = MagicMock()
        pawn.can_move = MagicMock(return_value = True)
        self.board.get_piece = MagicMock(return_value = "Pawn")
        self.move_handler.is_piece_move_valid = MagicMock()

        self.assertFalse(self.move_handler.is_move_valid(pawn, self.current_pos, self.new_pos,
                                                          MagicMock(), MagicMock(return_value=Color.BLACK)))
        self.move_handler.is_piece_move_valid.assert_not_called()

    def test_should_return_true_if_move_is_valid(self):
        pawn = MagicMock()
        pawn.can_move = MagicMock(return_value = True)
        self.board.get_piece = MagicMock(return_value = EMPTY_SQUARE)
        self.move_handler.is_piece_move_valid = MagicMock(return_value=True)

        self.assertTrue(self.move_handler.is_move_valid(pawn, self.current_pos,
                                                         self.new_pos, MagicMock(), MagicMock(return_value=Color.BLACK)))
        self.move_handler.is_piece_move_valid.assert_called_once()

    @patch("move_handler.isinstance", return_value=True)
    def test_piece_move_should_be_valid_if_is_knight(self, mock_isinstance):
        knight = MagicMock()
        self.board.is_simulated_action_valid = MagicMock()

        self.assertTrue(self.move_handler.is_piece_move_valid(knight, self.current_pos,
                                                               self.new_pos, MagicMock(), MagicMock()))
        mock_isinstance.assert_called_once_with(knight, Knight)
        self.board.is_simulated_action_valid.assert_called_once()

    @patch("move_handler.isinstance", side_effect=[False, True])
    def test_piece_move_should_be_valid_if_path_is_clear(self, mock_isinstance):
        pawn = MagicMock()
        self.board.is_path_clear = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock()

        self.assertTrue(self.move_handler.is_piece_move_valid(pawn, self.current_pos,
                                                               self.new_pos, MagicMock(), MagicMock()))
        mock_isinstance.assert_has_calls([call(pawn, Knight), call(pawn, Pawn)])
        self.board.is_path_clear.assert_called_once_with(self.current_pos, self.new_pos)

    @patch("move_handler.isinstance", side_effect=[False, True])
    def test_piece_move_should_not_be_valid_if_path_is_not_clear(self, mock_isinstance):
        pawn = MagicMock()
        self.board.is_path_clear = MagicMock(return_value=False)
        self.board.is_simulated_action_valid = MagicMock()

        self.assertFalse(self.move_handler.is_piece_move_valid(pawn, self.current_pos,
                                                                self.new_pos, MagicMock(), MagicMock()))
        mock_isinstance.assert_has_calls([call(pawn, Knight), call(pawn, Pawn)])
        self.board.is_simulated_action_valid.assert_not_called()

    @patch("move_handler.isinstance", return_value=True)
    def test_should_return_false_if_simulated_move_is_not_valid(self, mock_isinstance):
        pawn = MagicMock()
        self.board.is_path_clear = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=False)

        self.assertFalse(self.move_handler.is_piece_move_valid(pawn, self.current_pos,
                                                                self.new_pos, MagicMock(), MagicMock()))
        mock_isinstance.assert_called_once_with(pawn, Knight)

    @patch("move_handler.isinstance", side_effect=[False, False])
    def test_should_not_be_valid_if_pawn_is_none(self, mock_isinstance):
        pawn = None
        self.board.is_simulated_action_valid = MagicMock()

        self.assertFalse(self.move_handler.is_piece_move_valid(None, self.current_pos,
                                                                self.new_pos, MagicMock(), MagicMock()))
        mock_isinstance.assert_has_calls([call(pawn, Knight), call(pawn, Pawn)])
        self.board.is_simulated_action_valid.assert_not_called()
        