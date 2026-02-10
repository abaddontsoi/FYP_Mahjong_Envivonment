import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import random
from Policy import Policy

sys.path.insert(0, '.')
from MahjongTiles import MahjongTiles

class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = Policy()
        self.discard_pool = [MahjongTiles(1), MahjongTiles(10), MahjongTiles(19)]
        self.hand = [MahjongTiles(i) for i in range(1, 10)] + [MahjongTiles(i) for i in range(28, 32)]
        self.called_tuples = []
        self.call_tile = MahjongTiles(3)

    def test_extract_features(self):
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 'm')  # Since hand has 9 m tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)
        
        self.hand = [MahjongTiles(i) for i in range(10, 19)] + [MahjongTiles(i) for i in range(28, 32)]
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 'p')  # Since hand has 9 p tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)
        
        self.hand = [MahjongTiles(i) for i in range(19, 28)] + [MahjongTiles(i) for i in range(28, 32)]
        self.policy.update_board_state(self.discard_pool, self.hand, self.called_tuples)
        existing, hand_existing, dominating_suit, pair_count, consec_2_count, alternating_consec_2_count, pong_kong_count = self.policy.extract_features()
        self.assertIn(dominating_suit, ['m', 'p', 's'])
        self.assertEqual(dominating_suit, 's')  # Since hand has 9 s tiles, it should be the dominating suit
        self.assertEqual(consec_2_count, 8)
        self.assertEqual(alternating_consec_2_count, 7)

        # 13 Orphans
        self.hand = [
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
            MahjongTiles(34)
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