from BotPlayerGUI import BotPlayerGUI
from MahjongTile import MahjongTile
from ModelPolicy import ModelPolicy

class ModelPlayerGUI(BotPlayerGUI):
    def __init__(self, id = None):
        super().__init__(id)
        self.policy = ModelPolicy()