import pygame
from isometric_engine.config import *
from isometric_engine.control import *
from isometric_engine.grid import *
from isometric_engine.render_info import *
from isometric_engine.isometric_perspective import *
from isometric_engine.debug_text import *

# Initialize stuff before loop
pygame.init()

# Main engine stuff
clock = pygame.time.Clock()
screen = pygame.display.set_mode((CONF_WINDOW_WIDTH, CONF_WINDOW_HEIGHT))
render_info = RenderInfo()
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

        # Checking for mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_BUTTONS = pygame.mouse.get_pressed()
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSE_BUTTONS = pygame.mouse.get_pressed()

    # After events
    # Dragging check start
    if MOUSE_BUTTONS[0]:  # Left mouse button
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        # Populate mouse dragging history properly
        MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][0] = mouse_pos_x
        MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][1] = mouse_pos_y

        # Switch frame for mouse
        MOUSE_FRAME_SWITCH += 1
        MOUSE_FRAME_SWITCH = MOUSE_FRAME_SWITCH % 2

        if not MOUSE_DRAGGING and MOUSE_DRAGGING_HISTORY[0][0] != -1 and MOUSE_DRAGGING_HISTORY[1][0] != -1:
            rel_drag_x, rel_drag_y = (
                    MOUSE_DRAGGING_HISTORY[(MOUSE_FRAME_SWITCH + 1) % 2][0] - MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][0],
                    MOUSE_DRAGGING_HISTORY[(MOUSE_FRAME_SWITCH + 1) % 2][1] - MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][1])
            if rel_drag_x != 0 or rel_drag_y != 0:
                MOUSE_DRAGGING = True

    else:
        MOUSE_DRAGGING = False
        MOUSE_DRAGGING_HISTORY = [[-1, -1], [-1, -1]]
        MOUSE_FRAME_SWITCH = 0

    # If here we have mouse_frame_switch set that means we have at least two values in dragging history
    # Check for the differece
    if MOUSE_DRAGGING:
        MOUSE_DRAGGING_FRAME_DISTANCE = (
                MOUSE_DRAGGING_HISTORY[(MOUSE_FRAME_SWITCH + 1) % 2][0] - MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][0],
                MOUSE_DRAGGING_HISTORY[(MOUSE_FRAME_SWITCH + 1) % 2][1] - MOUSE_DRAGGING_HISTORY[MOUSE_FRAME_SWITCH][1])
        render_info.cam_offset_x += MOUSE_DRAGGING_FRAME_DISTANCE[0]
        render_info.cam_offset_y += MOUSE_DRAGGING_FRAME_DISTANCE[1]


    # Calculate delta time
    dt = clock.tick(CONF_FPS) / 1000.0

    # Fill screen with the background color
    screen.fill(CONF_BACKGROUND_COLOR)

    # Render stuff
    # UI stuff


    # Render isometric grid of water
    draw_grid_chunk(screen, render_info, GRID_CHUNK)

    # Debug text
    # TODO: Move this functions to debug_text.py
    if DEBUG:
        dt_text = debug_font.render(f"Delta Time: {dt: .4f} sec", True, text_color)
        screen.blit(dt_text, (10, 10))

        camera_offset_text = debug_font.render(
                f"Camera offset --> x: {render_info.cam_offset_x}, y: {render_info.cam_offset_y}", True, text_color)
        screen.blit(camera_offset_text, (10, 10 + 16 * 1))

        mouse_buttons_text = debug_font.render(f"Pressed mouse buttons: {MOUSE_BUTTONS}", True, text_color)
        screen.blit(mouse_buttons_text, (10, 10 + 16 * 2))

        if MOUSE_DRAGGING:
            mouse_drag_text = debug_font.render(
                    f"Mouse dragging distance --> x: {MOUSE_DRAGGING_FRAME_DISTANCE[0]}, y: {MOUSE_DRAGGING_FRAME_DISTANCE[1]}", True, text_color)
            screen.blit(mouse_drag_text, (10, 10 + 16 * 3))

    # Update FPS counter in window title
    pygame.display.set_caption(f"{CONF_WINDOW_TITLE} FPS: {clock.get_fps(): .2f}")

    # Update the display
    pygame.display.flip()

# Out of the loop - exit stuff
pygame.quit()

