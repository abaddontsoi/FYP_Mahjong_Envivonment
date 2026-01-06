import Player
import MahjongTiles
import random

class BotPlayer(Player.Player):
    def __init__(self, id):
        super().__init__(id)

    def discard(self):
        return self.hand.pop(random.randint(0, len(self.hand) - 1))
    
    def call_response(self, call_tile: MahjongTiles.MahjongTiles, chow_allowed = False):
        # Put those selected mahjong tiles to self.called_tuples, responses are: 
        # 'win'
        # 'kong'
        # 'pong'
        # 'chow'
        return False