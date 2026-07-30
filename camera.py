from settings import WIDTH, HEIGHT


class Camera:

    def __init__(self):

        self.zoom = 1.0
        self.target_zoom = 1.0

        self.offset_x = 0
        self.offset_y = 0
        self.manual_zoom = False

        self.dragging = False
        self.last_mouse = (0, 0)

        self.target = None
        self.follow_speed = 0.05


    def world_to_screen(self, x, y):

        screen_x = (
            (x + self.offset_x - WIDTH / 2)
            * self.zoom
            + WIDTH / 2
        )

        screen_y = (
            (y + self.offset_y - HEIGHT / 2)
            * self.zoom
            + HEIGHT / 2
        )

        return screen_x, screen_y


    def follow(self):

        if self.target:

            if hasattr(self.target, "x"):

                target_x = self.target.x
                target_y = self.target.y

            else:

                target_x = self.target.position[0]
                target_y = self.target.position[1]


            self.offset_x += (
                WIDTH / 2
                - target_x
                - self.offset_x
            ) * self.follow_speed


            self.offset_y += (
                HEIGHT / 2
                - target_y
                - self.offset_y
            ) * self.follow_speed


    def zoom_to_target(self):

        self.zoom += (
            self.target_zoom - self.zoom
        ) * 0.05