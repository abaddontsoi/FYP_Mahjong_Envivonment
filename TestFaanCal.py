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
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),  # Chow
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)                     # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
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

    def test_all_chow_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),  # Chow of 1-2-3 Characters
            (MahjongTiles(2), MahjongTiles(3), MahjongTiles(4)),  # Chow of 2-3-4 Characters
            (MahjongTiles(3), MahjongTiles(4), MahjongTiles(5))   # Chow of 3-4-5 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(4), MahjongTiles(5), MahjongTiles(6),  # Chow of 4-5-6 Characters
            MahjongTiles(7), MahjongTiles(7)                     # Pair of 7 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_chow_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),  # Chow of 1-2-3 Characters
            MahjongTiles(30), MahjongTiles(30),                     # Pair of 7 Characters
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(4),  # Chow of 2-3-4 Characters
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),  # Chow of 3-4-5 Characters
            MahjongTiles(4), MahjongTiles(5), MahjongTiles(6),  # Chow of 4-5-6 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)  
        self.assertTrue(self.calculator.all_chow_hand())

    def test_all_chow_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),  # Chow of 1-2-3 Characters
            (MahjongTiles(2), MahjongTiles(3), MahjongTiles(4)),  # Chow of 2-3-4 Characters
            (MahjongTiles(4), MahjongTiles(4), MahjongTiles(4))
        ]
        self.calculator.hand = [
            
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),
            MahjongTiles(30), MahjongTiles(30)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.all_chow_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),  # Chow of 1-2-3 Characters
            MahjongTiles(30), MahjongTiles(30),                     # Pair of 7 Characters
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Chow of 2-3-4 Characters
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),  # Chow of 3-4-5 Characters
            MahjongTiles(4), MahjongTiles(5), MahjongTiles(6),  # Chow of 4-5-6 Characters
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)  
        self.assertFalse(self.calculator.all_chow_hand())

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

    def test_little_dragon_hand(self):
        # No call
        self.calculator.hand = [
            MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32), # Red Dragon Pong
            MahjongTiles(33), MahjongTiles(33),  # White Dragon Pair
            MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34),  # Green Dragon Pong
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.little_dragon_hand())

        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32)), # Red Dragon Pong
            (MahjongTiles(34), MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34)), # Red Dragon Kong
        ]
        self.calculator.hand = [
            MahjongTiles(33), MahjongTiles(33),  # White Dragon Pairg
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.little_dragon_hand())

    def test_little_dragon_hand_false(self):
        self.calculator.hand = [
            MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32), # Red Dragon Pong
            MahjongTiles(33), MahjongTiles(33), MahjongTiles(33),  # White Dragon Pong
            MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34),  # Green Dragon Pong
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())
        
        self.calculator.called_tuples = [
            (MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32)), # Red Dragon Pong
            (MahjongTiles(33), MahjongTiles(33), MahjongTiles(33)),  # White Dragon Pong
            (MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())

        self.calculator.called_tuples = [
            (MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32)), # Red Dragon Pong
            (MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(13), MahjongTiles(14), MahjongTiles(15),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.little_dragon_hand())

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

        self.calculator.called_tuples = []
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

    def test_great_dragon_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32)), # Red Dragon Pong
            (MahjongTiles(33), MahjongTiles(33),  MahjongTiles(33)), # White Dragon Pong
            (MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34)),  # Green Dragon Pong
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.great_dragon_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32), # Red Dragon Pong
            MahjongTiles(33), MahjongTiles(33),  MahjongTiles(33), # White Dragon Pong 
            MahjongTiles(34), MahjongTiles(34),  MahjongTiles(34),  # Green Dragon Pong
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.great_dragon_hand())

    def test_great_dragon_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32)), # Red Dragon Pong
            (MahjongTiles(33), MahjongTiles(33),  MahjongTiles(33)), # White Dragon Pong
            (MahjongTiles(1), MahjongTiles(2),  MahjongTiles(3)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.great_dragon_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(32), MahjongTiles(32),  MahjongTiles(32), # Red Dragon Pong
            MahjongTiles(33), MahjongTiles(33),  MahjongTiles(33), # White Dragon Pong 
            MahjongTiles(1), MahjongTiles(2),  MahjongTiles(3),  # Chow
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),  # Chow
            MahjongTiles(8), MahjongTiles(8)  # Pair
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.great_dragon_hand())

    def test_pure_orphans_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(9), MahjongTiles(9), MahjongTiles(9), MahjongTiles(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Sok
            MahjongTiles(27), MahjongTiles(27), MahjongTiles(27),  # Pong of 9 Sok
            MahjongTiles(10), MahjongTiles(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.pure_orphans_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),  # Pong of 1 Characters
            MahjongTiles(9), MahjongTiles(9), MahjongTiles(9),  # Pong of 9 Characters
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Sok
            MahjongTiles(27), MahjongTiles(27), MahjongTiles(27),  # Pong of 9 Sok
            MahjongTiles(10), MahjongTiles(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.pure_orphans_hand())

    def test_pure_orphans_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(9), MahjongTiles(9), MahjongTiles(9), MahjongTiles(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Sok
            MahjongTiles(25), MahjongTiles(26), MahjongTiles(27),  # Chow 7-8-9 of Sok
            MahjongTiles(10), MahjongTiles(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())
        
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),  # Pong of 1 Characters
            (MahjongTiles(9), MahjongTiles(9), MahjongTiles(9), MahjongTiles(9))  # Pong of 9 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Sok
            MahjongTiles(27), MahjongTiles(27), MahjongTiles(27),  # Pong of 9 Sok
            MahjongTiles(10), MahjongTiles(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),  # Pong of 1 Characters
            MahjongTiles(9), MahjongTiles(9), MahjongTiles(9),  # Pong of 9 Characters
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),  # Pong of 1 Sok
            MahjongTiles(25), MahjongTiles(26), MahjongTiles(27),  # Chow 7-8-9 of Sok
            MahjongTiles(10), MahjongTiles(10)  # Pair of 1p
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.pure_orphans_hand())

    def test_all_winds_and_dragons(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(32), MahjongTiles(32), MahjongTiles(32)),  # White Pong
        ]
        self.calculator.hand = [
            MahjongTiles(31), MahjongTiles(31), MahjongTiles(31),  # North Pong
            MahjongTiles(34), MahjongTiles(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_winds_and_dragons())
        
        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # East Pong
            MahjongTiles(29), MahjongTiles(29), MahjongTiles(29),  # South Pong
            MahjongTiles(30), MahjongTiles(30), MahjongTiles(30),  # West Pong
            MahjongTiles(31), MahjongTiles(31), MahjongTiles(31),  # North Pong
            MahjongTiles(34), MahjongTiles(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.all_winds_and_dragons())

    def test_all_winds_and_dragons_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(3), MahjongTiles(4), MahjongTiles(5)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTiles(31), MahjongTiles(31), MahjongTiles(31),  # North Pong
            MahjongTiles(34), MahjongTiles(34)  # Pair of Red Dragon
        ]
        self.assertFalse(self.calculator.all_winds_and_dragons())
        
        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # East Pong
            MahjongTiles(29), MahjongTiles(29), MahjongTiles(29),  # South Pong
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),  # Chow
            MahjongTiles(31), MahjongTiles(31), MahjongTiles(31),  # North Pong
            MahjongTiles(34), MahjongTiles(34)  # Pair of Red Dragon
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.all_winds_and_dragons())

    def test_nine_gates_to_haven(self):
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(4),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),
            MahjongTiles(8), MahjongTiles(9), MahjongTiles(9),
            MahjongTiles(9), MahjongTiles(5)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())
        
        self.calculator.hand = [
            MahjongTiles(10), MahjongTiles(10), MahjongTiles(10),
            MahjongTiles(11), MahjongTiles(12), MahjongTiles(13),
            MahjongTiles(14), MahjongTiles(15), MahjongTiles(16),
            MahjongTiles(17), MahjongTiles(18), MahjongTiles(18),
            MahjongTiles(18), MahjongTiles(14)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())
        
        self.calculator.hand = [
            MahjongTiles(19), MahjongTiles(19), MahjongTiles(19),
            MahjongTiles(20), MahjongTiles(21), MahjongTiles(22),
            MahjongTiles(23), MahjongTiles(24), MahjongTiles(25),
            MahjongTiles(26), MahjongTiles(27), MahjongTiles(27),
            MahjongTiles(27), MahjongTiles(23)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertTrue(self.calculator.nine_gates_to_haven())

    def test_nine_gates_to_haven_false(self):
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),
        ]
        self.calculator.hand = [
            MahjongTiles(2), MahjongTiles(3), MahjongTiles(4),
            MahjongTiles(5), MahjongTiles(6), MahjongTiles(7),
            MahjongTiles(8), MahjongTiles(9), MahjongTiles(9),
            MahjongTiles(9), MahjongTiles(6)
        ]
        self.calculator.hand.sort(key=lambda x: x.classId)
        self.assertFalse(self.calculator.nine_gates_to_haven())

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

    def test_13_orphans_false(self):
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1),  # 1 and 9 of Characters
            MahjongTiles(10), MahjongTiles(18),  # 1 and 9 of Bamboos
            MahjongTiles(19), MahjongTiles(27),  # 1 and 9 of Dots
            MahjongTiles(28), MahjongTiles(29), MahjongTiles(30), MahjongTiles(31),  # Winds
            MahjongTiles(32), MahjongTiles(33), MahjongTiles(34),  # Dragons
            MahjongTiles(1)  # Pair of 1 of Characters
        ]
        self.assertFalse(self.calculator.thirteen_orphans())

    def test_little_4_winds_hand(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(30), MahjongTiles(30), MahjongTiles(30)),  # West Pong
        ]
        self.calculator.hand = [
            MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5),# Chow
            MahjongTiles(31), MahjongTiles(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5)), # Chow
        ]
        self.calculator.hand = [
            MahjongTiles(30), MahjongTiles(30), MahjongTiles(30),  # West Pong
            MahjongTiles(31), MahjongTiles(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # East Pong
            MahjongTiles(29), MahjongTiles(29), MahjongTiles(29),  # South Pong
            MahjongTiles(30), MahjongTiles(30), MahjongTiles(30),  # West Pong
            MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5),# Chow
            MahjongTiles(31), MahjongTiles(31)  # Pair of North
        ]
        self.assertTrue(self.calculator.little_4_winds_hand())

    def test_little_4_winds_hand_false(self):
        # Called
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5)), # Chow
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),  # Not West Pong
            MahjongTiles(31), MahjongTiles(31)  # Pair of North
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

        # No call
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(28), MahjongTiles(28), MahjongTiles(28),  # East Pong
            MahjongTiles(29), MahjongTiles(29), MahjongTiles(29),  # South Pong
            MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5),# Chow
            MahjongTiles(3),  MahjongTiles(4), MahjongTiles(5),# Chow
            MahjongTiles(31), MahjongTiles(31)  # Pair of North, missing West Pong
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

        # Greate 4 wind case
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(29), MahjongTiles(29), MahjongTiles(29)),  # South Pong
            (MahjongTiles(30), MahjongTiles(30), MahjongTiles(30)),  # West Pong
            (MahjongTiles(31), MahjongTiles(31), MahjongTiles(31)),  # North Pong
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1)  # Pair of North
        ]
        self.assertFalse(self.calculator.little_4_winds_hand())

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

    def test_faan_list(self):
        # No call, all chow hand, self drawn
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(2), MahjongTiles(3),
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),
            MahjongTiles(17), MahjongTiles(18), MahjongTiles(16),
            MahjongTiles(17), MahjongTiles(18), MahjongTiles(16),
            MahjongTiles(28), MahjongTiles(28)
        ]
        self.calculator.self_drawn_flag = True
        self.calculator.hand.sort(key=lambda x: x.classId)
        expected_faan = [('all_chow_hand', 1), ('self_drawn', 1), ('no_call', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        
        # No call, green, self drawn
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(33), MahjongTiles(33), MahjongTiles(33),
            MahjongTiles(3), MahjongTiles(4), MahjongTiles(5),
            MahjongTiles(17), MahjongTiles(18), MahjongTiles(16),
            MahjongTiles(17), MahjongTiles(18), MahjongTiles(16),
            MahjongTiles(28), MahjongTiles(28)
        ]
        self.calculator.self_drawn_flag = True
        self.calculator.hand.sort(key=lambda x: x.classId)
        expected_faan = [('green', 1), ('self_drawn', 1), ('no_call', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Round wind and round position
        self.calculator.called_tuples = [
            (MahjongTiles(28), MahjongTiles(28), MahjongTiles(28)),  # East Pong
            (MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)),  # Chow
        ]
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), 
            MahjongTiles(2), MahjongTiles(2),
            MahjongTiles(3), MahjongTiles(3),
            MahjongTiles(4), MahjongTiles(4)
        ]
        self.calculator.round = 0
        self.calculator.position = 0
        expected_faan = [('round_wind', 1), ('round_position', 1), ('clean_hand', 3)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Pure suit
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Pong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(6), MahjongTiles(7), MahjongTiles(8),  # Chow of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        
        # Pure suit and all chow hand
        self.calculator.called_tuples = []
        self.calculator.hand = [
            MahjongTiles(1), MahjongTiles(1), MahjongTiles(1),
            MahjongTiles(2), MahjongTiles(2), MahjongTiles(2),
            MahjongTiles(3), MahjongTiles(3), MahjongTiles(3),
            MahjongTiles(6), MahjongTiles(7), MahjongTiles(8),  # Chow of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('pure_suit', 7), ('all_chow_hand', 1)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

        # Pure Suit and All Pong Hand
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Pong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Pong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3))   # Pong of 3 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(4), MahjongTiles(4), MahjongTiles(4),  # Pong of 4 Characters
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('all_pong_hand', 3), ('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)
        
        # Pure Suit and All Kong Hand
        self.calculator.called_tuples = [
            (MahjongTiles(1), MahjongTiles(1), MahjongTiles(1), MahjongTiles(1)),  # Kong of 1 Characters
            (MahjongTiles(2), MahjongTiles(2), MahjongTiles(2), MahjongTiles(2)),  # Kong of 2 Characters
            (MahjongTiles(3), MahjongTiles(3), MahjongTiles(3), MahjongTiles(3)),   # Kong of 3 Characters
            (MahjongTiles(4), MahjongTiles(4), MahjongTiles(4), MahjongTiles(4))   # Kong of 4 Characters
        ]
        self.calculator.hand = [
            MahjongTiles(5), MahjongTiles(5)                     # Pair of 5 Characters
        ]
        expected_faan = [('all_kong_hand', 10), ('pure_suit', 7)]
        faan_result = self.calculator.check_faan_match()
        for faan in expected_faan:
            self.assertIn(faan, faan_result)

if __name__ == '__main__':
    unittest.main(verbosity=2)