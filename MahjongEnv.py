import MahjongTiles
import random
import BotPlayer, Player

class MahjongEnv:
    def __init__(self, real_player = False):
        self.deck = []
        self._generate_tiles()
        self._reset()
        self.wind = 0
        self.round = 0
        self.players = []
        self.real_player = real_player
        self.end_game = False
        self.current_player = 0
        self.discard_pool = []
        self.min_faan = 3
        self.max_faan = 10

    def _generate_tiles(self):
        # Create tiles
        for key, value in MahjongTiles.tile_classes.items():
            for _ in range(4):
                self.deck.append(MahjongTiles.MahjongTiles(key))
        
        # Shuffle the tiles
        random.shuffle(self.deck)
        print(f"Deck with {len(self.deck)} tiles shuffled.")

    def _reset(self):
        self.wind = 0
        self.round = 0
        self.current_player = 0

    def view_deck(self):
        for tile in self.deck:
            tile.print_tile()

    def add_players(self):
        if not self.real_player:
            self.players = [BotPlayer.BotPlayer() for _ in range(4)]
        else:
            self.players = [BotPlayer.BotPlayer() for _ in range(3)]
            self.players.append(Player.Player())
            random.shuffle(self.players)
        print(f'Total initialized players: {len(self.players)}')

    def game_state_check(self):
        if len(self.deck) == 0:
            self.end_game = True
            return

    def start_game(self):
        if len(self.players) != 4:
            raise ValueError
        
        for i in range(4):
            drawn_tiles = self.deck[:13]
            self.deck = self.deck[13:]
            self.players[i].draw_tiles(drawn_tiles)

        for i in range(4):
            print(f"Player {i+1}: ", end='')
            self.players[i].display_hand()
            print()
        print(f"{len(self.deck)} tiles in deck.")

        while not self.end_game:
            
            print("="*40)
            self.players[self.current_player].draw_tiles([self.deck.pop()])
            current_player_discard = self.players[self.current_player].discard()
            self.discard_pool.append(current_player_discard)
            print(f"Player {self.current_player} discards {current_player_discard.tile_class_info[1]} ")

            self.game_state_check()
            self.current_player += 1
            self.current_player %= 4