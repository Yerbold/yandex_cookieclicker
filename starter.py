import pygame
import os
import schedule
from BigCookie import BigCookie
from CookieScanner import CookieScanner
from Buildings import BuildingGroup, Cursors, Grandmas, Factories, Farms, Mines
from Buildings import productions, buildings


# ---

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


def human_readable(num):  # a function for a much easier measurement of numbers
    str_num = ''
    decimals = num - int(num)
    num -= decimals
    num = int(num)
    while num // 1000 > 0:
        str_num = ',' + str(num % 1000).rjust(3, '0') + str_num
        num //= 1000
    if decimals == 0:
        return str(num) + str_num
    else:
        return str(num) + str_num + str(round(decimals, 2))[1:]


double_click_power_cost = 100
# ---

class Background(pygame.sprite.Sprite):
    def __init__(self, group, image):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.transform.scale(image, (1100, 750))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


pygame.init()

font = pygame.font.SysFont('Calibri', 24, True, False)
medium_font = pygame.font.SysFont('Calibri', 30, False, False)
bigger_font = pygame.font.SysFont('Calibri', 36, True, False)

screen = pygame.display.set_mode((1100, 750), pygame.FULLSCREEN, pygame.RESIZABLE)
buildings_surface = pygame.Surface((200, 500))

all_sprites = pygame.sprite.Group()
background = Background(all_sprites, load_image('Background.jpg'))
big_cookie = BigCookie(all_sprites, load_image('BigCookie.png', -1))
cookie_scan = CookieScanner()
click_power_text = font.render('Double Click Power', False, (0, 0, 0))
cookie_amount = font.render('Amount: ' + str(big_cookie.cookies_amount), False, (0, 0, 0))
quit_text = font.render('Quit', False, (255, 0, 0))
store_text = bigger_font.render('Store', False, (0, 0, 0))
running = True
fps = 60
clock = pygame.time.Clock()
cursors = Cursors(big_cookie)
grandmas = Grandmas()
farms = Farms()
mines = Mines()
factories = Factories()
building_group = BuildingGroup(big_cookie)
building_group.append(cursors, grandmas, farms, mines, factories)
get_pressed = pygame.mouse.get_pressed
schedule.every(0.1).seconds.do(building_group.automatic_cookie_production)


while running:  # game loop
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            break
        if big_cookie.detect_click(mouse_pos) and any(get_pressed()):  # condition for pressing big cookie
            big_cookie.transform_image(220)
            big_cookie.change_pos(440, 30)
            big_cookie.add_cookies()
        else:
            big_cookie.transform_image(200)
            big_cookie.change_pos(450, 40)
        if 1050 < mouse_pos[0] and mouse_pos[1] < 20 and any(get_pressed()):  # condition for pressing quit button
            amount = big_cookie.cookies_amount
            cookies_per_click = big_cookie.cookies_per_click
            cookies_per_second = building_group.total_production
            cookie_scan.set_new_record(amount, cookies_per_click, int(cookies_per_second))
            running = False
            break
        if 900 < mouse_pos[0] and 140 <= mouse_pos[1] <= 200 and any(get_pressed()):  # condition for pressing double click power button
            if big_cookie.cookies_amount >= double_click_power_cost:
                big_cookie.add_cookies(-double_click_power_cost)
                big_cookie.cookies_per_click *= 2
                productions['cursor'] = big_cookie.cookies_per_click / 10
                cursors.produce = productions['cursor']
                double_click_power_cost *= 5
        if 900 < mouse_pos[0] and 210 < mouse_pos[1] < 760 and any(get_pressed()):  # condition for pressing buildings
            for i in range(5):
                if 210 + i * 100 <= mouse_pos[1] <= 310 + i * 100:
                    building_group.buy_specific_building(i)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    building_group.update_total_production()
    buildings_surface.fill((192, 192, 192))
    pygame.draw.rect(screen, (0, 0, 0), (1050, 0, 50, 25), 2)
    pygame.draw.rect(screen, (255, 215, 0), (900, 140, 200, 60))
    pygame.draw.rect(screen, (0, 0, 0), (900, 140, 200, 60), 3)
    cookies_amount = human_readable(int(big_cookie.cookies_amount))
    cookie_amount_text = font.render('Amount: ' + cookies_amount, False, (0, 0, 0))
    cursor_production = productions['cursor'] * cursors.n
    cookies_per_second = human_readable(building_group.total_production + cursor_production)
    cookies_ps_text = font.render('Cookies Per Second: ' + cookies_per_second, False, (0, 0, 0))
    click_power_cost_text = font.render(human_readable(double_click_power_cost), False, (0, 0, 0))
    screen.blit(click_power_text, (903, 150))
    screen.blit(click_power_cost_text, (903, 175))
    screen.blit(cookie_amount_text, (0, 0))
    screen.blit(cookies_ps_text, (0, 30))
    screen.blit(quit_text, (1055, 0))
    screen.blit(store_text, (900, 100))

    for i in range(5):  # drawing a table and content of buildings
        pygame.draw.rect(buildings_surface, (191, 96, 0), (0, i * 100, 200, 100), 10)
        building_amount = str(building_group.get_building_amount(i))
        info = buildings[i] + ' x' + building_amount
        production = '+' + human_readable(productions[buildings[i]])
        production_text = font.render(production, False, (0, 0, 0))
        building_name = medium_font.render(info, False, (0, 0, 0))
        cost = building_group.get_building_cost(i)
        building_cost = font.render('Cost: ' + human_readable(cost), False, (0, 0, 0))
        buildings_surface.blit(building_name, (10, 5 + i * 100))
        buildings_surface.blit(production_text, (10, 40 + i * 100))
        buildings_surface.blit(building_cost, (10, 70 + i * 100))

    screen.blit(buildings_surface, (900, 210))
    schedule.run_pending()
    clock.tick(fps)
    pygame.display.flip()

