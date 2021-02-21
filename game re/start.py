import sys
import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    exit, room, boss, first_key, second_key, new_player, x, y = None, None, None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('tp', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '/':
                Tile('локация', x, y)
            elif level[y][x] == '1':
                first_key = Key_1(x, y)
            elif level[y][x] == '2':
                second_key = Key_2(x, y)
            elif level[y][x] == 'b':
                boss = Boss(x, y)
            elif level[y][x] == 'r':
                room = Rooms(x, y)
            elif level[y][x] == 'e':
                exit = Exit(x, y)
    return exit, room, boss, first_key, second_key, new_player, x, y


key_1 = 0
key_2 = 0
tile_width = tile_height = 50
flag = 0
FPS = 50
width, height = 400, 400
WIDTH = HEIGHT = 500
secret = 0


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Key_1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(keys, all_sprites)
        self.image = first_key_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global key_1
        if pygame.sprite.spritecollideany(self, player_group):
            key_1 = 1
            self.kill()


class Key_2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(keys, all_sprites)
        self.image = first_key_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global key_2
        if pygame.sprite.spritecollideany(self, player_group):
            key_2 = 1
            self.kill()


class Rooms(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(rooms, all_sprites)
        self.image = rooms_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        pass


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exits, all_sprites)
        self.image = exit_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(simple, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        pass


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boss_game, all_sprites)
        self.image = boss_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, x, y):
        if secret == 1:
            if pygame.sprite.spritecollideany(self, exits):
                self.rect = self.rect.move(x + 35 * 50, y + 5 * 50)
            if pygame.sprite.spritecollideany(self, rooms):
                if key_1 == 1 and key_2 == 1:
                    self.rect = self.rect.move(x, y + 150)
                else:
                    self.rect = self.rect.move(x, y - 7)
            if pygame.sprite.spritecollideany(self, boss_game):
                self.rect = self.rect.move(x - 53 * 50, y + 18 * 50)
            elif pygame.sprite.spritecollideany(self, vertical_borders):
                if flag == 1:
                    self.rect = self.rect.move(x - 7, y)
                if flag == 2:
                    self.rect = self.rect.move(x + 7, y)
            elif pygame.sprite.spritecollideany(self, horizontal_borders):
                if flag == 3:
                    self.rect = self.rect.move(x, y + 7)
                if flag == 4:
                    self.rect = self.rect.move(x, y - 7)
        else:
            if pygame.sprite.spritecollideany(self, exits):
                self.rect = self.rect.move(x + 15 * 50, y + 17 * 50)
            if pygame.sprite.spritecollideany(self, rooms):
                if key_1 == 1 and key_2 == 1:
                    self.rect = self.rect.move(x, y + 150)
                else:
                    self.rect = self.rect.move(x, y - 7)
            if pygame.sprite.spritecollideany(self, boss_game):
                self.rect = self.rect.move(x - 53 * 50, y + 18 * 50)
            elif pygame.sprite.spritecollideany(self, vertical_borders) \
                    or pygame.sprite.spritecollideany(self, horizontal_borders):
                if flag == 1:
                    self.rect = self.rect.move(x - 7, y)
                if flag == 2:
                    self.rect = self.rect.move(x + 7, y)
                if flag == 3:
                    self.rect = self.rect.move(x, y + 7)
                if flag == 4:
                    self.rect = self.rect.move(x, y - 7)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["", "",
                  "                                 Жизнь",
                  "                                 Просто",
                  "                                 Фальшивка"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    Border(18 * 50, 12 * 50, 18 * 50, 14 * 50)
    Border(40 * 50, 4 * 50, 59 * 50, 4 * 50)
    Border(40 * 50, 4 * 50, 40 * 50, 6 * 50)
    Border(40 * 50, 6 * 50, 57 * 50, 6 * 50)
    Border(59 * 50, 4 * 50, 59 * 50, 20 * 50)
    Border(59 * 50, 20 * 50, 63 * 50, 20 * 50)
    Border(57 * 50, 6 * 50, 57 * 50, 20 * 50)
    Border(59 * 50, 20 * 50, 63 * 50, 20 * 50)
    Border(53 * 50, 20 * 50, 57 * 50, 20 * 50)
    Border(53 * 50, 20 * 50, 53 * 50, 22 * 50)
    Border(40 * 50, 22 * 50, 53 * 50, 22 * 50)
    Border(4 * 50, 53 * 50, 8 * 50, 53 * 50)
    Border(4 * 50, 53 * 50, 4 * 50, 57 * 50)
    Border(4 * 50, 57 * 50, 8 * 50, 57 * 50)
    Border(8 * 50, 56 * 50, 8 * 50, 57 * 50)
    Border(8 * 50, 56 * 50, 9 * 50, 56 * 50)
    Border(9 * 50, 56 * 50, 9 * 50, 62 * 50)
    Border(9 * 50, 62 * 50, 18 * 50, 62 * 50)
    Border(18 * 50, 61 * 50, 18 * 50, 62 * 50)
    Border(18 * 50, 61 * 50, 45 * 50, 61 * 50)
    Border(45 * 50, 58 * 50, 45 * 50, 61 * 50)
    Border(45 * 50, 58 * 50, 46 * 50, 58 * 50)
    Border(46 * 50, 57 * 50, 46 * 50, 58 * 50)
    Border(46 * 50, 57 * 50, 56 * 50, 57 * 50)
    Border(56 * 50, 55 * 50, 56 * 50, 57 * 50)
    Border(56 * 50, 55 * 50, 60 * 50, 55 * 50)
    Border(60 * 50, 53 * 50, 60 * 50, 55 * 50)
    Border(60 * 50, 53 * 50, 61 * 50, 53 * 50)
    Border(61 * 50, 48 * 50, 61 * 50, 53 * 50)
    Border(58 * 50, 48 * 50, 61 * 50, 48 * 50)
    Border(58 * 50, 47 * 50, 58 * 50, 48 * 50)
    Border(56 * 50, 47 * 50, 58 * 50, 47 * 50)
    Border(56 * 50, 46 * 50, 56 * 50, 47 * 50)
    Border(34 * 50, 46 * 50, 56 * 50, 46 * 50)
    Border(34 * 50, 46 * 50, 34 * 50, 47 * 50)
    Border(33 * 50, 47 * 50, 34 * 50, 47 * 50)
    Border(33 * 50, 47 * 50, 33 * 50, 48 * 50)
    Border(32 * 50, 48 * 50, 33 * 50, 48 * 50)
    Border(32 * 50, 48 * 50, 32 * 50, 49 * 50)
    Border(25 * 50, 49 * 50, 32 * 50, 49 * 50)
    Border(25 * 50, 47 * 50, 25 * 50, 49 * 50)
    Border(17 * 50, 47 * 50, 25 * 50, 47 * 50)
    Border(17 * 50, 47 * 50, 17 * 50, 49 * 50)
    Border(9 * 50, 49 * 50, 17 * 50, 49 * 50)
    Border(9 * 50, 49 * 50, 9 * 50, 54 * 50)
    Border(8 * 50, 54 * 50, 9 * 50, 54 * 50)
    Border(8 * 50, 53 * 50, 8 * 50, 54 * 50)
    Border(11 * 50, 51 * 50, 16 * 50, 51 * 50)
    Border(16 * 50, 51 * 50, 16 * 50, 54 * 50)
    Border(11 * 50, 54 * 50, 16 * 50, 54 * 50)
    Border(11 * 50, 51 * 50, 11 * 50, 54 * 50)
    Border(11 * 50, 56 * 50, 17 * 50, 56 * 50)
    Border(17 * 50, 56 * 50, 17 * 50, 60 * 50)
    Border(11 * 50, 60 * 50, 17 * 50, 60 * 50)
    Border(11 * 50, 56 * 50, 11 * 50, 60 * 50)
    Border(18 * 50, 48 * 50, 24 * 50, 48 * 50)
    Border(24 * 50, 48 * 50, 24 * 50, 51 * 50)
    Border(18 * 50, 51 * 50, 24 * 50, 51 * 50)
    Border(18 * 50, 48 * 50, 18 * 50, 51 * 50)
    Border(18 * 50, 59 * 50, 28 * 50, 59 * 50)
    Border(18 * 50, 59 * 50, 18 * 50, 60 * 50)
    Border(18 * 50, 60 * 50, 44 * 50, 60 * 50)
    Border(28 * 50, 57 * 50, 28 * 50, 59 * 50)
    Border(28 * 50, 57 * 50, 32 * 50, 57 * 50)
    Border(32 * 50, 53 * 50, 32 * 50, 57 * 50)
    Border(32 * 50, 53 * 50, 36 * 50, 53 * 50)
    Border(36 * 50, 52 * 50, 36 * 50, 53 * 50)
    Border(36 * 50, 52 * 50, 38 * 50, 52 * 50)
    Border(38 * 50, 51 * 50, 38 * 50, 52 * 50)
    Border(38 * 50, 51 * 50, 43 * 50, 51 * 50)
    Border(43 * 50, 51 * 50, 43 * 50, 52 * 50)
    Border(41 * 50, 52 * 50, 43 * 50, 52 * 50)
    Border(41 * 50, 52 * 50, 41 * 50, 53 * 50)
    Border(38 * 50, 53 * 50, 41 * 50, 53 * 50)
    Border(38 * 50, 53 * 50, 38 * 50, 56 * 50)
    Border(38 * 50, 56 * 50, 41 * 50, 56 * 50)
    Border(41 * 50, 56 * 50, 41 * 50, 58 * 50)
    Border(41 * 50, 58 * 50, 44 * 50, 58 * 50)
    Border(44 * 50, 58 * 50, 44 * 50, 60 * 50)
    Border(18 * 50, 53 * 50, 25 * 50, 53 * 50)
    Border(25 * 50, 50 * 50, 25 * 50, 53 * 50)
    Border(25 * 50, 50 * 50, 33 * 50, 50 * 50)
    Border(33 * 50, 49 * 50, 33 * 50, 50 * 50)
    Border(33 * 50, 49 * 50, 34 * 50, 49 * 50)
    Border(34 * 50, 48 * 50, 34 * 50, 49 * 50)
    Border(34 * 50, 48 * 50, 35 * 50, 48 * 50)
    Border(35 * 50, 47 * 50, 35 * 50, 48 * 50)
    Border(35 * 50, 47 * 50, 38 * 50, 47 * 50)
    Border(38 * 50, 47 * 50, 38 * 50, 50 * 50)
    Border(37 * 50, 50 * 50, 38 * 50, 50 * 50)
    Border(37 * 50, 50 * 50, 37 * 50, 51 * 50)
    Border(31 * 50, 51 * 50, 37 * 50, 51 * 50)
    Border(31 * 50, 51 * 50, 31 * 50, 56 * 50)
    Border(27 * 50, 56 * 50, 31 * 50, 56 * 50)
    Border(27 * 50, 56 * 50, 27 * 50, 58 * 50)
    Border(18 * 50, 58 * 50, 27 * 50, 58 * 50)
    Border(18 * 50, 53 * 50, 18 * 50, 58 * 50)
    Border(51 * 50, 50 * 50, 56 * 50, 50 * 50)
    Border(56 * 50, 49 * 50, 56 * 50, 50 * 50)
    Border(56 * 50, 49 * 50, 60 * 50, 49 * 50)
    Border(60 * 50, 49 * 50, 60 * 50, 52 * 50)
    Border(59 * 50, 52 * 50, 60 * 50, 52 * 50)
    Border(59 * 50, 52 * 50, 59 * 50, 54 * 50)
    Border(55 * 50, 54 * 50, 59 * 50, 54 * 50)
    Border(55 * 50, 54 * 50, 55 * 50, 56 * 50)
    Border(51 * 50, 56 * 50, 55 * 50, 56 * 50)
    Border(51 * 50, 50 * 50, 51 * 50, 56 * 50)
    Border(41 * 50, 47 * 50, 55 * 50, 47 * 50)
    Border(55 * 50, 47 * 50, 55 * 50, 49 * 50)
    Border(50 * 50, 49 * 50, 55 * 50, 49 * 50)
    Border(50 * 50, 49 * 50, 50 * 50, 50 * 50)
    Border(18 * 50, 12 * 50, 28 * 50, 12 * 50)
    Border(41 * 50, 47 * 50, 41 * 50, 50 * 50)
    Border(41 * 50, 50 * 50, 50 * 50, 50 * 50)
    Border(41 * 50, 47 * 50, 55 * 50, 47 * 50)
    Border(44 * 50, 52 * 50, 50 * 50, 52 * 50)
    Border(50 * 50, 52 * 50, 50 * 50, 56 * 50)
    Border(46 * 50, 56 * 50, 50 * 50, 56 * 50)
    Border(46 * 50, 55 * 50, 46 * 50, 56 * 50)
    Border(39 * 50, 55 * 50, 46 * 50, 55 * 50)
    Border(39 * 50, 54 * 50, 39 * 50, 55 * 50)
    Border(39 * 50, 54 * 50, 42 * 50, 54 * 50)
    Border(42 * 50, 53 * 50, 42 * 50, 54 * 50)
    Border(42 * 50, 53 * 50, 44 * 50, 53 * 50)
    Border(44 * 50, 52 * 50, 44 * 50, 53 * 50)
    Border(67 * 50, 61 * 50, 74 * 50, 61 * 50)
    Border(74 * 50, 61 * 50, 74 * 50, 66 * 50)
    Border(67 * 50, 61 * 50, 67 * 50, 66 * 50)
    Border(67 * 50, 66 * 50, 74 * 50, 66 * 50)
    Border(28 * 50, 12 * 50, 28 * 50, 14 * 50)
    Border(26 * 50, 14 * 50, 28 * 50, 14 * 50)
    Border(18 * 50, 14 * 50, 24 * 50, 14 * 50)
    Border(24 * 50, 14 * 50, 24 * 50, 19 * 50)
    Border(26 * 50, 14 * 50, 26 * 50, 16 * 50)
    Border(26 * 50, 16 * 50, 39 * 50, 16 * 50)
    Border(39 * 50, 16 * 50, 39 * 50, 20 * 50)
    Border(39 * 50, 20 * 50, 40 * 50, 20 * 50)
    Border(40 * 50, 20 * 50, 40 * 50, 22 * 50)
    Border(16 * 50, 19 * 50, 24 * 50, 19 * 50)
    Border(16 * 50, 18 * 50, 16 * 50, 19 * 50)
    Border(11 * 50, 18 * 50, 16 * 50, 18 * 50)
    Border(11 * 50, 18 * 50, 11 * 50, 20 * 50)
    Border(6 * 50, 20 * 50, 11 * 50, 20 * 50)
    Border(6 * 50, 20 * 50, 6 * 50, 21 * 50)
    Border(6 * 50, 21 * 50, 11 * 50, 21 * 50)
    Border(11 * 50, 21 * 50, 11 * 50, 22 * 50)
    Border(11 * 50, 22 * 50, 16 * 50, 22 * 50)
    Border(16 * 50, 21 * 50, 16 * 50, 22 * 50)
    Border(16 * 50, 21 * 50, 26 * 50, 21 * 50)
    Border(26 * 50, 18 * 50, 26 * 50, 21 * 50)
    Border(26 * 50, 18 * 50, 36 * 50, 18 * 50)
    Border(36 * 50, 18 * 50, 36 * 50, 20 * 50)
    Border(35 * 50, 20 * 50, 36 * 50, 20 * 50)
    Border(35 * 50, 20 * 50, 35 * 50, 29 * 50)
    Border(27 * 50, 29 * 50, 35 * 50, 29 * 50)
    Border(27 * 50, 29 * 50, 27 * 50, 31 * 50)
    Border(27 * 50, 31 * 50, 40 * 50, 31 * 50)
    Border(40 * 50, 24 * 50, 40 * 50, 31 * 50)
    Border(40 * 50, 24 * 50, 53 * 50, 24 * 50)
    Border(11 * 50, 22 * 50, 16 * 50, 22 * 50)
    Border(53 * 50, 24 * 50, 53 * 50, 26 * 50)
    Border(53 * 50, 26 * 50, 57 * 50, 26 * 50)
    Border(57 * 50, 26 * 50, 57 * 50, 35 * 50)
    Border(53 * 50, 35 * 50, 57 * 50, 35 * 50)
    Border(53 * 50, 35 * 50, 53 * 50, 41 * 50)
    Border(53 * 50, 41 * 50, 62 * 50, 41 * 50)
    Border(62 * 50, 35 * 50, 62 * 50, 41 * 50)
    Border(58 * 50, 35 * 50, 62 * 50, 35 * 50)
    Border(58 * 50, 26 * 50, 58 * 50, 35 * 50)
    Border(58 * 50, 26 * 50, 62 * 50, 26 * 50)
    Border(62 * 50, 24 * 50, 62 * 50, 26 * 50)
    Border(62 * 50, 24 * 50, 77 * 50, 24 * 50)
    Border(77 * 50, 24 * 50, 77 * 50, 31 * 50)
    Border(77 * 50, 31 * 50, 89 * 50, 31 * 50)
    Border(82 * 50, 20 * 50, 82 * 50, 29 * 50)
    Border(81 * 50, 20 * 50, 82 * 50, 29 * 50)
    Border(81 * 50, 18 * 50, 81 * 50, 20 * 50)
    Border(78 * 50, 16 * 50, 89 * 50, 16 * 50)
    Border(89 * 50, 16 * 50, 89 * 50, 31 * 50)
    Border(78 * 50, 16 * 50, 78 * 50, 20 * 50)
    Border(77 * 50, 20 * 50, 78 * 50, 20 * 50)
    Border(77 * 50, 20 * 50, 77 * 50, 22 * 50)
    Border(63 * 50, 22 * 50, 77 * 50, 22 * 50)
    Border(63 * 50, 20 * 50, 63 * 50, 22 * 50)
    if secret == 1:
        Border(82 * 50, 29 * 50, 89 * 50, 29 * 50)
        Border(81 * 50, 18 * 50, 89 * 50, 18 * 50)
    else:
        Border(82 * 50, 29 * 50, 87 * 50, 29 * 50)
        Border(87 * 50, 18 * 50, 87 * 50, 29 * 50)
        Border(81 * 50, 18 * 50, 87 * 50, 18 * 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    kor_x = 0
    kor_y = 0
    pygame.display.set_caption('OP')
    clock = pygame.time.Clock()
    pygame.init()
    keys = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    simple = pygame.sprite.Group()
    boss_game = pygame.sprite.Group()
    rooms = pygame.sprite.Group()
    exits = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    screen = pygame.display.set_mode((width, height))
    start_screen()
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'tp': load_image('tp.jpg'),
    }
    first_key_image = load_image('red_key.png')
    player_image = load_image('robot_1.png')
    boss_image = load_image('1.png')
    rooms_image = load_image('fon_lok.png')
    exit_image = load_image('1.png')
    if secret == 1:
        exit, room, boss, first_key, second_key, player, level_x, level_y = generate_level(load_level('rate.txt'))
    else:
        exit, room, boss, first_key, second_key, player, level_x, level_y = generate_level(load_level('rate1.txt'))
    camera = Camera()
    while True:
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.K_RIGHT:
                kor = event.pos()
                kor_x = kor[0]
                kor_y = kor[1]
            elif event.type == pygame.K_LEFT:
                kor = event.pos()
                kor_x = kor[0]
                kor_y = kor[1]
            elif event.type == pygame.K_UP:
                kor = event.pos()
                kor_x = kor[0]
                kor_y = kor[1]
            elif event.type == pygame.K_DOWN:
                kor = event.pos()
                kor_x = kor[0]
                kor_y = kor[1]
        if pygame.key.get_pressed()[1073741903]:  # вправо
            player.rect.x += 6
            flag = 1
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741904]:  # влево
            flag = 2
            player.rect.x -= 6
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741906]:  # вверх
            player.rect.y -= 6
            flag = 3
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741905]:  # вниз
            player.rect.y += 6
            flag = 4
            player.update(kor_x, kor_y)
        first_key.update()
        second_key.update()
        pygame.display.flip()
        screen.fill((163, 73, 164))
        simple.draw(screen)
        keys.draw(screen)
        boss_game.draw(screen)
        player_group.draw(screen)
        rooms.draw(screen)
        exits.draw(screen)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        clock.tick(FPS)
pygame.quit()
