import pygame
import os
from ModelPolicy import ModelPolicy
from PlayerGUI import PlayerGUI
from BotPlayerGUI import BotPlayerGUI
from ModelPlayerGUI import ModelPlayerGUI
import MahjongGUIEnv
import time
import json 

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)

# Dimension constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

class MahjongGUI:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mahjong Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_env = MahjongGUIEnv.MahjongGUIEnv(real_player=True)
        self.sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.has_human = False

    def run(self):
        # Search for config.json
        config_path = "config.json"

        players = []
        heuristic_bot_count = 0
        model_bot_count = 0
        human_count = 0
        game_log_location = None
        
        # Ensure file existance
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            heuristic_bot_count = config.get("heuristic_bot_count", 0)
            model_bot_count = config.get("model_bot_count", 0)
            human_count = config.get("human_count", 0)
            game_log_location = config.get("game_log_location", "raw_logs")
            
            # Ensure total player count is 4
            if heuristic_bot_count + model_bot_count + human_count != 4:
                raise ValueError("Total player count must be 4. Please check your config.json.")
        else:
            raise FileNotFoundError("config.json not found. Please create a config.json file with the following format: {\"heuristic_bot_count\": 3, \"model_bot_count\": 1, \"human_count\": 0}")


        heuristic_bots = [BotPlayerGUI(f'HeuristicBot{i+1}') for i in range(heuristic_bot_count)]

        model_bots = [ModelPlayerGUI(f'ModelBot{i+1}') for i in range(model_bot_count)]
        for bot in model_bots:
            bot.assign_policy(ModelPolicy())

        players = heuristic_bots + model_bots
        if human_count > 0:
            for i in range(human_count):
                players.append(PlayerGUI(f'HumanPlayer{i+1}'))
                self.has_human = True
        
        self.game_env.add_players(players) 
        # Assign game environment to players
        for player in self.game_env.players:
            player.assign_env(self.game_env)
        
        # Start the game
        self.game_env.start_game()


        # A Mahjong game that last for 4 winds
        while not self.game_env.end_game and self.running:

            # Start a new round
            while not self.game_env.end_round and self.running:

                # Event listening loop ends when game ends in each round
                while not self.game_env.end_game and self.running :
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                        else:
                            self.game_env.receive_input(event)
                    
                    self.game_env.update_game_state()
                    self.render()
                    self.clock.tick(120)
        log = self.game_env.log

        os.makedirs(game_log_location, exist_ok=True)

        tstamp = int(time.time())
        with open(os.path.join(game_log_location, f'game_log_{tstamp}.json') , 'w') as f:
            json.dump(log, f, indent=4)
        if self.game_env.winning_log:
            with open(os.path.join(game_log_location, f'winning_log_{tstamp}.json') , 'w') as f:
                json.dump(self.game_env.winning_log, f, indent=4)

        pygame.quit()

    def render(self):
        self.screen.fill(GREEN)  # Green background for the board

        # Remove all sprites if exists
        if self.ui_sprites:
            self.ui_sprites.empty()
        if self.sprites:
            self.sprites.empty()

        # Draw tiles and other game elements here
        self.game_env.refresh_screen_items()
        screen_items = self.game_env.get_screen_items()

        # Players scores display
        player_scores = screen_items['player_scores']
        for score_surface, score_rect in player_scores:
            self.screen.blit(score_surface, score_rect)

        # Discard pool display
        discard_pool = screen_items['discard_pool']
        for tile in discard_pool:
            self.sprites.add(tile)

        # Player hand display
        players = screen_items['players']
        if self.has_human:
            for idx, player in enumerate(players):
                if player.__class__ == PlayerGUI:
                    for tile in player.hand:
                        self.sprites.add(tile)
        else:
            for player in players:
                for tile in player.hand:
                    self.sprites.add(tile)

        # Player called tuples display
        players_called_tuples = screen_items['players_called_tuples']
        for idx, called_tuples in enumerate(players_called_tuples):
            for tuple in called_tuples:
                for tile in tuple:
                    self.sprites.add(tile)
        
        # Player action buttons display
        action_buttons = screen_items['player_action_buttons']
        for button in action_buttons:
            self.ui_sprites.add(button)
            
        # Player on-draw action buttons display
        on_draw_action_buttons = screen_items['player_on_draw_action_buttons']
        for button in on_draw_action_buttons:
            self.ui_sprites.add(button)
        
        # Player chow option buttons display
        chow_option_buttons = screen_items['player_chow_option_buttons']
        for button in chow_option_buttons:
            self.ui_sprites.add(button)

        self.sprites.draw(self.screen)
        self.ui_sprites.draw(self.screen)
        # print(f"Current game state: {self.game_env.game_state}")
        pygame.display.flip()


if __name__ == "__main__":
    game = MahjongGUI()
    game.run()