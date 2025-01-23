import pygame
from isometric_engine.config import *

# Initialize stuff before loop
pygame.init()

# Main engine stuff
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# UI stuff
debug_font = pygame.font.SysFont("Fira Code Medium", UI_FONT_SIZE, bold=True)
text_color = (255, 255, 255)

while ENGINE_RUNNING:
    # Event handling
    for event in pygame.event.get():
        # Check if quitting
        if event.type == pygame.QUIT:
            ENGINE_RUNNING = False

        # Check for keyboard input
        if event.type == pygame.KEYDOWN:
            # Check for Q - quit the game
            if event.key == pygame.K_q:
                ENGINE_RUNNING = False

    # Calculate delta time
    dt = clock.tick(FPS) / 1000.0

    # Fill screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Render stuff
    # UI stuff
    dt_text = debug_font.render(f"Delta Time: {dt: .4f} sec", True, text_color)

    screen.blit(dt_text, (10, 10))

    # Update FPS counter in window title
    pygame.display.set_caption(f"{WINDOW_TITLE} FPS: {clock.get_fps(): .2f}")

    # Update the display
    pygame.display.flip()

# Out of the loop - exit stuff
pygame.quit()

