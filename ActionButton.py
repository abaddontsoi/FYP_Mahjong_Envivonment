import pygame

class ActionButton(pygame.sprite.Sprite):
    def __init__(self, action, rect):
        super().__init__()
        self.action = action
        self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.image.fill((200, 200, 200))
        font = pygame.font.SysFont(None, 20)
        text_surf = font.render(str(action), True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(rect.width//2, rect.height//2))
        self.image.blit(text_surf, text_rect)
        self.rect = rect