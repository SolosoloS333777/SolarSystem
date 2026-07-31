import pygame
import sys

from settings import *
from planet import Planet
from star import Star
from sun import Sun
from camera import Camera
from info_panel import InfoPanel
from shooting_star import ShootingStar


pygame.init()


# -----------------------
# Window
# -----------------------

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()
camera = Camera()
info_panel = InfoPanel()
font = pygame.font.SysFont(
    "arial",
    22
)


# -----------------------
# Stars
# -----------------------

stars = []

for i in range(400):
    stars.append(
        Star(WIDTH, HEIGHT)
    )

shooting_star = ShootingStar(
    WIDTH,
    HEIGHT
)

# -----------------------
# Background
# -----------------------

background = pygame.image.load(
    "assets/background.jpg"
)

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)


# -----------------------
# Sun
# -----------------------

sun = Sun(
    "assets/sun.png",
    80,
    CENTER
)


# -----------------------
# Moon
# -----------------------

moon = Planet(
    "Moon",
    "assets/moon.png",
    12,
    45,
    2.5,
    {
    "distance": "384,400 km",
    "diameter": "3,474 km",
    "moons": "It is Earth's moon itself",
    "year": "27.3 days"
    }
    
)


# -----------------------
# Planets
# -----------------------

mercury = Planet(
    "Mercury",
    "assets/mercury.png",
    20,
    50,
    4.15,
    {
    "distance": "57.9 million km",
    "diameter": "4,879 km",
    "moons": "0",
    "year": "88 days"
    }
)

venus = Planet(
    "Venus",
    "assets/venus.png",
    28,
    80,
    1.62,
    {
    "distance": "108.2 million km",
    "diameter": "12,104 km",
    "moons": "0",
    "year": "225 days"
    }
)

earth = Planet(
    "Earth",
    "assets/earth.png",
    32,
    120,
    1.0,
    {
        "distance": "149.6 million km",
        "diameter": "12,742 km",
        "moons": "1",
        "year": "365 days"
    }
)

mars = Planet(
    "Mars",
    "assets/mars.png",
    24,
    160,
    0.53,
    {
        "distance": "227.9 million km",
        "diameter": "6,779 km",
        "moons": "2",
        "year": "687 days"
    }
)

jupiter = Planet(
    "Jupiter",
    "assets/jupiter.png",
    55,
    210,
    0.084,
    {
    "distance": "778.5 million km",
    "diameter": "139,820 km",
    "moons": "95",
    "year": "11.86 years"
    }
)

saturn = Planet(
    "Saturn",
    "assets/saturn.png",
    60,
    260,
    0.034,
    {
    "distance": "1.43 billion km",
    "diameter": "116,460 km",
    "moons": "146",
    "year": "29.5 years"
    }
)

uranus = Planet(
    "Uranus",
    "assets/uranus.png",
    45,
    310,
    0.012,
    {
    "distance": "2.87 billion km",
    "diameter": "50,724 km",
    "moons": "28",
    "year": "84 years"
    }
)

neptune = Planet(
    "Neptune",
    "assets/neptune.png",
    45,
    360,
    0.006,
    {
    "distance": "4.5 billion km",
    "diameter": "49,244 km",
    "moons": "16",
    "year": "164.8 years"
    }
)


planets = [
    
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune,
    
]

clickable_objects = [
    moon,
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune
]
selected_planet = None

time_scale = 1.0
paused = False

def draw_text(text, x, y):

    label = font.render(
        text,
        True,
        (255,255,255)
    )

    rect = label.get_rect(
        center=(x,y)
    )

    screen.blit(
        label,
        rect
    )
# -----------------------
# Game Loop
# -----------------------

running = True

while running:

    dt = clock.tick(FPS) / 1000
    camera.follow()

    if not camera.manual_zoom:
     camera.zoom_to_target()
  
    


    


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Faster
            if event.key == pygame.K_UP:
                time_scale *= 2

            # Slower
            elif event.key == pygame.K_DOWN:
                time_scale /= 2

            # Limit
            time_scale = max(0.125, min(time_scale, 16))

            # Pause / Resume
            if event.key == pygame.K_SPACE:
                paused = not paused
            

        # Zoom
        if event.type == pygame.MOUSEWHEEL:

            camera.manual_zoom = True

            if event.y > 0:
                camera.zoom *= 1.1

            if event.y < 0:
                camera.zoom /= 1.1

            camera.zoom = max(
                0.3,
                min(camera.zoom, 5)
            )


        # Mouse press
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_pos = pygame.mouse.get_pos()

                clicked = False


                if sun.is_clicked(mouse_pos, camera):

                    if selected_planet == sun:

                        camera.target = sun
                        camera.target_zoom = 3.0
                        camera.manual_zoom = False

                    else:

                        selected_planet = sun

                    clicked = True

                for planet in clickable_objects:

                    if planet.is_clicked(
                    mouse_pos,
                    camera
                        ):

                    # If already chosen --> clicking again
                        if selected_planet == planet:

                            camera.target = planet
                            camera.target_zoom = 3.0
                            camera.manual_zoom = False

                        # Just one/first cllick
                        else:

                            selected_planet = planet

                        clicked = True
                        break


                # Camera muvement if nothing is clicked
                if not clicked:

                    selected_planet =None
                    hovered_planet = None

                    # stop following object
                    camera.target = None

                    # return to full solar system view
                    camera.target_zoom = 1.0
                    camera.manual_zoom = False

                    # reset camera position
                    camera.offset_x = 0
                    camera.offset_y = 0

                    camera.dragging = True
                    camera.last_mouse = mouse_pos



        # Mouse release
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                camera.dragging = False

    hovered_planet = None

    mouse_pos = pygame.mouse.get_pos()
    # Check Sun first
    if sun.is_clicked(
        mouse_pos,
        camera
    ):
        hovered_planet = sun


    # Check planets
    else:
        for planet in clickable_objects:

            if planet.is_hovered(
            mouse_pos,
            camera
            ):
             hovered_planet = planet
             break
    # Stop drag
    if event.type == pygame.MOUSEBUTTONUP:

        if event.button == 1:

            camera.dragging = False
        # Stop Drag
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                camera.dragging = False
                    # Mouse click / Drag

    if camera.dragging:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - camera.last_mouse[0]
        dy = mouse_y - camera.last_mouse[1]

        camera.offset_x += dx / camera.zoom
        camera.offset_y += dy / camera.zoom

        camera.last_mouse = (
            mouse_x,
            mouse_y
        )
    # -----------------------
    # Draw Background
    # -----------------------

    screen.blit(
        background,
        (0, 0)
    )


    # -----------------------
    # Draw Stars
    # -----------------------

    for star in stars:
        star.update()
        star.draw(screen)
        shooting_star.update()
        shooting_star.draw(screen)



    # -----------------------
    # Update + Draw Planets
    # -----------------------

    # -----------------------
    # Update + Draw Planets
    # -----------------------

    for planet in planets:

        

        if not paused:
                planet.update(
                    CENTER,
                    dt * time_scale
                )

        if paused and len(planet.trail) > 0:
            planet.trail.pop(0)

   

        planet.draw_orbit(
         screen,
         CENTER,
         camera
        )
        planet.draw_trail(
            screen,
            camera
        )

        planet.draw(
          screen,
         camera
        )


    # -----------------------
    # Moon around Earth
    # -----------------------

    earth_position = earth.get_position()

    if not paused:
      moon.update(
        earth_position,
        dt * time_scale
      )

    moon.draw_orbit(
        screen,
        earth_position,
        camera
    )

    moon.draw(
        screen,
        camera
    )



    # -----------------------
    # Draw Sun
    # -----------------------

    if not paused:
        sun.update()

    sun.draw_glow(screen, camera)

    sun.draw(screen, camera)
    

    # Selected object highlight
    
    if hovered_planet:

        if hovered_planet == sun:

            sun.draw_highlight(
                screen,
                camera
            )

        else:

            hovered_planet.draw_highlight(
                screen,
                camera
            )
    if hovered_planet:

        if hovered_planet == sun:

            x, y = camera.world_to_screen(
                sun.position[0],
                sun.position[1]
            )

        else:

            x, y = camera.world_to_screen(
                hovered_planet.x,
                hovered_planet.y
            )


   
        draw_text(
            hovered_planet.name,
            x,
            y - 40
        )
    if selected_planet:
  
        if selected_planet == sun:

            sun.draw_highlight(screen, camera)

        else:

            selected_planet.draw_highlight(
                screen,
                camera
            )
    info_panel.draw(
        screen,
        selected_planet
    )



    pygame.display.flip()



pygame.quit()
sys.exit()
