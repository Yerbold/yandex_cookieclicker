import pygame
import os
from CookieScanner import CookieScanner


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
screen = pygame.display.set_mode((1100, 750), pygame.FULLSCREEN, pygame.RESIZABLE)
buildings = pygame.Surface((600, 400))
cookie_scan = CookieScanner()
cookie_scan.set_new_record()
font = pygame.font.SysFont('Calibri', 24, False, False)
font_building = pygame.font.SysFont('Calibri', 36, False, False)
count = cookie_scan.get_cookies_amount()
buildings_button = font_building.render('Buildings', False, (0, 0, 0))
cookie_amount = font.render('Amount: ' + str(count), False, (0, 0, 0))
quit_text = font.render('Quit', False, (255, 0, 0))
running = True
fps = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
big_cookie = BigCookie()

while running:
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            break
        if big_cookie.detect_click(mouse_pos) and any(pygame.mouse.get_pressed()):
            big_cookie.transform_image(220)
            big_cookie.change_pos(440, 30)
            count += 1
            cookie_amount = font.render('Amount: ' + str(count), False, (0, 0, 0))
        else:
            big_cookie.transform_image(200)
            big_cookie.change_pos(450, 40)
        if 1050 < mouse_pos[0] and mouse_pos[1] < 20 and any(pygame.mouse.get_pressed()):
            running = False


    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (1045, 0, 50, 25), 2)
    screen.blit(cookie_amount, (0, 0))
    screen.blit(quit_text, (1050, 0))
    screen.blit(buildings_button, (0, 700))
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
