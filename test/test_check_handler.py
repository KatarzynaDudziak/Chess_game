import unittest
from unittest.mock import patch, Mock, MagicMock, call
from check_handler import CheckHandler
from chessgame import Color
from pawns import Pawn, Knight, Color, WhitePawn, BlackPawn, WhiteBishop, BlackBishop, WhiteKnight, BlackKnight, \
    WhiteRook, BlackRook, WhiteQueen, BlackQueen, WhiteKing, BlackKing
from board import Board
from point import Point


class TestCheckHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.board = MagicMock()
        self.check_handler = CheckHandler(self.board)
        self.pawn = MagicMock()
        self.position = (1, 1)
        self.check_whose_turn = MagicMock()

    def test_return_black_color_if_white_pawn_can_make_a_check(self):
        check_whose_turn = MagicMock(return_value=Color.BLACK)
        self.board.white_pawns = [(self.pawn, self.position)]
        self.check_handler.can_make_a_check = MagicMock(return_value=True)

        self.assertEqual(self.check_handler.get_checked_king_color(check_whose_turn), Color.BLACK)
        self.check_handler.can_make_a_check.assert_called_once_with(self.board.white_pawns, Color.WHITE)
        
    def test_return_white_color_if_black_pawn_can_make_a_check(self):
        check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.board.black_pawns = [(self.pawn, self.position)]
        self.check_handler.can_make_a_check = MagicMock(return_value=True)

        self.assertEqual(self.check_handler.get_checked_king_color(check_whose_turn), Color.WHITE)
        self.check_handler.can_make_a_check.assert_called_once_with(self.board.black_pawns, Color.BLACK)

    def test_return_none_if_no_pawn_can_make_a_check(self):
        check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.board.white_pawns = [(self.pawn, self.position)]
        self.check_handler.can_make_a_check = MagicMock(return_value=False)

        self.assertIsNone(self.check_handler.get_checked_king_color(check_whose_turn))
        self.assertEqual(self.check_handler.can_make_a_check.call_count, 2)

    def test_should_return_white_color_if_is_black_turn_and_black_pawn_can_make_a_check(self):
        check_whose_turn = MagicMock(return_value=Color.BLACK)
        self.board.white_pawns = [(self.pawn, self.position)]
        self.board.black_pawns = [(self.pawn, self.position)]
        self.check_handler.can_make_a_check = MagicMock(side_effect=[False, True])

        self.assertEqual(self.check_handler.get_checked_king_color(check_whose_turn), Color.WHITE)
        self.check_handler.can_make_a_check.assert_has_calls([call(self.board.white_pawns, Color.WHITE),
                                                              call(self.board.black_pawns, Color.BLACK)])
        
    def test_should_return_black_color_if_is_white_turn_and_white_pawn_can_make_a_check(self):
        check_whose_turn = MagicMock(return_value=Color.WHITE)
        self.board.white_pawns = [(self.pawn, self.position)]
        self.board.black_pawns = [(self.pawn, self.position)]
        self.check_handler.can_make_a_check = MagicMock(side_effect=[False, True])

        self.assertEqual(self.check_handler.get_checked_king_color(check_whose_turn), Color.BLACK)
        self.check_handler.can_make_a_check.assert_has_calls([call(self.board.black_pawns, Color.BLACK),
                                                              call(self.board.white_pawns, Color.WHITE)])

    def test_should_return_false_if_can_escape_check(self):
        pawns_list = [(self.pawn, self.position)]
        self.board.get_piece = MagicMock(return_value=self.pawn)
        self.check_handler.can_escape_check = MagicMock(return_value=True)

        self.assertFalse(self.check_handler.is_checkmate(pawns_list, self.check_whose_turn))
        
        self.board.get_piece.assert_called_once_with(self.position)
        self.check_handler.can_escape_check.assert_called_once_with(self.pawn, self.position, self.check_whose_turn)

    def test_should_return_true_if_cannot_escape_check(self):
        pawns_list = [(self.pawn, self.position)]
        self.board.get_piece = MagicMock(return_value=self.pawn)
        self.check_handler.can_escape_check = MagicMock(return_value=False)

        self.assertTrue(self.check_handler.is_checkmate(pawns_list, self.check_whose_turn))
        
        self.board.get_piece.assert_called_once_with(self.position)
        self.check_handler.can_escape_check.assert_called_once_with(self.pawn, self.position, self.check_whose_turn)

    @patch('check_handler.range')
    @patch('check_handler.Point')
    def test_should_return_true_if_pawn_can_move(self, mock_point, mock_range):
        new_pos = (0, 0)
        mock_range.return_value = new_pos
        mock_point.return_value = new_pos
        self.pawn.can_move = MagicMock(return_value=True)
        self.pawn.can_capture = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=True)
        self.check_handler.get_checked_king_color = MagicMock()

        self.assertTrue(self.check_handler.can_escape_check(self.pawn, self.position, self.check_whose_turn))
        
        self.assertEqual(mock_range.call_count, 2)
        mock_point.assert_called()
        self.pawn.can_move.assert_called_once_with(self.position, new_pos)
        self.pawn.can_capture.assert_not_called()
        self.board.is_simulated_action_valid.assert_called_once_with(self.pawn, self.position,
                                                                      new_pos, self.check_handler.get_checked_king_color, self.check_whose_turn)

    @patch('check_handler.range')
    @patch('check_handler.Point')
    def test_should_return_true_if_pawn_can_capture_opponent(self, mock_point, mock_range):
        new_pos = (0, 0)
        mock_range.return_value = new_pos
        mock_point.return_value = new_pos
        self.pawn.can_move = MagicMock(return_value=False)
        self.pawn.can_capture = MagicMock(return_value=True)
        self.board.is_simulated_action_valid = MagicMock(return_value=True)
        self.check_handler.get_checked_king_color = MagicMock()

        self.assertTrue(self.check_handler.can_escape_check(self.pawn, self.position, self.check_whose_turn))
        
        self.assertEqual(mock_range.call_count, 2)
        mock_point.assert_called()
        self.pawn.can_move.assert_called_once_with(self.position, new_pos)
        self.pawn.can_capture.assert_called_once_with(self.position, new_pos)
        self.board.is_simulated_action_valid.assert_called_once_with(self.pawn, self.position,
                                                                      new_pos, self.check_handler.get_checked_king_color, self.check_whose_turn)

    @patch('check_handler.range', return_value=range(1))
    @patch('check_handler.Point')
    def test_should_return_False_if_pawn_cannot_move_or_capture(self, mock_point, mock_range):
        new_pos = (0, 0)
        mock_point.return_value = new_pos
        self.pawn.can_move = MagicMock(return_value=False)
        self.pawn.can_capture = MagicMock(return_value=False)
        self.board.is_simulated_action_valid = MagicMock(return_value=True)
        self.check_handler.get_checked_king_color = MagicMock()

        self.assertFalse(self.check_handler.can_escape_check(self.pawn, self.position, self.check_whose_turn))
        
        self.assertEqual(mock_range.call_count, 2)
        mock_point.assert_called()
        self.pawn.can_move.assert_called_once_with(self.position, new_pos)
        self.pawn.can_capture.assert_called_once_with(self.position, new_pos)
        self.board.is_simulated_action_valid.assert_not_called()

    @patch('check_handler.range', return_value=range(1))
    @patch('check_handler.Point', return_value=None)
    def test_should_return_False_if_point_is_none(self, mock_point, mock_range):
        self.pawn.can_move = MagicMock(return_value=False)
        self.pawn.can_capture = MagicMock(return_value=False)
        self.board.is_simulated_action_valid = MagicMock(return_value=False)
        self.check_handler.get_checked_king_color = MagicMock()

        self.assertFalse(self.check_handler.can_escape_check(self.pawn, self.position, self.check_whose_turn))
        
        self.assertEqual(mock_range.call_count, 2)
        mock_point.assert_called()
        self.pawn.can_move.assert_called_once_with(self.position, None)
        self.pawn.can_capture.assert_called_once_with(self.position, None)
        self.board.is_simulated_action_valid.assert_not_called()

    def test_should_return_true_if_can_capture_king(self):
        king_pos = (0, 0)
        pawns_list = [(self.pawn, self.position)]
        self.board.get_piece = MagicMock(return_value=self.pawn)
        self.board.get_king_position = MagicMock(return_value=king_pos)
        self.check_handler.can_capture_king = MagicMock(return_value=True)

        self.assertTrue(self.check_handler.can_make_a_check(pawns_list))
        
        self.check_handler.can_capture_king.assert_called_once_with(self.pawn, self.position, king_pos)

    def test_should_return_false_if_cannot_capture_king(self):
        king_pos = (0, 0)
        pawns_list = [(self.pawn, self.position)]
        self.board.get_piece = MagicMock(return_value=self.pawn)
        self.board.get_king_position = MagicMock(return_value=king_pos)
        self.check_handler.can_capture_king = MagicMock(return_value=False)

        self.assertFalse(self.check_handler.can_make_a_check(pawns_list))

        self.check_handler.can_capture_king.assert_called_once_with(self.pawn, self.position, king_pos)

    def test_should_return_false_if_king_position_is_none(self):
        pawns_list = [(self.pawn, self.position)]
        self.board.get_piece = MagicMock(return_value=self.pawn)
        self.board.get_king_position = MagicMock(return_value=None)
        self.check_handler.can_capture_king = MagicMock()

        self.assertFalse(self.check_handler.can_make_a_check(pawns_list))
        
        self.board.get_king_position.assert_called_once_with(self.pawn)
        self.check_handler.can_capture_king.assert_not_called()

    def test_should_return_false_if_pawns_list_is_empty(self):
        pawns_list = []
        self.board.get_piece = MagicMock()
        self.board.get_king_position = MagicMock()
        self.check_handler.can_capture_king = MagicMock()

        self.assertFalse(self.check_handler.can_make_a_check(pawns_list, pawns_color=Color.WHITE))
        
        self.board.get_piece.assert_not_called()
        self.board.get_king_position.assert_not_called()
        self.check_handler.can_capture_king.assert_not_called()

    @patch("check_handler.isinstance")
    def test_should_return_true_if_knight_can_capture_king(self, mock_isinstance):
        king_pos = (0, 0)
        knight = MagicMock()
        knight.can_capture = MagicMock(return_value=True)
        self.board.is_path_clear = MagicMock()

        self.assertTrue(self.check_handler.can_capture_king(knight, self.position, king_pos))

        mock_isinstance.assert_called_once_with(knight, Knight)
        knight.can_capture.assert_called_once_with(self.position, king_pos)
        self.board.is_path_clear.assert_not_called()

    @patch("check_handler.isinstance")
    def tets_should_return_true_if_pawn_can_capture_king(self, mock_isinstance):
        king_pos = (0, 0)
        self.pawn.can_capture = MagicMock(return_value=True)
        self.board.is_path_clear = MagicMock(return_value=True)

        self.assertTrue(self.check_handler.can_capture_king(self.pawn, self.position, king_pos))

        mock_isinstance.assert_called_once_with(self.pawn, Knight)
        self.pawn.can_capture.assert_called_once_with(self.position, king_pos)
        self.board.is_path_clear.assert_called_once_with(self.position, king_pos)

    @patch("check_handler.isinstance")
    def test_should_return_false_if_piece_cannot_capture_king(self, mock_isinstance):
        king_pos = (0, 0)
        self.pawn.can_capture = MagicMock(return_value=False)
        self.board.is_path_clear = MagicMock(return_value=False)
        mock_isinstance.return_value = False

        self.assertFalse(self.check_handler.can_capture_king(self.pawn, self.position, king_pos))

        mock_isinstance.assert_called_once_with(self.pawn, Knight)
        self.pawn.can_capture.assert_called_once_with(self.position, king_pos)
        self.board.is_path_clear.assert_not_called()
