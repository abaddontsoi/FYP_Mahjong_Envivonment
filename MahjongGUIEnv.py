import random
import pygame
import MahjongTiles
from PlayerGUI import PlayerGUI
from BotPlayerGUI import BotPlayerGUI

class MahjongGUIEnv:

    def __init__(self, real_player = True):
        self.deck = []
        self._reset()
        self.wind = -1
        self.round = -1
        self.players = []
        self.real_player = real_player
        self.end_round = False
        self.end_game = False
        self.current_player = 0
        self.discard_pool = []
        self.min_faan = 3
        self.max_faan = 10
        self.discard_buffer = None

    def _reset(self):
        self.wind = 0
        self.round = 0
        self.current_player = 0

    def _generate_tiles(self):
        # Clear deck
        self.deck = []
        # Create tiles
        for key, value in MahjongTiles.tile_classes.items():
            for _ in range(4):
                self.deck.append(MahjongTiles.MahjongTiles(key))
        
        # Shuffle the tiles
        random.shuffle(self.deck)
        print(f"Deck with {len(self.deck)} tiles shuffled.")

    def _view_deck(self):
        for tile in self.deck:
            tile.print_tile()

    def get_pool_and_buffer(self):
        discard_pool = self.discard_pool
        
        if self.discard_buffer:
            return discard_pool + [self.discard_buffer]
        
        return discard_pool

    def request_player_discard(self, current_player):
        self.discard_buffer = self.players[current_player].discard()

    def game_state_check(self):
        # Check if this round is last round of the game
        if self.wind == 3 and self.round == 3:
            self.end_game = True
            return
    
        # Update round and wind info
        self.round += 1
        self.round %= 4
        if self.round == 0:
            self.wind += 1
            self.wind %= 4

    def pool_for_call(self):
        temp_current_player = self.current_player
        # Pool all players to see if they can call or not
        call_queues = {
            'win': [],
            'kong': [],
            'pong': [],
            'chow': []
        }
        for i in range(3):
            temp_current_player += 1
            temp_current_player %= 4
            call_response = self.players[temp_current_player].call_response(self.discard_buffer, i==0)
            if call_response and call_response != 'pass':
                call_queues[call_response].append(temp_current_player)

        action_taken = False        
        # Check if any player is to win
        if call_queues['win']:
            self.end_round = True
            for i in call_queues['win']:
                action_taken = True
                print(f"Player {self.players[i].id} wins!")
            return

        # Check if any player is to kong
        elif call_queues['kong']:
            # Player id
            action_player = call_queues['kong'][0]
            # Move the tile to player's hand
            self.players[action_player].kong(self.discard_buffer)
            self.discard_buffer = None
            # Draw 1 tile
            self.players[action_player].draw_tiles([self.deck.pop(0)])
            action_taken = True

        # Check if any player is to pong
        elif call_queues['pong']:
            action_player = call_queues['pong'][0]
            # Move the tile to player's hand
            self.players[action_player].pong(self.discard_buffer)
            self.discard_buffer = None
            action_taken = True

        # Check if any player is to chow
        elif call_queues['chow']:
            action_player = call_queues['chow'][0]
            # Move the tile to player's hand
            self.players[action_player].chow(self.discard_buffer)
            self.discard_buffer = None
            action_taken = True

        if action_taken:
            # Discard
            self.request_player_discard(action_player)
            self.current_player = action_player
            self.discard_buffer = None
            self.pool_for_call()
        else:
            if self.discard_buffer:
                self.discard_pool.append(self.discard_buffer)
                self.discard_buffer = None

    def round_state_check(self):
        self.pool_for_call()

        if len(self.deck) == 0:
            self.end_round = True
            return
        
        self.current_player += 1
        self.current_player %= 4

    def add_players(self, players: list[PlayerGUI]):
        self.players = players
        random.shuffle(self.players)

    def round_reset(self):
        # Clear players' hand
        for player in self.players:
            player.clear_hand()

        self.end_round = False
        self._generate_tiles()
        self.discard_pool = []
        self.discard_buffer = None
        
        # Shift players play order
        self.players.append(self.players[0])
        self.players.pop()
        self.game_state_check()
    
    def handle_event(self, player: PlayerGUI):
        response = None
        while response is None:
            if pygame.event.get() == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                response = True
        return response

    def init_game(self):
        if len(self.players) != 4:
            raise ValueError
        
        while not self.end_game:
            # Reset each round
            print("="*40)
            self.round_reset()
            winds = ['East', 'South', 'West', 'North']
            print(f"{winds[self.wind]} Wind {self.round + 1} Round")

            for player in self.players:
                drawn_tiles = self.deck[:13]
                self.deck = self.deck[13:]
                player.hand = drawn_tiles
                player.sort_hand()
    
    def get_screen_items(self):
        player_tiles = []
        for player in self.players:
            player.align_hand_sprites()
            player_tiles.append(player.hand)

        # Process discard pool tiles' positions

        return {
            'player_tiles': player_tiles,
            'discard_pool': self.discard_pool,
        }