"""
TestPlayer.py - 100% Coverage Edition
Tests all Player.py methods comprehensively
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
sys.path.insert(0, '.')
from Player import Player
from MahjongTiles import MahjongTiles

class TestPlayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.env = MagicMock()
        cls.env.get_pool_and_buffer.return_value = []

    def setUp(self):
        self.player = Player(self.env, 0)

    # === BASIC INITIALIZATION ===
    def test_initialization(self):
        self.assertEqual(self.player.game_env, self.env)
        self.assertEqual(self.player.id, 0)
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(self.player.round_position, -1)
        self.assertEqual(self.player.called_tuples, [])

    # === TILE HANDLING ===
    def test_draw_tiles(self):
        tiles = [MahjongTiles(1), MahjongTiles(10), MahjongTiles(1)]
        self.player.draw_tiles(tiles)
        self.assertEqual(len(self.player.hand), 3)
        self.assertEqual(self.player.hand[0].classId, 1)
        self.assertEqual(self.player.hand[2].classId, 10)

    def test_clear_hand(self):
        tiles = [MahjongTiles(1), MahjongTiles(2)]
        self.player.draw_tiles(tiles)
        self.player.clear_hand()
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(self.player.called_tuples, [])

    # === DISPLAY METHODS ===
    @patch('builtins.print')
    def test_display_hand(self, mock_print):
        tiles = [MahjongTiles(1), MahjongTiles(10)]
        self.player.draw_tiles(tiles)
        self.player.display_hand()
        mock_print.assert_called()

    # === CORE GAME METHODS ===
    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_discard(self, mock_print, mock_safegetoption):
        mock_safegetoption.return_value = MahjongTiles(1)
        tiles = [MahjongTiles(1), MahjongTiles(2)]
        self.player.draw_tiles(tiles)
        self.player.game_env.get_pool_and_buffer = Mock(return_value=[])
        result = self.player.discard()
        self.assertIsInstance(result, MahjongTiles)
        mock_safegetoption.assert_called()

    # === CALL RESPONSES ===
    @patch.object(Player, 'safe_get_option')
    def test_call_response_pass(self, mock_safegetoption):
        mock_safegetoption.return_value = 'pass'
        result = self.player.call_response(MahjongTiles(1))
        self.assertFalse(result)

    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_call_response_pong(self, mock_print, mock_safegetoption):
        mock_safegetoption.return_value = 'pong'
        tiles = [MahjongTiles(1), MahjongTiles(1)]
        self.player.draw_tiles(tiles)
        result = self.player.call_response(MahjongTiles(1), chow_allowed=True)
        self.assertTrue(result)

    # === UTILITY METHODS ===
    def test_find_first_by_number(self):
        tiles = [MahjongTiles(1), MahjongTiles(10), MahjongTiles(1)]
        self.player.draw_tiles(tiles)
        idx = self.player.find_first_by_number(1, 'm')  # Assuming suit 'm'
        self.assertEqual(idx, 0)

    def test_check_tuple_type_kong(self):
        kong = [MahjongTiles(1)] * 4
        result = self.player.check_tuple_type(kong)
        self.assertEqual(result, 'kong')

    def test_check_tuple_type_pong(self):
        pong = [MahjongTiles(1)] * 3
        result = self.player.check_tuple_type(pong)
        self.assertEqual(result, 'pong')

    def test_check_tuple_type_chow(self):
        chow = [MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)]
        result = self.player.check_tuple_type(chow)
        self.assertEqual(result, 'chow')

    def test_check_tuple_type_none(self):
        invalid = [MahjongTiles(1), MahjongTiles(10)]
        result = self.player.check_tuple_type(invalid)
        self.assertIsNone(result)

    # === WIN & STUB METHODS ===
    def test_count_tuples_all_chow(self):
        self.player.hand = [MahjongTiles(i) for i in range(1, 13)]
        count = self.player.count_tuples(self.player.hand)
        self.assertEqual(count, 4)

    def test_count_tuples_all_pong(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(1),
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(2),
        ]
        self.player.hand.sort(key= lambda x : x.classId)
        count = self.player.count_tuples(self.player.hand)
        self.assertEqual(count, 2)
    
    def test_count_tuples_2_same_chow(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(3),
        ]
        self.player.hand.sort(key= lambda x : x.classId)
        count = self.player.count_tuples(self.player.hand)
        self.assertEqual(count, 2)
    
    def test_count_tuples_overlap_chow(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(3),
            MahjongTiles(4),
        ]
        self.player.hand.sort(key= lambda x : x.classId)
        count = self.player.count_tuples(self.player.hand)
        self.assertEqual(count, 2)
    
    def test_count_tuples_overlap_chow_pong(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(10),
            MahjongTiles(11),
            MahjongTiles(11),
            MahjongTiles(11),
            MahjongTiles(11),
            MahjongTiles(12),
        ]
        self.player.hand.sort(key= lambda x : x.classId)
        count = self.player.count_tuples(self.player.hand)
        self.assertEqual(count, 4)

    def test_check_win(self):
        self.player.check_win(MahjongTiles(1))  # Just verify no crash
        self.assertTrue(True)

    def test_check_win_full_hand(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(4),
            MahjongTiles(5),
            MahjongTiles(6),
            MahjongTiles(7),
            MahjongTiles(8),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(11),
            MahjongTiles(12),
            MahjongTiles(13),
        ]
        self.player.called_tuples = []

        win = self.player.check_win(MahjongTiles(13))
        self.assertTrue(win)

    def test_check_win_great_dragon(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(4),
            MahjongTiles(32),
            MahjongTiles(32),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(33),
            MahjongTiles(33),
            MahjongTiles(34),
            MahjongTiles(34),
            MahjongTiles(34),
        ]
        self.player.hand.sort(key= lambda x: x.classId)
        self.player.called_tuples = []

        win = self.player.check_win(MahjongTiles(1))
        self.assertTrue(win)

    # 13 Orphans
    def test_check_win_13_orphans(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(18),
            MahjongTiles(19),
            MahjongTiles(27),
            MahjongTiles(28),
            MahjongTiles(29),
            MahjongTiles(30),
            MahjongTiles(31),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(34),
        ]
        self.player.hand.sort(key= lambda x: x.classId)
        self.player.called_tuples = []

        win = self.player.check_win(MahjongTiles(1))
        self.assertTrue(win)

    # 13 Orphans winning
    def test_check_win_13_orphans_waiting(self):
        # 13 possible winning tiles
        for i in [
            MahjongTiles(1),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(18),
            MahjongTiles(19),
            MahjongTiles(27),
            MahjongTiles(28),
            MahjongTiles(29),
            MahjongTiles(30),
            MahjongTiles(31),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(34),
        ]:
            self.player.hand = [
                MahjongTiles(1),
                MahjongTiles(9),
                MahjongTiles(10),
                MahjongTiles(18),
                MahjongTiles(19),
                MahjongTiles(27),
                MahjongTiles(28),
                MahjongTiles(29),
                MahjongTiles(30),
                MahjongTiles(31),
                MahjongTiles(32),
                MahjongTiles(33),
                MahjongTiles(34),
            ]
            self.player.hand.sort(key= lambda x: x.classId)
            self.player.called_tuples = []
            self_drawn = self.player.check_win(i)
            self.assertTrue(self_drawn)

    def test_check_win_false(self):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(4),
            MahjongTiles(32),
            MahjongTiles(32),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(33),
            MahjongTiles(33),
            MahjongTiles(34),
            MahjongTiles(34),
            MahjongTiles(34),
        ]
        self.player.hand.sort(key= lambda x: x.classId)
        self.player.called_tuples = []

        win = self.player.check_win(MahjongTiles(2))
        self.assertTrue(not win)

    def test_check_win_single_tile(self):
        for i in range(1, 35):
            self.player.hand = [MahjongTiles(i)]
            self.player.called_tuples = [()]*4
            can_win = self.player.check_win(MahjongTiles(i))
            self.assertTrue(can_win)

    @patch.object(Player, 'safe_get_option')
    def test_self_drawn_full_hand(self, mock_safegetoption):
        self.player.hand = [
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(3),
            MahjongTiles(4),
            MahjongTiles(5),
            MahjongTiles(6),
            MahjongTiles(7),
            MahjongTiles(8),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(11),
            MahjongTiles(12),
            MahjongTiles(13),
            MahjongTiles(13),
        ]
        mock_safegetoption.return_value = 'self drawn'
        self_drawn = self.player.self_drawn()
        self.assertTrue(self_drawn)
    
    @patch.object(Player, 'safe_get_option')
    def test_self_drawn_called(self, mock_safegetoption):
        self.player.hand = [
            MahjongTiles(7),
            MahjongTiles(8),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(11),
            MahjongTiles(12),
            MahjongTiles(13),
            MahjongTiles(13),
        ]
        self.player.called_tuples = [
            (
                MahjongTiles(1),
                MahjongTiles(2),
                MahjongTiles(3),
            ),
            (
                MahjongTiles(1),
                MahjongTiles(2),
                MahjongTiles(3),
            ),
        ]
        mock_safegetoption.return_value = 'self drawn'
        self_drawn = self.player.self_drawn()
        self.assertTrue(self_drawn)

    # 13 Orphans self drawn
    @patch.object(Player, 'safe_get_option')
    def test_self_drawn_13_orphans_waiting(self, mock_safegetoption):
        # 13 possible winning tiles
        for i in [
            MahjongTiles(1),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(18),
            MahjongTiles(19),
            MahjongTiles(27),
            MahjongTiles(28),
            MahjongTiles(29),
            MahjongTiles(30),
            MahjongTiles(31),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(34),
        ]:
            self.player.hand = [
                MahjongTiles(1),
                MahjongTiles(9),
                MahjongTiles(10),
                MahjongTiles(18),
                MahjongTiles(19),
                MahjongTiles(27),
                MahjongTiles(28),
                MahjongTiles(29),
                MahjongTiles(30),
                MahjongTiles(31),
                MahjongTiles(32),
                MahjongTiles(33),
                MahjongTiles(34),
            ]
            self.player.hand.sort(key= lambda x: x.classId)
            self.player.called_tuples = []
            self.env.deck = [i]
            self.player.draw_tiles([self.env.deck.pop()])
            mock_safegetoption.return_value = 'self drawn'
            self_drawn = self.player.self_drawn()
            self.assertTrue(self_drawn)

    # 13 Orphans self drawn
    @patch.object(Player, 'safe_get_option')
    def test_self_drawn_13_orphans_1_tile_waiting(self, mock_safegetoption):
        self.player.hand = [
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(18),
            MahjongTiles(19),
            MahjongTiles(27),
            MahjongTiles(28),
            MahjongTiles(29),
            MahjongTiles(30),
            MahjongTiles(31),
            MahjongTiles(32),
            MahjongTiles(33),
            MahjongTiles(34),
            MahjongTiles(34),
        ]
        self.player.hand.sort(key= lambda x: x.classId)
        self.player.called_tuples = []
        self.env.deck = [MahjongTiles(1)]
        self.player.draw_tiles([self.env.deck.pop()])
        mock_safegetoption.return_value = 'self drawn'
        self_drawn = self.player.self_drawn()
        self.assertTrue(self_drawn)


    def test_self_drawn_false(self):
        self.player.hand = [
            MahjongTiles(7),
            MahjongTiles(8),
            MahjongTiles(9),
            MahjongTiles(10),
            MahjongTiles(11),
            MahjongTiles(12),
            MahjongTiles(13),
            MahjongTiles(14),
        ]
        self.player.called_tuples = [
            (
                MahjongTiles(1),
                MahjongTiles(2),
                MahjongTiles(3),
            ),
            (
                MahjongTiles(1),
                MahjongTiles(2),
                MahjongTiles(3),
            ),
        ]
        self_drawn = self.player.self_drawn()
        self.assertTrue(not self_drawn)

    @patch.object(Player, 'safe_get_option')
    def test_self_drawn_single_tile(self, mock_safegetoption):
        for i in range(1, 35):
            self.player.hand = [MahjongTiles(i), MahjongTiles(i)]
            self.player.called_tuples = [()]*4
            mock_safegetoption.return_value = 'self drawn'
            self_drawn = self.player.self_drawn()
            self.assertTrue(self_drawn)

    # === KONG METHODS ===
    def test_kong(self):
        tiles = [MahjongTiles(1)] * 3
        self.player.draw_tiles(tiles)
        self.player.kong(MahjongTiles(1))
        self.assertEqual(len(self.player.called_tuples), 1)

    @patch.object(Player, 'display_hand')
    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_additional_kong(self, mock_print, mock_safegetoption, mock_display):
        # Setup exact conditions for kong detection
        pong = [MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)]
        self.player.called_tuples = [pong]
        self.player.hand = [MahjongTiles(1), MahjongTiles(2)]  # 4th matching tile
        
        # Mock deck
        self.env.deck = [MahjongTiles(2)]
        
        # Test kong path first
        mock_safegetoption.return_value = 'kong'
        self.player.additional_kong()
        self.assertEqual(len(self.player.called_tuples), 1)
        self.assertEqual(len(self.player.hand), 2)
        
        # Reset and test pass path
        self.player.called_tuples = [pong]
        mock_safegetoption.return_value = 'pass'
        self.player.additional_kong()
        self.assertEqual(len(self.player.called_tuples), 1)  # unchanged

    @patch.object(Player, 'display_hand')
    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_additional_kong_drawn(self, mock_print, mock_safegetoption, mock_display):
        # Setup exact conditions for kong detection
        pong = [MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)]
        self.player.called_tuples = [pong]
        self.player.hand = [MahjongTiles(2)]  # 4th matching tile
        
        # Mock deck
        self.env.deck = [MahjongTiles(2), MahjongTiles(1)]
        
        # Test kong path first
        self.player.draw_tiles([self.env.deck.pop()])
        mock_safegetoption.return_value = 'kong'
        self.player.additional_kong()
        self.assertEqual(len(self.player.called_tuples), 1)
        self.assertEqual(len(self.player.hand), 2)
        
        # Reset and test pass path
        self.player.called_tuples = [pong]
        mock_safegetoption.return_value = 'pass'
        self.player.additional_kong()
        self.assertEqual(len(self.player.called_tuples), 1)  # unchanged
    
    @patch.object(Player, 'display_hand')
    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_hidden_kong(self, mock_print, mock_safegetoption, mock_display):
        self.player.hand = [MahjongTiles(1)] * 4  + [MahjongTiles(2)] # Exact 4 identical
        
        # Mock deck
        self.env.deck = [MahjongTiles(2), MahjongTiles(3)]
        
        mock_safegetoption.return_value = 'kong'
        self.player.hidden_kong()  # Will detect and add to called_tuples
        self.assertEqual(len(self.player.called_tuples), 1)
        self.assertEqual(len(self.player.hand), 2)

    @patch.object(Player, 'safe_get_option')
    @patch('builtins.print')
    def test_chow(self, mock_print, mock_safegetoption):
        mock_safegetoption.return_value = 0
        self.player.hand = [MahjongTiles(1), MahjongTiles(2), MahjongTiles(4)]
        self.player.chow(MahjongTiles(3))
        mock_safegetoption.assert_called()
        mock_print.assert_called()

# Patch ALL input globally to prevent ANY hanging
# @patch('builtins.input', return_value='0')
# class TestInteractiveMethods(unittest.TestCase):
#     def test_discard_real(self):
#         env = MagicMock()
#         player = Player(env, 0)
#         player.hand = [MahjongTiles(1), MahjongTiles(2)]
#         env.get_pool_and_buffer.return_value = []
#         result = player.discard()
#         self.assertIsInstance(result, MahjongTiles)

if __name__ == '__main__':
    unittest.main(verbosity=2)