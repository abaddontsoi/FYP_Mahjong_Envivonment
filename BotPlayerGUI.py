from PlayerGUI import PlayerGUI
import MahjongTiles
import random
from Policy import Policy

class BotPlayerGUI(PlayerGUI):
    def __init__(self, id = None):
        super().__init__(id)
        self.policy = Policy()

    def view_other_players_call_tuples(self):
        if self.game_env is None or self.round_position == -1:
            return []
        other_player_call_tuples = []
        for i in range(3):
            current_player = self.game_env.players[(self.round_position + 1 + i) % 4]
            other_player_call_tuples.append(current_player.called_tuples)
        return other_player_call_tuples

    def update_board_state(self):
        if any([
            self.game_env is None,
            self.round_position == -1,
            self.hand == [],
        ]):
            return
        
        # Getting 3 other players' call tuples
        other_player_call_tuples = self.view_other_players_call_tuples()

        self.policy.update_board_state(self.game_env.discard_pool, self.hand, other_player_call_tuples)

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