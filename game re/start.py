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
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('tp', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                tile = Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


tile_width = tile_height = 50
flag = 0
FPS = 50
width, height = 500, 500
WIDTH = HEIGHT = 500

class Teleport_blocks(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tp, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

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

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, x, y):
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if flag == 1:
                self.rect = self.rect.move(x - 5, y)
            if flag == 2:
                self.rect = self.rect.move(x + 5, y)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if flag == 3:
                self.rect = self.rect.move(x, y + 5)
            if flag == 4:
                self.rect = self.rect.move(x, y - 5)






def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
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
    clock = pygame.time.Clock()
    pygame.init()
    tp = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    simple = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    screen = pygame.display.set_mode((width, height))
    start_screen()
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'tp': load_image('tp.jpg')
    }
    player_image = load_image('robot_1.png')
    player, level_x, level_y = generate_level(load_level('rate.txt'))
    while True:
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
        if pygame.key.get_pressed()[1073741903]: #вправо
            player.rect.x += 3
            flag = 1
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741904]: #влево
            flag = 2
            player.rect.x -= 3
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741906]: #вверх
            player.rect.y -= 3
            flag = 3
            player.update(kor_x, kor_y)
        elif pygame.key.get_pressed()[1073741905]: #вниз
            player.rect.y += 3
            flag = 4
            player.update(kor_x, kor_y)
        pygame.display.flip()
        screen.fill((255, 255, 255))
        simple.draw(screen)
        player_group.draw(screen)
        tp.draw(screen)
        Border(0, 200, width, 200)
        Border(0, 300, width, height)
        Border(0, 200, 0, height)
        Border(width, 200, width, height)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        clock.tick(FPS)
pygame.quit()