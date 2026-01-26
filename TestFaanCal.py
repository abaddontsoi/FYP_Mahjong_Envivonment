import unittest
from unittest.mock import patch, MagicMock, Mock
import sys

from FaanCalculator import FaanCalculator
sys.path.insert(0, '.')
from MahjongTiles import MahjongTiles


class TestFaanCal(unittest.TestCase):

    def setUp(self):
        self.calculator = FaanCalculator(0, 0)

    def test_is_valid_winning_hand(self):
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),  # Chow
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)                     # Pair
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())

    def test_red_white_green(self):
        self.calculator.hand = [
            MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32), # Red Dragon Pong
            MahjongTiles(33), MahjongTiles(33), MahjongTiles(33),  # White Dragon Pong
            MahjongTiles(34), MahjongTiles(34), MahjongTiles(34),  # Green Dragon Pong
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)                     # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.red())
        self.assertTrue(self.calculator.white())
        self.assertTrue(self.calculator.green())

    def test_red_white_green_false(self):
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(2),  MahjongTiles(2),
            MahjongTiles(3), MahjongTiles(3), MahjongTiles(3),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),
            MahjongTiles(8), MahjongTiles(8)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.red())
        self.assertFalse(self.calculator.white())
        self.assertFalse(self.calculator.green())

    def test_round_wind(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.round = i
            self.calculator.hand = [
                MahjongTiles(28 + i), MahjongTiles(28 + i), MahjongTiles(28 + i),  # Pong of round wind
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(15), MahjongTiles(15), MahjongTiles(15),  # Pong
                MahjongTiles(8), MahjongTiles(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertTrue(self.calculator.round_wind())
    
    def test_round_wind_false(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.round = i
            self.calculator.hand = [
                MahjongTiles(28 - i - 1), MahjongTiles(28 - i), MahjongTiles(28 - i),
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(15), MahjongTiles(15), MahjongTiles(15),  # Pong
                MahjongTiles(8), MahjongTiles(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertFalse(self.calculator.round_wind())

    def test_round_position(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.position = i
            self.calculator.hand = [
                MahjongTiles(28 + i), MahjongTiles(28 + i), MahjongTiles(28 + i),  # Pong of position wind
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(15), MahjongTiles(15), MahjongTiles(15),  # Pong
                MahjongTiles(8), MahjongTiles(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertTrue(self.calculator.round_position())

    def test_round_position_false(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.position = i
            self.calculator.hand = [
                MahjongTiles(28 - i - 1), MahjongTiles(28 - i - 1), MahjongTiles(28 - i - 1),  # Pong of position wind
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
                MahjongTiles(15), MahjongTiles(15), MahjongTiles(15),  # Pong
                MahjongTiles(8), MahjongTiles(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertFalse(self.calculator.round_position())

    def test_mixed_orphans(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(9), MahjongTiles(9), MahjongTiles(9), MahjongTiles(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Characters
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # Pong of 1 Characters
            MahjongTiles(30), MahjongTiles(30)  # Pair of 5 of Characters
        ]
        self.assertTrue(self.calculator.mixed_orphans())

    def test_mixed_orphans_false(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(9), MahjongTiles(9), MahjongTiles(9), MahjongTiles(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Characters
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # Pong of 1 Characters
            MahjongTiles(3), MahjongTiles(3)  # Pair of 5 of Characters
        ]
        self.assertFalse(self.calculator.mixed_orphans())

    def test_all_pong_hand(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Pong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.all_pong_hand())
    
    def test_all_pong_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),  # Chow of 1-2-3 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Pong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        self.assertFalse(self.calculator.all_pong_hand())

    def test_clean_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),
            (MahjongTiles(4), MahjongTiles(5), MahjongTiles(6)),
            (MahjongTiles(7), MahjongTiles(8), MahjongTiles(9)),
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),
        ]
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.clean_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),
            MahjongTiles(4), MahjongTiles(5), MahjongTiles(6),
            MahjongTiles(7), MahjongTiles(8), MahjongTiles(9),
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),
            MahjongTiles(31), MahjongTiles(31)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.clean_hand())

    def test_clean_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),
            (MahjongTiles(4), MahjongTiles(5), MahjongTiles(6)),
            (MahjongTiles(7), MahjongTiles(8), MahjongTiles(9)),
            (MahjongTiles(11), MahjongTiles(11), MahjongTiles(11)),
        ]
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.clean_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),
            MahjongTiles(4), MahjongTiles(5), MahjongTiles(6),
            MahjongTiles(7), MahjongTiles(8), MahjongTiles(9),
            MahjongTiles(11), MahjongTiles(11), MahjongTiles(11),
            MahjongTiles(31), MahjongTiles(31)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.clean_hand())

    def test_pure_suit(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),
            (MahjongTiles(4), MahjongTiles(5), MahjongTiles(6)),
            (MahjongTiles(7), MahjongTiles(8), MahjongTiles(9)),
            (MahjongTiles(7), MahjongTiles(8), MahjongTiles(9)),
        ]
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.pure_suit())

    def test_pure_suit_no_call(self):
        self.calculator.called_tuples = [
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(4),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7), MahjongTiles(8), 
            MahjongTiles(9), MahjongTiles(9), MahjongTiles(9),
            MahjongTiles(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.pure_suit())

    def test_pure_suit_false(self):
        self.calculator.called_tuples = [
            (
                MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),
            ),
            (
                MahjongTiles(11), MahjongTiles(11), MahjongTiles(11),
            ),
        ]
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(4),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7), MahjongTiles(8), 
            MahjongTiles(9), MahjongTiles(9), MahjongTiles(9),
            MahjongTiles(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.pure_suit())

    def test_13_orphans(self):
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(9),  # 1 and 9 of Characters
            MahjongTiles(10), MahjongTiles(18),  # 1 and 9 of Bamboos
            MahjongTiles(19), MahjongTiles(27),  # 1 and 9 of Dots
            MahjongTiles(28), MahjongTiles(29), MahjongTiles(30), MahjongTiles(31),  # Winds
            MahjongTiles(32), MahjongTiles(33), MahjongTiles(34),  # Dragons
            MahjongTiles(1)  # Pair of 1 of Characters
        ]
        self.assertTrue(self.calculator.thirteen_orphans())

    def test_not_13_orphans(self):
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1),  # 1 and 9 of Characters
            MahjongTiles(10), MahjongTiles(18),  # 1 and 9 of Bamboos
            MahjongTiles(19), MahjongTiles(27),  # 1 and 9 of Dots
            MahjongTiles(28), MahjongTiles(29), MahjongTiles(30), MahjongTiles(31),  # Winds
            MahjongTiles(32), MahjongTiles(33), MahjongTiles(34),  # Dragons
            MahjongTiles(1)  # Pair of 1 of Characters
        ]
        self.assertFalse(self.calculator.thirteen_orphans())

    def test_great_4_winds_hand(self):
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(30), MahjongTiles(30), MahjongTiles(30)),  # West Pong
            (MahjongTiles(31), MahjongTiles(31), MahjongTiles(31)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1)  # Pair of 1 of Characters
        ]
        self.assertTrue(self.calculator.great_4_winds_hand())
    
    def test_great_4_winds_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(30), MahjongTiles(30), MahjongTiles(30)),  # West Pong
            (MahjongTiles(2), MahjongTiles(3), MahjongTiles(4)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1)  # Pair of 1 of Characters
        ]
        self.assertFalse(self.calculator.great_4_winds_hand())

    def test_all_kong_hand(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Kong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Kong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3), MahjongTiles(3)),  # Kong of 3 Characters
            (MahjongTiles(4), MahjongTiles(4), MahjongTiles(4), MahjongTiles(4))  # Kong of 4 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(5)  # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.all_kong_hand())
    
    def test_all_kong_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Kong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Kong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3), MahjongTiles(3)),  # Kong of 3 Characters
            (MahjongTiles(4), MahjongTiles(4), MahjongTiles(4))
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(5)
        ]
        self.assertFalse(self.calculator.all_kong_hand())

    def test_4_hidden_pongs(self):
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),  # Pong of 1 Characters
            MahjongTiles(2), MahjongTiles(2), MahjongTiles(2),  # Pong of 2 Characters
            MahjongTiles(3), MahjongTiles(3), MahjongTiles(3),  # Pong of 3 Characters
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.four_hidden_pong())
    
    def test_4_hidden_pongs_false(self):
        self.calculator.called_tuples = [
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),  # Pong of 1 Characters
            MahjongTiles(2), MahjongTiles(2), MahjongTiles(2),  # Pong of 2 Characters
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(3),  # Pong of 3 Characters
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        self.assertFalse(self.calculator.four_hidden_pong())

if __name__ == '__main__':
    unittest.main(verbosity=2)