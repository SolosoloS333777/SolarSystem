import pygame
import math


class Planet:

    def __init__(
        self,
        name,
        image_path,
        size,
        orbit_radius,
        speed,
        info,
        
    ):

        # Planet information
        self.name = name
        self.info = info
        self.trail = []
        # Load image
        
        self.original_image = pygame.image.load(
        image_path
        ).convert_alpha()

        self.original_image = pygame.transform.scale(
          self.original_image,
            (size, size)
        )

        self.image = self.original_image
        self.size = size

        # Movement
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = 0

        # Position
        self.x = 0
        self.y = 0


    def update(self, center, dt):

        # Increase angle based on time
        self.angle += self.speed * dt * 60

        # Calculate position
        self.x = (
            center[0]
            + math.cos(math.radians(self.angle))
            * self.orbit_radius
        )

        self.y = (
            center[1]
            + math.sin(math.radians(self.angle))
            * self.orbit_radius
        )

        self.trail.append((self.x, self.y))

        trail_lengths = {
            "Mercury": 35,
            "Venus": 45,
            "Earth": 60,
            "Mars": 70,
            "Jupiter": 300,
            "Saturn": 410,
            "Uranus": 720,
            "Neptune": 999,
            "Moon": 25
        }

        max_trail = trail_lengths.get(
            self.name,
            60
        )

        if len(self.trail) > max_trail:
            self.trail.pop(0)


    def draw_orbit(self, screen, center, camera):

        center_x, center_y = camera.world_to_screen(
        center[0],
        center[1]
        )

        pygame.draw.circle(
        screen,
        (80, 80, 80),
        (int(center_x), int(center_y)),
        int(self.orbit_radius * camera.zoom),
        1
        )

    def draw_trail(self, screen, camera):

        if len(self.trail) < 2:
            return

        colors = {
            "Mercury": (180, 180, 180),
            "Venus": (255, 220, 120),
            "Earth": (80, 170, 255),
            "Mars": (255, 90, 90),
            "Jupiter": (255, 170, 70),
            "Saturn": (255, 220, 120),
            "Uranus": (120, 255, 255),
            "Neptune": (70, 120, 255),
            "Moon": (220, 220, 220)
        }

        color = colors.get(self.name, (255, 255, 255))

        for i, point in enumerate(self.trail):

            x, y = camera.world_to_screen(
                point[0],
                point[1]
            )

            progress = i / len(self.trail)

            radius = max(
                1,
                int(progress * 6)
            )

            alpha = int(progress * 180)

            glow = pygame.Surface(
                (radius * 8, radius * 8),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (*color, alpha),
                (
                    glow.get_width() // 2,
                    glow.get_height() // 2
                ),
                radius
            )

            screen.blit(
                glow,
                (
                    x - glow.get_width() // 2,
                    y - glow.get_height() // 2
                )
            )
    def draw(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(
          self.x,
          self.y
        )

        scaled_size = max(
           4,
           int(self.size * camera.zoom)
        )

        image = pygame.transform.smoothscale(
           self.original_image,
           (scaled_size, scaled_size)
        )

        rect = image.get_rect(
         center=(screen_x, screen_y)
        )

        screen.blit(
           image,
           rect
        )
    def draw_highlight(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.x,
            self.y
        )

        radius = int(
            self.size * camera.zoom / 2 + 8
        )

        pygame.draw.circle(
            screen,
            (255, 255, 100),
            (
                int(screen_x),
                int(screen_y)
            ),
            radius,
            2
        )
    def get_position(self):
        return (self.x, self.y)
    def is_hovered(self, mouse_pos, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.x,
            self.y
        )

        distance = math.sqrt(
            (mouse_pos[0] - screen_x) ** 2 +
            (mouse_pos[1] - screen_y) ** 2
        )

        return distance < self.size * camera.zoom
    def is_clicked(self, mouse_pos, camera):

        screen_x, screen_y = camera.world_to_screen(
         self.x,
         self.y
        )

        distance = math.sqrt(
          (mouse_pos[0] - screen_x) ** 2 +
          (mouse_pos[1] - screen_y) ** 2
        )

        return distance < self.size * camera.zoom
    