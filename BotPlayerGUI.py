from PlayerGUI import PlayerGUI
import MahjongTiles
import random

class BotPlayerGUI(PlayerGUI):
    def __init__(self, id = None):
        super().__init__(id)

    def convert_hand_to_feature_vector(self):
        m = [0]*9
        s = [0]*9
        p = [0]*9
        z = [0]*7
        for tile in self.hand:
            if tile.tile_suit == 'm':
                m[tile.tile_number - 1] += 1
            elif tile.tile_suit == 's':
                s[tile.tile_number - 1] += 1
            elif tile.tile_suit == 'p':
                p[tile.tile_number - 1] += 1
            elif tile.tile_suit == 'z':
                z[tile.tile_number - 1] += 1
            
        # Count for pairs

        # Count for triplets missing 1
        return (m, s, p, z)

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