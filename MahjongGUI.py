import pygame
from BotPlayerGUI import BotPlayerGUI
from PlayerGUI import PlayerGUI
from MahjongGUIEnv import MahjongGUIEnv

# Constants - add these at the top after imports
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

class MahjongGame:
    def __init__(self, real_player = True):
        self.state = "MENU"  # State machine
        self.sprites = pygame.sprite.Group()  # All game objects
        self.ui_sprites = pygame.sprite.LayeredUpdates()  # UI layer
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Game variables
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

        # pygame UI setup
        pygame.font.init()
        # Font for buttons
        font = pygame.font.Font(None, 48)

        # Button rects (vertically aligned in center)
        center_x, center_y = self.screen.get_rect().center
        btn_width, btn_height = 200, 60
        spacing = 10

        play_text = font.render("Play", True, BLACK)
        self.play_btn = pygame.Surface((btn_width, btn_height))
        self.play_btn.fill(WHITE)
        play_rect = play_text.get_rect(center=(btn_width//2, btn_height//2))
        self.play_btn.blit(play_text, play_rect)
        self.play_btn_rect = self.play_btn.get_rect(center=(center_x, center_y - 80))  # Top button

        logs_text = font.render("Logs", True, BLACK)
        self.logs_btn = pygame.Surface((btn_width, btn_height))
        self.logs_btn.fill(WHITE)
        logs_rect = logs_text.get_rect(center=(btn_width//2, btn_height//2))
        self.logs_btn.blit(logs_text, logs_rect)
        self.logs_btn_rect = self.logs_btn.get_rect(center=(center_x, center_y))     # Middle

        quit_text = font.render("Quit", True, BLACK)
        self.quit_btn = pygame.Surface((btn_width, btn_height))
        self.quit_btn.fill(WHITE)
        quit_rect = quit_text.get_rect(center=(btn_width//2, btn_height//2))
        self.quit_btn.blit(quit_text, quit_rect)
        self.quit_btn_rect = self.quit_btn.get_rect(center=(center_x, center_y + 80)) # Bottom

        self.game_env = MahjongGUIEnv(real_player=real_player)


    def run(self):
        pygame.init()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = True
                
                if self.state == "MENU":
                    # Play button
                    if self.play_btn_rect.collidepoint(mouse_pos):
                        self.state = "PLAY"
                        print("Starting game...")
                        players = [BotPlayerGUI(i) for i in range(3)] + [PlayerGUI(3)]
                        for p in players:
                            p.assign_env(self.game_env)
                        self.game_env.add_players(players)
                        self.game_env.init_game()
                    # Logs button  
                    elif self.logs_btn_rect.collidepoint(mouse_pos):
                        self.state = "LOGS"
                    # Quit button
                    elif self.quit_btn_rect.collidepoint(mouse_pos):
                        return False
        
        return True

    def menu_update(self, mouse_pos, mouse_clicked):
        if mouse_clicked:
            if self.play_btn_rect.collidepoint(mouse_pos):  # Use _rect
                self.state = "PLAY"
            elif self.logs_btn_rect.collidepoint(mouse_pos):
                self.state = "LOGS"
            elif self.quit_btn_rect.collidepoint(mouse_pos):
                self.running = False
    
    def play_update(self):
        screen_item = self.game_env.get_screen_items()
        # Update sprites based on game state    
        players_items = screen_item['player_tiles']
        discard_pool = screen_item['discard_pool']

        self.sprites.empty()  # Clear existing sprites
        
        for i, hand in enumerate(players_items):
            for j, tile in enumerate(hand):
                tile.rect.bottomright = (tile.rect.bottomright[0], 950 - i * 100)
                self.sprites.add(tile)
                
        self.sprites.update()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if self.state == "MENU":
            self.menu_update(mouse_pos, mouse_clicked)

        elif self.state == "PLAY":
            screen_item = self.game_env.get_screen_items()
            # Update sprites based on game state    
            players_items = screen_item['player_tiles']
            discard_pool = screen_item['discard_pool']

            self.sprites.empty()  # Clear existing sprites
            
            for i, hand in enumerate(players_items):
                for j, tile in enumerate(hand):
                    tile.rect.bottomright = (tile.rect.bottomright[0], 950 - i * 100)
                    self.sprites.add(tile)
            
            
            
            self.sprites.update()

    def render(self):
        self.screen.fill(GREEN)  # Green background
        
        if self.state == "MENU":
            # Title at top
            title_font = pygame.font.Font(None, 72)
            title_surf = title_font.render("Mahjong GUI", True, WHITE)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
            # In render(), calculate once
            screen_rect = self.screen.get_rect()
            title_rect = title_surf.get_rect(center=screen_rect.center)
            title_rect.top = 100  # Adjust vertical position
            self.screen.blit(title_surf, title_rect)
            
            # Draw the 3 buttons
            self.screen.blit(self.play_btn, self.play_btn_rect)
            self.screen.blit(self.logs_btn, self.logs_btn_rect)
            self.screen.blit(self.quit_btn, self.quit_btn_rect)
            
            # Hover borders
            mouse_pos = pygame.mouse.get_pos()
            if self.play_btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLUE, self.play_btn_rect, 4)
            if self.logs_btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLUE, self.logs_btn_rect, 4)
            if self.quit_btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLUE, self.quit_btn_rect, 4)
        
        elif self.state == "PLAY":
            self.sprites.draw(self.screen)
            self.ui_sprites.draw(self.screen)
        
        pygame.display.flip()



if __name__ == "__main__":
    game = MahjongGame(real_player=True)
    game.run()