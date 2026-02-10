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

        self.policy.update_board_state(self.game_env.discard_pool, self.hand, self.called_tuples, other_player_call_tuples)

    def discard(self):
        print(f"Bot Player {self.id} has {len(self.hand)} tiles")
        self.update_board_state()
        idx = self.policy.decide_discard()
        print(f"Bot Player {self.id} discards tile {self.hand[idx].classId}")
        return self.hand.pop(idx)

    def decide_call_action(self, call_tile: MahjongTiles.MahjongTiles, possible_actions: list):
        if not possible_actions:
            return None
        
        self.update_board_state()
        if 'win' in possible_actions:
            print(f"Bot Player {self.id} decides to win on tile {call_tile.classId}")
            return 'win'
        
        if 'chow' in possible_actions:
            should_chow, chow_option = self.policy.decide_chow(call_tile)
            if not should_chow:
                possible_actions.remove('chow')
        
        if 'pong' in possible_actions:
            should_pong = self.policy.decide_pong(call_tile)
            if not should_pong:
                possible_actions.remove('pong')
        
        if 'kong' in possible_actions:
            should_kong = self.policy.decide_kong(call_tile)
            if not should_kong:
                possible_actions.remove('kong')

        action = possible_actions[0]
        print(f"Bot Player {self.id} decides to {action} on tile {call_tile.classId}")
        return action