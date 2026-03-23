import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import random
from Policy import Policy

sys.path.insert(0, '.')
from MahjongTile import MahjongTile

class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = Policy()
        self.discard_pool = [MahjongTile(1), MahjongTile(10), MahjongTile(19)]
        self.hand = [MahjongTile(i) for i in range(1, 10)] + [MahjongTile(i) for i in range(28, 32)]
        self.called_tuples = []
        self.call_tile = MahjongTile(3)

    def test_extract_features(self):
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 'm')  # Since hand has 9 m tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)
        
        self.hand = [MahjongTile(i) for i in range(10, 19)] + [MahjongTile(i) for i in range(28, 32)]
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 'p')  # Since hand has 9 p tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)
        
        self.hand = [MahjongTile(i) for i in range(19, 28)] + [MahjongTile(i) for i in range(28, 32)]
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 's')  # Since hand has 9 s tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)

        # 13 Orphans
        self.hand = [
            MahjongTile(1),
            MahjongTile(9),
            MahjongTile(10),
            MahjongTile(18),
            MahjongTile(19),
            MahjongTile(27),
            MahjongTile(28),
            MahjongTile(29),
            MahjongTile(30),
            MahjongTile(31),
            MahjongTile(32),
            MahjongTile(33),
            MahjongTile(34)
        ]
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 'm') # Since index() only returns the first occurrence of max count, hence is 'm'
        self.assertEqual(consec_2_count, 0)
        self.assertEqual(alternating_consec_2_count, 0) # 13 orphans has no consecutive/ alternating consecutive tiles

    def test_decide_kong(self):
        result = self.policy.decide_kong(self.call_tile)
        self.assertFalse(result)

    def test_decide_pong(self):
        result = self.policy.decide_pong(self.call_tile)
        self.assertFalse(result)

    def test_decide_chow_helper(self):
        ...

    def test_decide_chow(self):
        result = self.policy.decide_chow(self.call_tile)
        self.assertFalse(result)

    def test_decide_win(self):
        result = self.policy.decide_win(self.call_tile)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)