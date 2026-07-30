import pygame
import math


class Sun:

    def __init__(self, image_path, size, position):

        self.original_image = pygame.image.load(
            image_path
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
             self.original_image,
             (size, size)
        )

        self.image = self.original_image

        self.position = position

        self.size = size

        self.time = 0
        
        self.angle = 0

        self.name = "Sun"

        self.info = {
            "type": "Star",
            "diameter": "1.39 million km",
            "temperature": "5,500 °C",
            "age": "4.6 billion years",
            "planets": "8"
        }


    def update(self):

        self.time += 0.05
        self.angle += 0.2


    def draw_glow(self, screen, camera):

        pulse = math.sin(self.time) * 20

        glow_radius = int(
            (self.size * camera.zoom) * 5 + pulse
        )


        glow_surface = pygame.Surface(
            (
                glow_radius * 2,
                glow_radius * 2
            ),
            pygame.SRCALPHA
        )


        for i in range(10, 0, -1):

            radius = int(
                glow_radius * i / 10
            )

            alpha = int(
                4 * i
            )

            pygame.draw.circle(
                glow_surface,
                (255, 180, 40, alpha),
                (
                    glow_radius,
                    glow_radius
                ),
                radius
            )


        screen_x, screen_y = camera.world_to_screen(
            self.position[0],
            self.position[1]
        )


        screen.blit(
            glow_surface,
            (
                screen_x - glow_radius,
                screen_y - glow_radius
            )
        )
    def draw(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.position[0],
            self.position[1]
        )


        scale = 1 + math.sin(self.time) * 0.03

        new_size = int(
                self.size * camera.zoom * scale
            )


        sun_image = pygame.transform.smoothscale(
                self.image,
                (new_size, new_size)
            )


        rotated_image = pygame.transform.rotate(
                sun_image,
                self.angle
            )


        rect = rotated_image.get_rect(
            center=(
                screen_x,
                screen_y
            )
        )


        screen.blit(
            rotated_image,
            rect
        )

        
    def is_clicked(self, mouse_pos, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.position[0],
            self.position[1]
        )

        distance = math.sqrt(
            (mouse_pos[0] - screen_x) ** 2 +
            (mouse_pos[1] - screen_y) ** 2
        )

        return distance < self.size * camera.zoom * 0.4
    def draw_highlight(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.position[0],
            self.position[1]
        )

        radius = int(
            self.size * camera.zoom / 2 + 12
        )

        pygame.draw.circle(
            screen,
            (255, 230, 100),
            (
                int(screen_x),
                int(screen_y)
            ),
            radius,
            3
        )

        