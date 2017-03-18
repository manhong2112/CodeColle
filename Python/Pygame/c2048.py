import random
from copy import deepcopy as copy

import pygame


def calc_color(i):
    return 255 - (i ** 2 % 255)


class Game(object):
    vector = {pygame.K_w: (0, 1),
              pygame.K_s: (0, -1),
              pygame.K_a: (1, 0),
              pygame.K_d: (-1, 0)}

    def __init__(self):
        self.block = ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0])
        self.recently_block = copy(self.block)
        self.block[random.randint(0, 3)][random.randint(0, 3)] = random.choice((2, 2, 4))
        pass

    def next(self):
        loc_list = []
        for x in range(4):
            for y in range(4):
                if not self.block[x][y]:
                    loc_list.append((x, y))

        if loc_list:
            if self.recently_block == self.block:
                return True
        else:
            return self.movable()

        loc = random.choice(loc_list)
        self.block[loc[0]][loc[1]] = random.choice((2, 2, 4))
        return True
        pass

    def end(self):
        self.print()
        print("# END #")
        print("# Your Score is: {0} #".format(self.score()))
        input("Enter to continue...")
        exit()
        pass

    def move(self, direction, is_check=False):
        cache = copy(self.block)
        dx, dy = self.vector[direction]
        i = ()
        while i != cache:
            i = copy(cache)
            for x in range(3, -1, -1):
                for y in range(3, -1, -1):
                    _x, _y = x - dx, y - dy
                    if not (0 <= _x < 4 and 0 <= _y < 4):
                        continue
                    if cache[y][x] and (not cache[_y][_x] or cache[y][x] == cache[_y][_x]):
                        cache[_y][_x] += cache[y][x]
                        cache[y][x] = 0
        if is_check:
            return cache != self.block

        self.recently_block = copy(self.block)
        self.block = cache
        pass

    def movable(self):
        for i in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
            if self.move(i, True):
                return True
        return False
        pass

    def print(self, display=None, _font=None):
        if display is None or _font is None:
            for x in range(4):
                for y in range(4):
                    print(self.block[x][y], end=' ')
                print()
        else:
            for x in range(4):
                for y in range(4):
                    v = self.block[x][y]
                    pygame.draw.rect(
                            display,
                            (calc_color(v ** 2), calc_color(v ** 3), calc_color(v ** 5)),  # color
                            (120 * y, 120 * x, 120, 120))  # x, y ,width, height
                    display.blit(
                            _font.render(
                                    str(v) if v != 0 else "",
                                    1,
                                    (30, 30, 30)
                            ),
                            (120 * y + 54, 120 * x + 54))
        pass

    def score(self):
        def _f(val, score=0):
            for i in val:
                score += _f(i) if type(i) == list else i
            return score

        return _f(self.block)


pygame.init()
screen = pygame.display.set_mode((480, 480), 0, 32)
pygame.display.set_caption("2048")

font = pygame.font.SysFont("arial", 20)

game = Game()
game.print(screen, font)

k = ""
finish = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_r:
                game.print(screen, font)
                game = Game()
                finish = False

            if finish:
                game.print(screen, font)
                screen.blit(font.render(
                                "You lose, total score is {}".format(game.score()),
                                1,
                                (30, 30, 30)
                            ), (120, 240))
                screen.blit(font.render(
                                "press ESC to leave",
                                1,
                                (30, 30, 30)
                            ), (128, 260))
                screen.blit(font.render(
                                "press R to restart",
                                1,
                                (30, 30, 30)
                            ), (128, 280))

                pygame.display.update()
                continue

            k = event.key
            try:
                game.move(k)
                finish = not game.next()
            except KeyError:
                continue
            finally:
                game.print(screen, font)
                k = ""

    pygame.display.update()
