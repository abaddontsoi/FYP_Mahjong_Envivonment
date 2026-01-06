import Player

class BotPlayer(Player.Player):
    def __init__(self):
        super().__init__()

    def discard(self):
        return self.hand.pop()