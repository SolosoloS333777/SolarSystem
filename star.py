import pygame
import random


class Star:

    def __init__(self, width, height):

        self.x = random.randint(0, width)
        self.y = random.randint(0, height)

        self.size = random.randint(1, 3)

        self.brightness = random.randint(120, 255)

        self.direction = random.choice([-1, 1])

        self.speed = random.randint(1, 3)


    def update(self):

        self.brightness += self.direction * self.speed

        if self.brightness >= 255:
            self.brightness = 255
            self.direction = -1

        if self.brightness <= 80:
            self.brightness = 80
            self.direction = 1


    def draw(self, screen):

        color = (
            self.brightness,
            self.brightness,
            self.brightness
        )

        pygame.draw.circle(
            screen,
            color,
            (self.x, self.y),
            self.size
        )