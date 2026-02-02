import pygame
import random
from PlayerGUI import PlayerGUI
from BotPlayerGUI import BotPlayerGUI
import MahjongGUIEnv
import datetime

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
        self.game_env.assign_game_loop(self)
        self.sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()

    def run(self):
        # Add players
        self.game_env.add_players([
            # PlayerGUI('Alice'),
            # PlayerGUI('Bob'),
            # PlayerGUI('Charlie'),
            # PlayerGUI('Diana'),
            BotPlayerGUI('Bot1'),
            BotPlayerGUI('Bot2'),
            BotPlayerGUI('Bot3'),
            PlayerGUI('You')
        ]) 
        random.shuffle(self.game_env.players)
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
        with open(f'game_log_{datetime.datetime.now()}.json', 'w') as f:
            import json
            json.dump(log, f, indent=4)

        pygame.quit()

    # Event handler
    def handle_events(self):
        ...

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

        # Discard pool display
        discard_pool = screen_items['discard_pool']
        for tile in discard_pool:
            self.sprites.add(tile)

        # Player hand display
        players = screen_items['players']
        for idx, player in enumerate(players):
            # if player.__class__ == PlayerGUI and player.__class__ != BotPlayerGUI:
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