from PlayerGUI import PlayerGUI
import MahjongTiles
import random

class BotPlayerGUI(PlayerGUI):
    def __init__(self, id = None):
        super().__init__(id)

    def discard(self):
        return self.hand.pop(random.randint(0, len(self.hand) - 1))

    def decide_call_action(self, call_tile: MahjongTiles.MahjongTiles, possible_actions: list):
        if not possible_actions:
            return None
        if 'win' in possible_actions:
            print(f"Bot Player {self.id} decides to win on tile {call_tile.classId}")
            return 'win'
        action = random.choice(possible_actions)
        print(f"Bot Player {self.id} decides to {action} on tile {call_tile.classId}")
        return action