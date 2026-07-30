import pygame


class InfoPanel:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "arial",
            22
        )


    def draw(self, screen, planet):

        if planet is None:
            return


        x = 30
        y = 30


        width = 300
        height = 250


        panel = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )


        panel.fill(
            (20, 20, 30, 220)
        )


        screen.blit(
            panel,
            (x, y)
        )


        title = self.font.render(
            planet.name,
            True,
            (255,255,255)
        )


        screen.blit(
            title,
            (x+20,y+20)
        )


        line_y = y + 60


        for key,value in planet.info.items():

            text = self.font.render(
                f"{key}: {value}",
                True,
                (220,220,220)
            )


            screen.blit(
                text,
                (x+20,line_y)
            )


            line_y += 35