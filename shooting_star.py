import pygame
import random


class ShootingStar:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.active = False
        self.timer = random.randint(15, 20) * 1000
        self.last_spawn = pygame.time.get_ticks()


    def spawn(self):

        self.active = True

        self.x = random.randint(-200, self.width)

        self.y = random.randint(-100, self.height // 2)

        self.speed_x = random.randint(3, 6)
        self.speed_y = random.randint(2, 3)


    def update(self):

        now = pygame.time.get_ticks()

        if not self.active:

            if now - self.last_spawn > self.timer:

                self.spawn()

        else:

            self.x += self.speed_x
            self.y += self.speed_y

            if (
                self.x > self.width + 200
                or
                self.y > self.height + 200
            ):

                self.active = False
                self.last_spawn = now
                self.timer = random.randint(3, 7) * 1000


    def draw(self, screen):

        if not self.active:
            return

        for i in range(25):

            alpha = max(0, 255 - i * 10)

            surface = pygame.Surface(
                (8, 8),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                surface,
                (255, 255, 180, alpha),
                (4, 4),
                4
            )

            screen.blit(
                surface,
                (
                    self.x - i * 8,
                    self.y - i * 4
                )
            )

        pygame.draw.circle(
            screen,
            (255,255,255),
            (int(self.x), int(self.y)),
            3
        )