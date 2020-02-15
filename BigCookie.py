import pygame


class BigCookie(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.original_image = pygame.transform.scale(image, (200, 200))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 40

    def detect_click(self, mouse_pos):
        if (self.rect.x < mouse_pos[0] < self.rect.x + 340
                and self.rect.y < mouse_pos[1] < self.rect.y + 340):
            return True

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def transform_image(self, w):
        self.image = pygame.transform.scale(self.original_image, (w, w))
