import unittest
from unittest.mock import patch, MagicMock, Mock
import sys

from FaanCalculator import FaanCalculator
sys.path.insert(0, '.')
from MahjongTile import MahjongTile


class TestFaanCal(unittest.TestCase):

    def setUp(self):
        self.calculator = FaanCalculator(0, 0)

    def test_is_valid_winning_hand(self):
        self.calculator.hand = [
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong
            MahjongTile(1), MahjongTile(2), MahjongTile(3),  # Chow
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)                     # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.is_valid_winning_hand())

    def test_red_white_green(self):
        self.calculator.hand = [
            MahjongTile(32), MahjongTile(32),  MahjongTile(32), # Red Dragon Pong
            MahjongTile(33), MahjongTile(33), MahjongTile(33),  # White Dragon Pong
            MahjongTile(34), MahjongTile(34), MahjongTile(34),  # Green Dragon Pong
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)                     # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.red())
        self.assertTrue(self.calculator.white())
        self.assertTrue(self.calculator.green())

    def test_red_white_green_false(self):
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(2),  MahjongTile(2),
            MahjongTile(3), MahjongTile(3), MahjongTile(3),
            MahjongTile(5), MahjongTile(6), MahjongTile(7),
            MahjongTile(5), MahjongTile(6), MahjongTile(7),
            MahjongTile(8), MahjongTile(8)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.red())
        self.assertFalse(self.calculator.white())
        self.assertFalse(self.calculator.green())

    def test_round_wind(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.round = i
            self.calculator.hand = [
                MahjongTile(28 + i), MahjongTile(28 + i), MahjongTile(28 + i),  # Pong of round wind
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(15), MahjongTile(15), MahjongTile(15),  # Pong
                MahjongTile(8), MahjongTile(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertTrue(self.calculator.round_wind())
    
    def test_round_wind_false(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.round = i
            self.calculator.hand = [
                MahjongTile(28 - i - 1), MahjongTile(28 - i), MahjongTile(28 - i),
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(15), MahjongTile(15), MahjongTile(15),  # Pong
                MahjongTile(8), MahjongTile(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertFalse(self.calculator.round_wind())

    def test_round_position(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.position = i
            self.calculator.hand = [
                MahjongTile(28 + i), MahjongTile(28 + i), MahjongTile(28 + i),  # Pong of position wind
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(15), MahjongTile(15), MahjongTile(15),  # Pong
                MahjongTile(8), MahjongTile(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertTrue(self.calculator.round_position())

    def test_round_position_false(self):
        for i in [0, 1, 2, 3]:  # East, South, West, North
            self.calculator.position = i
            self.calculator.hand = [
                MahjongTile(28 - i - 1), MahjongTile(28 - i - 1), MahjongTile(28 - i - 1),  # Pong of position wind
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
                MahjongTile(15), MahjongTile(15), MahjongTile(15),  # Pong
                MahjongTile(8), MahjongTile(8)                     # Pair
            ]
            self.calculator.hand.sort(key=lambda x: x.classId)
            self.assertFalse(self.calculator.round_position())

    def test_mixed_orphans(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(9), MahjongTile(9), MahjongTile(9), MahjongTile(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Characters
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # Pong of 1 Characters
            MahjongTile(30), MahjongTile(30)  # Pair of 5 of Characters
        ]
        self.assertTrue(self.calculator.mixed_orphans())

    def test_mixed_orphans_false(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(9), MahjongTile(9), MahjongTile(9), MahjongTile(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Characters
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # Pong of 1 Characters
            MahjongTile(3), MahjongTile(3)  # Pair of 5 of Characters
        ]
        self.assertFalse(self.calculator.mixed_orphans())

    def test_all_chow_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),  # Chow of 1-2-3 Characters
            (MahjongTile(2), MahjongTile(3), MahjongTile(4)),  # Chow of 2-3-4 Characters
            (MahjongTile(3), MahjongTile(4), MahjongTile(5))   # Chow of 3-4-5 Characters
        ]
        self.calculator.hand = [
            MahjongTile(4), MahjongTile(5), MahjongTile(6),  # Chow of 4-5-6 Characters
            MahjongTile(7), MahjongTile(7)                     # Pair of 7 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_chow_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),  # Chow of 1-2-3 Characters
            MahjongTile(30), MahjongTile(30),                     # Pair of 7 Characters
            MahjongTile(2), MahjongTile(3), MahjongTile(4),  # Chow of 2-3-4 Characters
            MahjongTile(3), MahjongTile(4), MahjongTile(5),  # Chow of 3-4-5 Characters
            MahjongTile(4), MahjongTile(5), MahjongTile(6),  # Chow of 4-5-6 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)  
        self.assertTrue(self.calculator.all_chow_hand())

    def test_all_chow_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),  # Chow of 1-2-3 Characters
            (MahjongTile(2), MahjongTile(3), MahjongTile(4)),  # Chow of 2-3-4 Characters
            (MahjongTile(4), MahjongTile(4), MahjongTile(4))
        ]
        self.calculator.hand = [
            
            MahjongTile(3), MahjongTile(4), MahjongTile(5),
            MahjongTile(30), MahjongTile(30)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.all_chow_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),  # Chow of 1-2-3 Characters
            MahjongTile(30), MahjongTile(30),                     # Pair of 7 Characters
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Chow of 2-3-4 Characters
            MahjongTile(3), MahjongTile(4), MahjongTile(5),  # Chow of 3-4-5 Characters
            MahjongTile(4), MahjongTile(5), MahjongTile(6),  # Chow of 4-5-6 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)  
        self.assertFalse(self.calculator.all_chow_hand())

    def test_all_pong_hand(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.all_pong_hand())
    
    def test_all_pong_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),  # Chow of 1-2-3 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        self.assertFalse(self.calculator.all_pong_hand())

    def test_clean_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),
            (MahjongTile(4), MahjongTile(5), MahjongTile(6)),
            (MahjongTile(7), MahjongTile(8), MahjongTile(9)),
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),
        ]
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.clean_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),
            MahjongTile(4), MahjongTile(5), MahjongTile(6),
            MahjongTile(7), MahjongTile(8), MahjongTile(9),
            MahjongTile(28), MahjongTile(28), MahjongTile(28),
            MahjongTile(31), MahjongTile(31)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.clean_hand())

    def test_clean_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),
            (MahjongTile(4), MahjongTile(5), MahjongTile(6)),
            (MahjongTile(7), MahjongTile(8), MahjongTile(9)),
            (MahjongTile(11), MahjongTile(11), MahjongTile(11)),
        ]
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.clean_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),
            MahjongTile(4), MahjongTile(5), MahjongTile(6),
            MahjongTile(7), MahjongTile(8), MahjongTile(9),
            MahjongTile(11), MahjongTile(11), MahjongTile(11),
            MahjongTile(31), MahjongTile(31)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.clean_hand())

    def test_little_dragon_hand(self):
        # No call
        self.calculator.hand = [
            MahjongTile(32), MahjongTile(32),  MahjongTile(32), # Red Dragon Pong
            MahjongTile(33), MahjongTile(33),  # White Dragon Pair
            MahjongTile(34), MahjongTile(34),  MahjongTile(34),  # Green Dragon Pong
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.little_dragon_hand())

        # Called
        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(34), MahjongTile(34), MahjongTile(34),  MahjongTile(34)), # Red Dragon Kong
        ]
        self.calculator.hand = [
            MahjongTile(33), MahjongTile(33),  # White Dragon Pairg
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.little_dragon_hand())

    def test_little_dragon_hand_false(self):
        self.calculator.hand = [
            MahjongTile(32), MahjongTile(32),  MahjongTile(32), # Red Dragon Pong
            MahjongTile(33), MahjongTile(33), MahjongTile(33),  # White Dragon Pong
            MahjongTile(34), MahjongTile(34),  MahjongTile(34),  # Green Dragon Pong
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())
        
        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(33), MahjongTile(33), MahjongTile(33)),  # White Dragon Pong
            (MahjongTile(34), MahjongTile(34),  MahjongTile(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())

        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(34), MahjongTile(34),  MahjongTile(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(13), MahjongTile(14), MahjongTile(15),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())

    def test_pure_suit(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),
            (MahjongTile(4), MahjongTile(5), MahjongTile(6)),
            (MahjongTile(7), MahjongTile(8), MahjongTile(9)),
            (MahjongTile(7), MahjongTile(8), MahjongTile(9)),
        ]
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.pure_suit())

        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),
            MahjongTile(2), MahjongTile(3), MahjongTile(4),
            MahjongTile(5), MahjongTile(6), MahjongTile(7), MahjongTile(8), 
            MahjongTile(9), MahjongTile(9), MahjongTile(9),
            MahjongTile(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertTrue(self.calculator.pure_suit())

    def test_pure_suit_false(self):
        self.calculator.called_tuples = [
            (
                MahjongTile(1), MahjongTile(1), MahjongTile(1),
            ),
            (
                MahjongTile(11), MahjongTile(11), MahjongTile(11),
            ),
        ]
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(3), MahjongTile(4),
            MahjongTile(5), MahjongTile(6), MahjongTile(7), MahjongTile(8), 
            MahjongTile(9), MahjongTile(9), MahjongTile(9),
            MahjongTile(2)
        ]
        self.assertTrue(self.calculator.is_valid_winning_hand())
        self.assertFalse(self.calculator.pure_suit())

    def test_great_dragon_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(33), MahjongTile(33),  MahjongTile(33)), # White Dragon Pong
            (MahjongTile(34), MahjongTile(34),  MahjongTile(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.great_dragon_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(32), MahjongTile(32),  MahjongTile(32), # Red Dragon Pong
            MahjongTile(33), MahjongTile(33),  MahjongTile(33), # White Dragon Pong 
            MahjongTile(34), MahjongTile(34),  MahjongTile(34),  # Green Dragon Pong
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.great_dragon_hand())

    def test_great_dragon_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(33), MahjongTile(33),  MahjongTile(33)), # White Dragon Pong
            (MahjongTile(1), MahjongTile(2),  MahjongTile(3)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.great_dragon_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(32), MahjongTile(32),  MahjongTile(32), # Red Dragon Pong
            MahjongTile(33), MahjongTile(33),  MahjongTile(33), # White Dragon Pong 
            MahjongTile(1), MahjongTile(2),  MahjongTile(3),  # Chow
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.great_dragon_hand())

    def test_pure_orphans_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(9), MahjongTile(9), MahjongTile(9), MahjongTile(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Sok
            MahjongTile(27), MahjongTile(27), MahjongTile(27),  # Pong of 9 Sok
            MahjongTile(10), MahjongTile(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.pure_orphans_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),  # Pong of 1 Characters
            MahjongTile(9), MahjongTile(9), MahjongTile(9),  # Pong of 9 Characters
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Sok
            MahjongTile(27), MahjongTile(27), MahjongTile(27),  # Pong of 9 Sok
            MahjongTile(10), MahjongTile(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.pure_orphans_hand())

    def test_pure_orphans_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(9), MahjongTile(9), MahjongTile(9), MahjongTile(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Sok
            MahjongTile(25), MahjongTile(26), MahjongTile(27),  # Chow 7-8-9 of Sok
            MahjongTile(10), MahjongTile(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())
        
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),  # Pong of 1 Characters
            (MahjongTile(9), MahjongTile(9), MahjongTile(9), MahjongTile(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Sok
            MahjongTile(27), MahjongTile(27), MahjongTile(27),  # Pong of 9 Sok
            MahjongTile(10), MahjongTile(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),  # Pong of 1 Characters
            MahjongTile(9), MahjongTile(9), MahjongTile(9),  # Pong of 9 Characters
            MahjongTile(19), MahjongTile(19), MahjongTile(19),  # Pong of 1 Sok
            MahjongTile(25), MahjongTile(26), MahjongTile(27),  # Chow 7-8-9 of Sok
            MahjongTile(10), MahjongTile(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())

    def test_all_winds_and_dragons(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(32), MahjongTile(32), MahjongTile(32)),  # White Pong
        ]
        self.calculator.hand = [
            MahjongTile(31), MahjongTile(31), MahjongTile(31),  # North Pong
            MahjongTile(34), MahjongTile(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_winds_and_dragons())
        
        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # East Pong
            MahjongTile(29), MahjongTile(29), MahjongTile(29),  # South Pong
            MahjongTile(30), MahjongTile(30), MahjongTile(30),  # West Pong
            MahjongTile(31), MahjongTile(31), MahjongTile(31),  # North Pong
            MahjongTile(34), MahjongTile(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_winds_and_dragons())

    def test_all_winds_and_dragons_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(3), MahjongTile(4), MahjongTile(5)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTile(31), MahjongTile(31), MahjongTile(31),  # North Pong
            MahjongTile(34), MahjongTile(34)  # Pair of Red Dragon
        ]
        self.assertFalse(self.calculator.all_winds_and_dragons())
        
        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # East Pong
            MahjongTile(29), MahjongTile(29), MahjongTile(29),  # South Pong
            MahjongTile(3), MahjongTile(4), MahjongTile(5),  # Chow
            MahjongTile(31), MahjongTile(31), MahjongTile(31),  # North Pong
            MahjongTile(34), MahjongTile(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.all_winds_and_dragons())

    def test_nine_gates_to_haven(self):
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),
            MahjongTile(2), MahjongTile(3), MahjongTile(4),
            MahjongTile(5), MahjongTile(6), MahjongTile(7),
            MahjongTile(8), MahjongTile(9), MahjongTile(9),
            MahjongTile(9), MahjongTile(5)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())
        
        self.calculator.hand = [
            MahjongTile(10), MahjongTile(10), MahjongTile(10),
            MahjongTile(11), MahjongTile(12), MahjongTile(13),
            MahjongTile(14), MahjongTile(15), MahjongTile(16),
            MahjongTile(17), MahjongTile(18), MahjongTile(18),
            MahjongTile(18), MahjongTile(14)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())
        
        self.calculator.hand = [
            MahjongTile(19), MahjongTile(19), MahjongTile(19),
            MahjongTile(20), MahjongTile(21), MahjongTile(22),
            MahjongTile(23), MahjongTile(24), MahjongTile(25),
            MahjongTile(26), MahjongTile(27), MahjongTile(27),
            MahjongTile(27), MahjongTile(23)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())

    def test_nine_gates_to_haven_false(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),
        ]
        self.calculator.hand = [
            MahjongTile(2), MahjongTile(3), MahjongTile(4),
            MahjongTile(5), MahjongTile(6), MahjongTile(7),
            MahjongTile(8), MahjongTile(9), MahjongTile(9),
            MahjongTile(9), MahjongTile(6)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.nine_gates_to_haven())

    def test_13_orphans(self):
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(9),  # 1 and 9 of Characters
            MahjongTile(10), MahjongTile(18),  # 1 and 9 of Bamboos
            MahjongTile(19), MahjongTile(27),  # 1 and 9 of Dots
            MahjongTile(28), MahjongTile(29), MahjongTile(30), MahjongTile(31),  # Winds
            MahjongTile(32), MahjongTile(33), MahjongTile(34),  # Dragons
            MahjongTile(1)  # Pair of 1 of Characters
        ]
        self.assertTrue(self.calculator.thirteen_orphans())

    def test_13_orphans_false(self):
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1),  # 1 and 9 of Characters
            MahjongTile(10), MahjongTile(18),  # 1 and 9 of Bamboos
            MahjongTile(19), MahjongTile(27),  # 1 and 9 of Dots
            MahjongTile(28), MahjongTile(29), MahjongTile(30), MahjongTile(31),  # Winds
            MahjongTile(32), MahjongTile(33), MahjongTile(34),  # Dragons
            MahjongTile(1)  # Pair of 1 of Characters
        ]
        self.assertFalse(self.calculator.thirteen_orphans())

    def test_little_4_winds_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(30), MahjongTile(30), MahjongTile(30)),  # West Pong
        ]
        self.calculator.hand = [
            MahjongTile(3),  MahjongTile(4), MahjongTile(5),# Chow
            MahjongTile(31), MahjongTile(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

        # Called
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(3),  MahjongTile(4), MahjongTile(5)), # Chow
        ]
        self.calculator.hand = [
            MahjongTile(30), MahjongTile(30), MahjongTile(30),  # West Pong
            MahjongTile(31), MahjongTile(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # East Pong
            MahjongTile(29), MahjongTile(29), MahjongTile(29),  # South Pong
            MahjongTile(30), MahjongTile(30), MahjongTile(30),  # West Pong
            MahjongTile(3),  MahjongTile(4), MahjongTile(5),# Chow
            MahjongTile(31), MahjongTile(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

    def test_little_4_winds_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(3),  MahjongTile(4), MahjongTile(5)), # Chow
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),  # Not West Pong
            MahjongTile(31), MahjongTile(31)  # Pair of North
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(28), MahjongTile(28), MahjongTile(28),  # East Pong
            MahjongTile(29), MahjongTile(29), MahjongTile(29),  # South Pong
            MahjongTile(3),  MahjongTile(4), MahjongTile(5),# Chow
            MahjongTile(3),  MahjongTile(4), MahjongTile(5),# Chow
            MahjongTile(31), MahjongTile(31)  # Pair of North, missing West Pong
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

        # Greate 4 wind case
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(30), MahjongTile(30), MahjongTile(30)),  # West Pong
            (MahjongTile(31), MahjongTile(31), MahjongTile(31)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1)  # Pair of North
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

    def test_great_4_winds_hand(self):
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(30), MahjongTile(30), MahjongTile(30)),  # West Pong
            (MahjongTile(31), MahjongTile(31), MahjongTile(31)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1)  # Pair of 1 of Characters
        ]
        self.assertTrue(self.calculator.great_4_winds_hand())
    
    def test_great_4_winds_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(29), MahjongTile(29), MahjongTile(29)),  # South Pong
            (MahjongTile(30), MahjongTile(30), MahjongTile(30)),  # West Pong
            (MahjongTile(2), MahjongTile(3), MahjongTile(4)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1)  # Pair of 1 of Characters
        ]
        self.assertFalse(self.calculator.great_4_winds_hand())

    def test_all_kong_hand(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Kong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Kong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3), MahjongTile(3)),  # Kong of 3 Characters
            (MahjongTile(4), MahjongTile(4), MahjongTile(4), MahjongTile(4))  # Kong of 4 Characters
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(5)  # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.all_kong_hand())
    
    def test_all_kong_hand_false(self):
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Kong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Kong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3), MahjongTile(3)),  # Kong of 3 Characters
            (MahjongTile(4), MahjongTile(4), MahjongTile(4))
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(5)
        ]
        self.assertFalse(self.calculator.all_kong_hand())

    def test_4_hidden_pongs(self):
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),  # Pong of 1 Characters
            MahjongTile(2), MahjongTile(2), MahjongTile(2),  # Pong of 2 Characters
            MahjongTile(3), MahjongTile(3), MahjongTile(3),  # Pong of 3 Characters
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        self.assertTrue(self.calculator.four_hidden_pong())
    
    def test_4_hidden_pongs_false(self):
        self.calculator.called_tuples = [
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),  # Pong of 1 Characters
            MahjongTile(2), MahjongTile(2), MahjongTile(2),  # Pong of 2 Characters
            MahjongTile(2), MahjongTile(3), MahjongTile(3),  # Pong of 3 Characters
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        self.assertFalse(self.calculator.four_hidden_pong())

    def test_faan_list(self):
        # No call, all chow hand, self drawn
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),
            MahjongTile(3), MahjongTile(4), MahjongTile(5),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(28), MahjongTile(28)
        ]
        self.calculator.self_drawn_flag = True
        self.calculator.hand.sort(key=lambda x: x.classId)
        expected_faan = [('all_chow_hand', 1), ('self_drawn', 1), ('no_call', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        self.calculator.self_drawn_flag = False
        
        # No call, green, self drawn
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(33), MahjongTile(33), MahjongTile(33),
            MahjongTile(3), MahjongTile(4), MahjongTile(5),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(28), MahjongTile(28)
        ]
        self.calculator.self_drawn_flag = True
        self.calculator.hand.sort(key=lambda x: x.classId)
        expected_faan = [('green', 1), ('self_drawn', 1), ('no_call', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        self.calculator.self_drawn_flag = False

        self.calculator.self_drawn_on_last_tile_flag = True
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(2), MahjongTile(3),
            MahjongTile(3), MahjongTile(4), MahjongTile(5),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(17), MahjongTile(18), MahjongTile(16),
            MahjongTile(28), MahjongTile(28)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        expected_faan = [('all_chow_hand', 1), ('self_drawn_on_last_tile', 1), ('no_call', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        self.calculator.self_drawn_on_last_tile_flag = False

        # Round wind and round position
        self.calculator.called_tuples = [
            (MahjongTile(28), MahjongTile(28), MahjongTile(28)),  # East Pong
            (MahjongTile(1), MahjongTile(2), MahjongTile(3)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), 
            MahjongTile(2), MahjongTile(2),
            MahjongTile(3), MahjongTile(3),
            MahjongTile(4), MahjongTile(4)
        ]
        self.calculator.round = 0
        self.calculator.position = 0
        expected_faan = [('round_wind', 1), ('round_position', 1), ('clean_hand', 3)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Self drawn after kong
        self.calculator.self_drawn_flag = True
        self.calculator.consecutive_kong_count = 1
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Kong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(12), MahjongTile(13), MahjongTile(14),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('self_drawn_after_kong', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        self.calculator.self_drawn_flag = False
        self.calculator.consecutive_kong_count = 0

        # Just all pong hand
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(12), MahjongTile(12), MahjongTile(12),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('all_pong_hand', 3)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Pure suit
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(6), MahjongTile(7), MahjongTile(8),  # Chow of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        
        # Pure suit and all chow hand
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTile(1), MahjongTile(1), MahjongTile(1),
            MahjongTile(2), MahjongTile(2), MahjongTile(2),
            MahjongTile(3), MahjongTile(3), MahjongTile(3),
            MahjongTile(6), MahjongTile(7), MahjongTile(8),  # Chow of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('pure_suit', 7), ('all_chow_hand', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Pure Suit, All Pong Hand and self drawn after 2 kongs
        self.calculator.self_drawn_flag = True
        self.calculator.consecutive_kong_count = 2
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Pong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Pong of 2 Characters
            (MahjongTile(6), MahjongTile(7), MahjongTile(8))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTile(4), MahjongTile(4), MahjongTile(4),  # Pong of 4 Characters
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('self_drawn_after_2kong', 10), ('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        self.calculator.self_drawn_flag = False
        self.calculator.consecutive_kong_count = 0
        
        # Little/Great Dragon hand
        self.calculator.called_tuples = [
            (MahjongTile(32), MahjongTile(32),  MahjongTile(32)), # Red Dragon Pong
            (MahjongTile(33), MahjongTile(33),  MahjongTile(33)), # White Dragon Pong
            (MahjongTile(34), MahjongTile(34),  MahjongTile(34))  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(6), MahjongTile(7),  # Chow
            MahjongTile(8), MahjongTile(8)  # Pair
        ]
        expected_faan = [('great_dragon_hand', 10)]
        excluded_faan = ['little_dragon_hand', 'red', 'white', 'green']
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        for faan in excluded_faan:
            self.assertNotIn(faan, faan_result)
        
        # Pure Suit and All Kong Hand
        self.calculator.called_tuples = [
            (MahjongTile(1), MahjongTile(1), MahjongTile(1), MahjongTile(1)),  # Kong of 1 Characters
            (MahjongTile(2), MahjongTile(2), MahjongTile(2), MahjongTile(2)),  # Kong of 2 Characters
            (MahjongTile(3), MahjongTile(3), MahjongTile(3), MahjongTile(3)),   # Kong of 3 Characters
            (MahjongTile(4), MahjongTile(4), MahjongTile(4), MahjongTile(4))   # Kong of 4 Characters
        ]
        self.calculator.hand = [
            MahjongTile(5), MahjongTile(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('all_kong_hand', 10), ('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

if __name__ == '__main__':
    unittest.main(verbosity=2)