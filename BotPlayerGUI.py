from PlayerGUI import PlayerGUI
import MahjongTiles
import random

class BotPlayerGUI(PlayerGUI):
    def __init__(self, id = None):
        super().__init__(id)

    def discard(self):
        return self.hand.pop(random.randint(0, len(self.hand) - 1))

    def check_possible_calls(self, call_tile: MahjongTiles.MahjongTiles, chow_allowed = False):
        actions = []
        
        return actions

    def display_hand(self):
        return