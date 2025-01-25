import pygame
from isometric_engine.config import *
from isometric_engine.control import *
from isometric_engine.grid import *
from isometric_engine.isometric_perspective import *

# Initialize stuff before loop
pygame.init()

# Main engine stuff
clock = pygame.time.Clock()
screen = pygame.display.set_mode((CONF_WINDOW_WIDTH, CONF_WINDOW_HEIGHT))
pygame.display.set_caption(CONF_WINDOW_TITLE)

# UI stuff
debug_font = pygame.font.SysFont("Fira Code Medium", CONF_UI_FONT_SIZE, bold=True)
text_color = (255, 255, 255)

DEBUG = False

while CNTRL_ENGINE_RUNNING:
    # Event handling
    for event in pygame.event.get():
        # Check if quitting
        if event.type == pygame.QUIT:
            CNTRL_ENGINE_RUNNING = False

        # Check for keyboard input
        if event.type == pygame.KEYDOWN:
            # Check for Q - quit the game
            if event.key == pygame.K_q:
                CNTRL_ENGINE_RUNNING = False
            # Turning debug on and off
            if pygame.key.get_mods() & pygame.KMOD_LCTRL and event.key == pygame.K_F11:
                DEBUG = not DEBUG

    # Calculate delta time
    dt = clock.tick(CONF_FPS) / 1000.0

    # Fill screen with the background color
    screen.fill(CONF_BACKGROUND_COLOR)

    # Render stuff
    # UI stuff

    # Debug text
    if DEBUG:
        dt_text = debug_font.render(f"Delta Time: {dt: .4f} sec", True, text_color)
        screen.blit(dt_text, (10, 10))

    # Render isometric grid of water
    draw_grid_chunk(screen, GRID_CHUNK)

    # Update FPS counter in window title
    pygame.display.set_caption(f"{CONF_WINDOW_TITLE} FPS: {clock.get_fps(): .2f}")

    # Update the display
    pygame.display.flip()

# Out of the loop - exit stuff
pygame.quit()

