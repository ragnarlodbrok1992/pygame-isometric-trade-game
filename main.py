import pygame
from isometric_engine.config import *
from isometric_engine.control import *
from isometric_engine.grid import *
from isometric_engine.render_info import *
from isometric_engine.isometric_perspective import *
from isometric_engine.debug_text import *
from isometric_engine.game_state import *

# Initialize stuff before loop
pygame.init()

# Main engine library stuff
clock = pygame.time.Clock()
screen = pygame.display.set_mode((CONF_WINDOW_WIDTH, CONF_WINDOW_HEIGHT))
pygame.display.set_caption(CONF_WINDOW_TITLE)

# Main engine local stuff
render_info = RenderInfo()
game_state = GameState()

# UI stuff
debug_font = pygame.font.SysFont("Fira Code Medium", CONF_UI_FONT_SIZE, bold=True)
text_color = (255, 255, 255)

# Debug variables
DEBUG = False

while CNTRL_ENGINE_RUNNING:
    # =================== EVENT PROCESSING ==================
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
            MOUSE_SELECTION_GAME_AREA = True  # There are no UI elements right now

        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSE_BUTTONS = pygame.mouse.get_pressed()

            if MOUSE_SELECTION_GAME_AREA and not MOUSE_DRAGGING:
                # We clicked stuff and we are not dragging - right now we try to look for a grid tile to select
                # TODO: possible bug - we might not have click position data here but I might be wrong
                #                      I think only when one have button down and button down in the same frame???
                print("Clicking!")
                # FIXME: This global state is still not working
                mouse_pos = pygame.mouse.get_pos()
                get_tile_from_grid(GRID_CHUNK, render_info, game_state, mouse_pos)
                # print(hex(id(GAME_STATE_CLICKED_TILE)))
                # print(GAME_STATE_CLICKED_TILE)
                # print(hex(id(HANDLE_GAME_STATE)))
                # print(HANDLE_GAME_STATE)

            MOUSE_SELECTION_GAME_AREA = False
            # GAME_STATE_CLICKED_TILE = (-1, -1)

    # After events - still processing controls!
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

    # ================== FINISHING EVENT PROCESSING ===================


    # Calculate delta time
    dt = clock.tick(CONF_FPS) / 1000.0

    # Fill screen with the background color
    screen.fill(CONF_BACKGROUND_COLOR)

    # Render stuff
    # UI stuff


    # Render isometric grid of water
    draw_grid_chunk(screen, render_info, game_state, GRID_CHUNK)

    # Debug rendering
    # if normal_proj_grid_bounding_box_points:
    #         pygame.draw.polygon(screen, (255, 255, 255), normal_proj_grid_bounding_box_points, width=1)

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

        current_mouse_position_text = debug_font.render(f"Current mouse position: {pygame.mouse.get_pos()}", True, text_color)
        screen.blit(current_mouse_position_text, (10, 10 + 16 * 3))

        if MOUSE_DRAGGING:
            mouse_drag_text = debug_font.render(
                    f"Mouse dragging distance --> x: {MOUSE_DRAGGING_FRAME_DISTANCE[0]}, y: {MOUSE_DRAGGING_FRAME_DISTANCE[1]}", True, text_color)
            screen.blit(mouse_drag_text, (10, 10 + 16 * 4))

    # Update FPS counter in window title
    pygame.display.set_caption(f"{CONF_WINDOW_TITLE} FPS: {clock.get_fps(): .2f}")

    # Update the display
    pygame.display.flip()

# Out of the loop - exit stuff
pygame.quit()

