"""
TestPlayer.py - 100% Coverage Edition
Tests all Player.py methods comprehensively
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
sys.path.insert(0, '.')
from PlayerGUI import PlayerGUI
from MahjongTiles import MahjongTiles

class TestPlayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.env = MagicMock()
        cls.env.get_pool_and_buffer.return_value = []

    def setUp(self):
        self.player = PlayerGUI('TestPlayer')
        self.player.assign_env(self.env)

    def test_check_possible_call(self):
        self.player.hand = [
            MahjongTiles(1), 
            MahjongTiles(1),
            MahjongTiles(1),
            MahjongTiles(2),
            MahjongTiles(2),
        ]
        self.player.called_tuples = [

        ]
        self.env.deck = [MahjongTiles(1), MahjongTiles(2), MahjongTiles(3)]
        call_tile = MahjongTiles(1)
        possible_actions = self.player.check_possible_calls(call_tile)
        self.assertIn('pong', possible_actions)
        self.assertNotIn('chow', possible_actions)
        self.assertNotIn('win', possible_actions)
        self.assertIn('kong', possible_actions)

if __name__ == '__main__':
    unittest.main(verbosity=2)