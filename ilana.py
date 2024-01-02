import sys
import pygame
import os
import random

WIDTH = 564 * 2
HEIGHT = 282 * 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ilana")


class Banana:

    def __init__(self, x):
        self.width = 60
        self.x = x
        self.y = 420
        self.height = 50
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

        if self.x <= - WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('assets/images/banana.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Ilana:

    def __init__(self):
        self.width = 120
        self.height = 200
        self.x = 40
        self.y = 280
        self.dy = 7
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jumpstop = 100
        self.falling = False
        self.fallstop = self.y
        self.texture_num = 1
        self.set_texture()
        self.show()

    def update(self, loops):

        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jumpstop:
                self.fall()
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fallstop:
                self.stop()


        if loops % 5 == 0:
            self.texture_num = (self.texture_num + 1) % 8
            self.set_texture()

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f'assets/images/ilana_{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def jump(self):
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True

class Background:

    def __init__(self, x, y):
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.y = y
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

        if self.x <= - WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('assets/images/background.jpeg')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Game:

    def __init__(self):
        self.bg = [Background(0, 0), Background(WIDTH, 0)]
        self.speed = 5
        self.ilana = Ilana()
        self.bananas = []

    def time_to_spawn(self, loops):
        return loops % 100 == 0

    def spawn_banana(self):
        if len(self.bananas) > 0:
            previous_banana = self.bananas[-1]
            x = random.randint(previous_banana.x + self.ilana.width*2, WIDTH + previous_banana.x + self.ilana.width)
        else:
            x = random.randint(WIDTH + 200, 2000)
        banana = Banana(x)
        self.bananas.append(banana)
def main():
    game = Game()
    ilana = game.ilana
    #banana = game.banana
    clock = pygame.time.Clock()
    loops = 0
    # mainloop
    while True:
        loops += 1
        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        ilana.update(loops)
        ilana.show()

        if game.time_to_spawn(loops):
            game.spawn_banana()
        for banana in game.bananas:
            banana.update(-game.speed)
            banana.show()

        # Show bananas

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if ilana.onground:
                        ilana.jump()
        clock.tick(80)
        pygame.display.update()

if __name__ == '__main__':
    main()
