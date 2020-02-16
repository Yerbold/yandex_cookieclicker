import pygame
from CookieScanner import CookieScanner


class BigCookie(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.original_image = pygame.transform.scale(image, (200, 200))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 40
        self.radius = self.rect.size[0] // 2
        self.center = (550, 140)
        cookie_scan = CookieScanner()
        self.cookies_amount = 0
        self.cookies_per_click = 4

    def add_cookies(self, amount=-1):
        if amount == -1:
            self.cookies_amount += self.cookies_per_click
        else:
            self.cookies_amount += amount

    def detect_click(self, mouse_pos):
        distance = (mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2
        distance **= 0.5
        if self.radius >= distance:
            return True

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def transform_image(self, w):
        self.image = pygame.transform.scale(self.original_image, (w, w))
