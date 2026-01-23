import pygame

class ActionButton(pygame.sprite.Sprite):
    def __init__(self, action, rect, img_paths: list[str] = None):
        super().__init__()
        self.action = action
        self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.image.fill((200, 200, 200))
        font = pygame.font.SysFont(None, 20)
        text_surf = font.render(str(action), True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(rect.width//2, rect.height//2))
        self.image.blit(text_surf, text_rect)
        self.rect = rect

        # Use images if provided
        if img_paths:
            try:
                # All images should be displayed
                images = [pygame.image.load(path) for path in img_paths]
                # Add all images side by side
                total_width = sum(img.get_width() for img in images)
                max_height = max(img.get_height() for img in images)
                combined_image = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
                current_x = 0
                for img in images:
                    combined_image.blit(img, (current_x, 0))
                    current_x += img.get_width()
                # Resize to fit button
                self.image = pygame.transform.scale(combined_image, (rect.width, rect.height))
            except Exception as e:
                print(f"Error loading image for action {action}: {e}")