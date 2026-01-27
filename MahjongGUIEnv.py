import random
import MahjongTiles
from PlayerGUI import PlayerGUI
from BotPlayerGUI import BotPlayerGUI
import pygame
from ActionButton import ActionButton


game_states = [
    'initializing_round', 
    'player_drawing_from_deck', 
    'checking_on_draw_action',
    'player_take_on_draw_action',
    'waiting_discard', 
    'pooling_for_action', 
    'player_take_action',
    'player_choose_chow_tiles',
    'ending_round', 
    'ending_wind', 
    'ending_game'
]

class MahjongGUIEnv:
    def __init__(self, real_player = True):
        # Main game loop
        self.game_loop = None

        self.deck = []
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
        self.event_buffer = None
        self.game_state = None

        # Display and call related
        self.screen_items = {
            'players': [],
            'players_called_tuples': [],
            'discard_pool': [],
            'player_action_buttons': [],
            'player_on_draw_action_buttons': [],
            'player_chow_option_buttons': []
        }
        self.call_actions = []
        self.current_player_on_draw_actions = []
        self.current_player_chow_options = []
        self.current_chow_action_player = None

        # Logging related
        self.log = []

    def assign_game_loop(self, game_loop):
        self.game_loop = game_loop

    def generate_tiles(self):
        # Clear deck
        self.deck = []
        # Create tiles
        for key, value in MahjongTiles.tile_classes.items():
            for _ in range(4):
                self.deck.append(MahjongTiles.MahjongTiles(key))
        # for i in range(1, 35):
        #     self.deck.append(MahjongTiles.MahjongTiles(i))

        # Shuffle the tiles
        random.shuffle(self.deck)
        print(f"Deck with {len(self.deck)} tiles shuffled.")

    def add_players(self, players: list[PlayerGUI]):
        self.players = players
        random.shuffle(self.players)
        print(f'Total initialized players: {len(self.players)}')

    def round_reset(self):
        # Clear players' hand
        for player in self.players:
            player.clear_hand()

        self.end_round = False
        self.generate_tiles()
        self.discard_pool = []
        self.discard_buffer = None
        
        # Shift players play order
        self.players.append(self.players[0])
        self.players.pop()


    def receive_input(self, input_data: pygame.event.Event):
        self.event_buffer = input_data

    # State based update method
    def update_game_state(self):
        if self.game_state == None:
            self.game_state = 'initializing_round'
            print("Initializing {} wind {} round.".format(['East', 'South', 'West', 'North'][self.wind], self.round + 1))
        
        if self.game_state == 'initializing_round':
            self.round_reset()

            # Draw initial 13 tiles for each player
            for idx, player in enumerate(self.players):
                initial_tiles = [self.deck.pop() for _ in range(13)]
                # initial_tiles = [
                #     MahjongTiles.MahjongTiles(i) for i in range(1,14)
                # ]
                player.draw_tiles(initial_tiles)
                player.set_position(idx)

            self.game_state = 'player_drawing_from_deck'
            print("Player draw from deck.")

        if self.game_state == 'player_drawing_from_deck':
            # Check if deck is empty
            # If yes, this round has ended
            if not self.deck:
                print("No more tiles in deck, round ends in a draw.")
                self.end_round = True
                self.game_state = 'ending_round'
            else:
                current_player = self.players[self.current_player]
                drawn_tile = self.deck.pop()
                current_player.draw_tiles([drawn_tile])
                print(f"Player {current_player.id} drew a tile.")
                self.game_state = 'checking_on_draw_action'

        if self.game_state == 'checking_on_draw_action':
            # Check for self-drawn winning/additional kong/hidden kong action
            on_draw_actions = self.players[self.current_player].check_on_draw_action()
            if on_draw_actions and self.players[self.current_player].__class__ is PlayerGUI:
                self.current_player_on_draw_actions = on_draw_actions
                print(f"Player {self.players[self.current_player].id} on draw actions: {self.current_player_on_draw_actions}")
                self.game_state = 'player_take_on_draw_action'
            else:
                self.game_state = 'waiting_discard'
        
        if self.game_state == 'player_take_on_draw_action':
            # Create action buttons for the player
            action_player = self.current_player
            if self.players[action_player].__class__ is BotPlayerGUI:
                chosen_action = None                
                # Handle action
                if chosen_action == 'self_drawn':
                    self.end_round = True
                    print(f"Player {self.players[action_player].id} wins!")
                    self.game_state = 'ending_round'
                elif chosen_action == 'additional_kong':
                    self.players[action_player].additional_kong()
                    # Draw 1 tile
                    self.players[action_player].draw_tiles([self.deck.pop(0)])
                    self.game_state = 'checking_on_draw_action'
                elif chosen_action == 'hidden_kong':
                    self.players[action_player].hidden_kong()
                    # Draw 1 tile
                    self.players[action_player].draw_tiles([self.deck.pop(0)])
                    self.game_state = 'checking_on_draw_action'
                else:
                    self.game_state = 'waiting_discard'
            elif self.event_buffer is not None and self.event_buffer.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = self.event_buffer.pos
                current_player = self.players[action_player]

                hand_y = 1000 - ((self.current_player) % 4) * (self.players[(self.current_player) % 4].hand[0].rect.height + 20)
                button_start_x = 1000  # Start after ~5 tiles (50+5*55=325)
                button_y = hand_y  # Just below tiles
                button_width, button_height = 100, 50
                for btn_idx, action in enumerate(self.current_player_on_draw_actions):
                    btn_x = button_start_x + btn_idx * 120
                    btn_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
                    if btn_rect.collidepoint(mouse_pos):
                        chosen_action = action
                        print(f"Player {current_player.id} chose action: {chosen_action}")

                        # Handle action
                        if chosen_action == 'self_drawn':
                            self.end_round = True
                            winning_faan = self.players[action_player].win()
                            print(f"Player {current_player.id} wins (self drawn): {winning_faan}")
                            self.game_state = 'ending_round'
                            self.current_player_on_draw_actions = []
                            self.log.append({
                                'player_id': current_player.id,
                                'action': 'self_drawn',
                                'player_hand': [str(tile) for tile in current_player.hand],
                                'called_tuples': [[str(tile) for tile in tup] for tup in current_player.called_tuples],
                                'discard_pool': [str(tile) for tile in self.discard_pool]
                            })
                            break
                        elif chosen_action == 'additional_kong':
                            current_player.additional_kong()
                            # Handles robbing kong

                            # Draw 1 tile
                            current_player.draw_tiles([self.deck.pop(0)])
                            self.current_player_on_draw_actions = []
                            self.game_state = 'waiting_discard'
                            self.log.append({
                                'player_id': current_player.id,
                                'action': 'additional_kong',
                                'player_hand': [str(tile) for tile in current_player.hand],
                                'called_tuples': [[str(tile) for tile in tup] for tup in current_player.called_tuples],
                                'discard_pool': [str(tile) for tile in self.discard_pool]
                            })
                        elif chosen_action == 'hidden_kong':
                            current_player.hidden_kong()
                            # Draw 1 tile
                            current_player.draw_tiles([self.deck.pop(0)])
                            self.current_player_on_draw_actions = []
                            self.game_state = 'waiting_discard'
                            self.log.append({
                                'player_id': current_player.id,
                                'action': 'hidden_kong',
                                'player_hand': [str(tile) for tile in current_player.hand],
                                'called_tuples': [[str(tile) for tile in tup] for tup in current_player.called_tuples],
                                'discard_pool': [str(tile) for tile in self.discard_pool]
                            })
                        elif chosen_action == 'pass':
                            self.current_player_on_draw_actions = []
                            self.game_state = 'waiting_discard'
                        
                        self.event_buffer = None
                        break
            
                # self.current_player_on_draw_actions = []
        
        if self.game_state == 'waiting_discard':
            # Wait for player to discard a tile
            # Check clicking event from event buffer
            # See if it is on any tile of current player's hand
            action_player = self.current_player
            if type(self.players[action_player]) == BotPlayerGUI:
                self.discard_buffer = self.players[action_player].discard()
                print(f"Player {self.players[action_player].id} discarded a tile.")
                self.game_state = 'pooling_for_action'
                self.log.append({
                    'player_id': self.players[action_player].id,
                    'action': 'discard',
                    'player_hand': [str(tile) for tile in self.players[action_player].hand],
                    'called_tuples': [[str(tile) for tile in tup] for tup in self.players[action_player].called_tuples],
                    'discard_pool': [str(tile) for tile in self.discard_pool],
                    'discarded_tile': str(self.discard_buffer)
                })
            elif self.event_buffer is not None and self.event_buffer.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = self.event_buffer.pos
                current_player = self.players[action_player]
                for tile in current_player.hand:
                    if tile.rect.collidepoint(mouse_pos):
                        self.discard_buffer = tile
                        print(f"Player {current_player.id} discarded a tile.")
                        self.event_buffer = None
                        self.game_state = 'pooling_for_action'
                        self.log.append({
                            'player_id': current_player.id,
                            'action': 'discard',
                            'player_hand': [str(tile) for tile in current_player.hand],
                            'called_tuples': [[str(tile) for tile in tup] for tup in current_player.called_tuples],
                            'discard_pool': [str(tile) for tile in self.discard_pool],
                            'discarded_tile': str(self.discard_buffer)
                        })
                        break
                # Filter out the discarded tile
                current_player.hand = [tile for tile in current_player.hand if tile != self.discard_buffer]
                current_player.align_tile_sprites()
                current_player.faan_calculator.self_drawn_flag = False
                current_player.faan_calculator.consecutive_kong_count = 0
                current_player.faan_calculator.robbing_additional_kong_flag = False
                current_player.faan_calculator.self_drawn_on_last_tile_flag = False

        if self.game_state == 'pooling_for_action':
            if self.discard_buffer:
                # Pool each player for call actions
                has_call = False
                for i in range(1, 4):
                    player_actions = self.players[(self.current_player + i) % 4].check_possible_calls(self.discard_buffer, i==1)
                    if player_actions:
                        has_call = True
                        player_actions.append('pass')
                    self.call_actions.append(player_actions)
                self.game_state = 'player_take_action'

                # If not call, move discard buffer to discard pool
                if not has_call:
                    print(f"Tile {self.discard_buffer} added to discard pool.")
                    self.discard_pool.append(self.discard_buffer)
                    self.discard_buffer = None
                    self.call_actions = []

                    # Allow next player to draw (original order)
                    self.current_player += 1
                    self.current_player %= 4
                    self.game_state = 'player_drawing_from_deck'
            else:
                # No discard buffer, move to next player
                self.current_player += 1
                self.current_player %= 4
                self.game_state = 'player_drawing_from_deck'

        if self.game_state == 'player_take_action':
            # Check the event buffer for player's action
            action_player = None
            call_queue = {
                'win': [],
                'kong': [],
                'pong': [],
                'chow': []
            }
            for i in range(1, 4):
                if self.event_buffer is not None and self.discard_buffer and self.event_buffer.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = self.event_buffer.pos
                    if self.screen_items['player_action_buttons']:
                        possible_actions = self.screen_items['player_action_buttons'][i-1]
                        for btn_idx, action in enumerate(possible_actions):
                            if action.rect.collidepoint(mouse_pos):
                                action_player = (self.current_player + i) % 4
                                chosen_action = action.action
                                print(f"Player {self.players[action_player].id} chose action: {chosen_action}")

                                # Handle action
                                if chosen_action == 'win':
                                    self.end_round = True
                                    print(f"Player {self.players[action_player].id} wins from {self.players[self.current_player].id}!")
                                    winning_faan = self.players[action_player].win(self.discard_buffer)
                                    print(f"Winning hand faan: {winning_faan}")
                                    self.game_state = 'ending_round'
                                    self.log.append({
                                        'player_id': self.players[action_player].id,
                                        'action': 'win',
                                        'player_hand': [str(tile) for tile in self.players[action_player].hand],
                                        'called_tuples': [[str(tile) for tile in tup] for tup in self.players[action_player].called_tuples],
                                        'discard_pool': [str(tile) for tile in self.discard_pool],
                                        'winning_tile': str(self.discard_buffer)
                                    })
                                    break
                                elif chosen_action == 'kong':
                                    self.players[action_player].kong(self.discard_buffer)
                                    self.discard_buffer = None
                                    # Draw 1 tile
                                    self.players[action_player].draw_tiles([self.deck.pop(0)])
                                    self.log.append({
                                        'player_id': self.players[action_player].id,
                                        'action': 'kong',
                                        'player_hand': [str(tile) for tile in self.players[action_player].hand],
                                        'called_tuples': [[str(tile) for tile in tup] for tup in self.players[action_player].called_tuples],
                                        'discard_pool': [str(tile) for tile in self.discard_pool],
                                        'winning_tile': str(self.discard_buffer)
                                    })
                                elif chosen_action == 'pong':
                                    self.players[action_player].pong(self.discard_buffer)
                                    self.discard_buffer = None
                                    self.log.append({
                                        'player_id': self.players[action_player].id,
                                        'action': 'pong',
                                        'player_hand': [str(tile) for tile in self.players[action_player].hand],
                                        'called_tuples': [[str(tile) for tile in tup] for tup in self.players[action_player].called_tuples],
                                        'discard_pool': [str(tile) for tile in self.discard_pool],
                                        'winning_tile': str(self.discard_buffer)
                                    })
                                elif chosen_action == 'chow':
                                    self.current_player_chow_options = self.players[action_player].get_chow_options(self.discard_buffer)
                                    if len(self.current_player_chow_options) > 1:
                                        # Multiple chow options, let player choose
                                        print(f"Player {self.players[action_player].id} chow options: {[ [str(tile) for tile in option] for option in self.current_player_chow_options ]}")
                                        self.current_chow_action_player = action_player
                                        self.game_state = 'player_choose_chow_tiles'
                                        break
                                    elif len(self.current_player_chow_options) == 1: 
                                        self.players[action_player].chow(self.discard_buffer, self.current_player_chow_options[0])
                                        self.current_player_chow_options = []
                                        self.discard_buffer = None
                                    self.log.append({
                                        'player_id': self.players[action_player].id,
                                        'action': 'chow',
                                        'player_hand': [str(tile) for tile in self.players[action_player].hand],
                                        'called_tuples': [[str(tile) for tile in tup] for tup in self.players[action_player].called_tuples],
                                        'discard_pool': [str(tile) for tile in self.discard_pool],
                                        'winning_tile': str(self.discard_buffer)
                                    })
                                elif chosen_action == 'pass':
                                    # If all players pass, add to discard pool
                                    if i == 3:
                                        print(f"Tile {self.discard_buffer} added to discard pool.")
                                        self.discard_pool.append(self.discard_buffer)
                                        self.discard_buffer = None

                                        # Allow next player to draw (original order)
                                        self.current_player = action_player + 1
                                        self.current_player %= 4
                                        self.game_state = 'player_drawing_from_deck'
                                        self.call_actions = []


                                # Discard
                                if chosen_action != 'pass':
                                    self.game_state = 'waiting_discard'
                                    self.current_chow_action_player = None
                                    self.current_player = action_player
                                else:
                                    # Original order
                                    self.current_player += 1
                                    self.current_player %= 4
                                    self.game_state = 'player_drawing_from_deck'
                                    self.current_chow_action_player = None

                                self.discard_buffer = None
                                self.call_actions = []
                                
                                self.event_buffer = None
                                break

                if action_player is not None:
                    break

        if self.game_state == 'player_choose_chow_tiles':
            action_player = self.current_chow_action_player
            if type(self.players[action_player]) == BotPlayerGUI:
                chosen_option = self.current_player_chow_options[0]
                self.players[action_player].chow(self.discard_buffer, chosen_option)
                self.discard_buffer = None
                self.current_player_chow_options = []
                self.game_state = 'waiting_discard'
                self.current_chow_action_player = None
            elif self.event_buffer is not None and self.event_buffer.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = self.event_buffer.pos
                current_player = self.players[action_player]

                # Detect which chow option button is clicked
                for idx, chow_btn in enumerate(self.screen_items['player_chow_option_buttons']):
                    if chow_btn.rect.collidepoint(mouse_pos):
                        chosen_option = self.current_player_chow_options[idx]
                        print(f"Player {current_player.id} chose chow option: {[str(tile) for tile in chosen_option]}")

                        self.players[action_player].chow(self.discard_buffer, chosen_option)
                        self.game_state = 'waiting_discard'
                        self.call_actions = []
                        self.current_player_chow_options = []
                        self.current_chow_action_player = None
                        self.current_player = action_player
                        self.event_buffer = None
                        self.discard_buffer = None
                        break

        if self.game_state == 'ending_round':
            print("Round ended.")
            self.end_round = True
            if self.round >= 3:
                self.game_state = 'ending_wind'
                self.wind = (self.wind + 1) % 4
            else:
                self.round += 1
                self.wind = (self.wind + 1) % 4
                self.game_state = None

        if self.game_state == 'ending_wind':
            print("Wind ended.")
            self.end_round = True
            self.wind += 1
            self.wind %= 4
            self.round = 0
            if self.wind == 0:
                self.game_state = 'ending_game'
            else:
                self.game_state = None

        if self.game_state == 'ending_game': 
            print("Game ended.")
            self.end_game = True
            # Conclude players performance

        if not self.event_buffer:
            return
        
    def start_game(self):
        if len(self.players) != 4:
            raise ValueError
        
        self.round = 0
        self.wind = 0
        self.current_player = 0
        self.game_state = None
        print("Game started.")

    def refresh_screen_items(self):
        self.screen_items = {
            'players': [],
            'players_called_tuples': [],
            'discard_pool': [],
            'player_action_buttons': [],
            'player_on_draw_action_buttons': [],
            'player_chow_option_buttons': []
        }

        for idx, player in enumerate(self.players):
            player.align_tile_sprites()
            for tile in player.hand:
                tile.rect.topleft = (tile.rect.topleft[0], 1000 - idx * (tile.rect.height + 20))
            self.screen_items['players'].append(player)            

            player.align_called_tuple_sprites()
            for tuple in player.called_tuples:
                for tile in tuple:
                    tile.rect.topleft = (tile.rect.topleft[0], 1000 - idx * (tile.rect.height + 20))
            self.screen_items['players_called_tuples'].append(player.called_tuples)

        # Collect tiles from discard pool
        # Update location for each tile in discard pool, each row should have at most 20 tiles
        for idx, tile in enumerate(self.discard_pool[-80:]):
            tile.rect.topleft = (50 + (idx % 20) * (tile.rect.width + 5), 50 + (idx //20) * (tile.rect.height + 5))
        
        # Limit displayed discard pool to last 80 tiles
        self.screen_items['discard_pool'].extend(self.discard_pool[-80:])
        if self.discard_buffer:
            self.discard_buffer.rect.topleft = (50 + (len(self.discard_pool) % 20) * (self.discard_buffer.rect.width + 5), 50 + (len(self.discard_pool) //20) * (self.discard_buffer.rect.height + 5))
            self.screen_items['discard_pool'].append(self.discard_buffer)
        
        # Create action buttons for each player based on call_actions
        for idx, actions in enumerate(self.call_actions):
            # Position: Right of hand, below tiles
            hand_y = 1000 - ((self.current_player + idx + 1) % 4) * (self.players[(self.current_player + idx + 1) % 4].hand[0].rect.height + 20)
            button_start_x = 1000  # Start after ~5 tiles (50+5*55=325)
            button_y = hand_y  # Just below tiles
            button_width, button_height = 70, 35
            
            player_buttons = []
            for btn_idx, action in enumerate(actions):
                btn_x = button_start_x + btn_idx * 80
                btn_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
                button = ActionButton(action, btn_rect)
                player_buttons.append(button)
                
            self.screen_items['player_action_buttons'].append(player_buttons)
        
        
        # Create action buttons for current player's on draw actions
        if self.current_player_on_draw_actions:
            hand_y = 1000 - ((self.current_player) % 4) * (self.players[(self.current_player) % 4].hand[0].rect.height + 20)
            button_start_x = 1000  # Start after ~5 tiles (50+5*55=325)
            button_y = hand_y  # Just below tiles
            button_width, button_height = 100, 50
            
            on_draw_buttons = []
            for btn_idx, action in enumerate(self.current_player_on_draw_actions):
                btn_x = button_start_x + btn_idx * 120
                btn_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
                button = ActionButton(action, btn_rect)
                on_draw_buttons.append(button)
                
            self.screen_items['player_on_draw_action_buttons'].extend(on_draw_buttons)
        
        if self.current_player_chow_options:
            hand_y = 1000 - ((self.current_chow_action_player) % 4) * (self.players[(self.current_chow_action_player) % 4].hand[0].rect.height + 20)
            button_start_x = 1000
            button_y = hand_y  - 100 # Above tiles
            button_width, button_height = 200, 50

            chow_option_buttons = []
            for btn_idx, option in enumerate(self.current_player_chow_options):
                btn_x = button_start_x + btn_idx * (200 + 50)
                btn_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
                button = ActionButton(f'', btn_rect, img_paths=[tile.tile_image_path for tile in option])
                chow_option_buttons.append(button)
                
            self.screen_items['player_chow_option_buttons'].extend(chow_option_buttons)

    def get_screen_items(self):
        return self.screen_items