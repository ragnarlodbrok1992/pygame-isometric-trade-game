import pygame
import random
import string

from pathlib import Path

# Engine stuff
from isometric_engine.config import *
from isometric_engine.control import *
from isometric_engine.debug_text import *
from isometric_engine.grid import *
from isometric_engine.render_info import *
from isometric_engine.isometric_perspective import *
from isometric_engine.game_state import *
from isometric_engine.ui_state import *
from isometric_engine.console import *

# Game stuff
from isometric_engine.game.ship import *


# Initialize stuff before loop
pygame.init()

# Main engine library stuff
clock = pygame.time.Clock()
screen: pygame.Surface = pygame.display.set_mode((CONF_WINDOW_WIDTH, CONF_WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption(CONF_WINDOW_TITLE)

pygame.key.set_repeat(500, 30)

# Main engine local stuff
debug_text = DebugText()
render_info = RenderInfo()
game_state = GameState()
ui_state = UIState()
console = Console()

# Inner game entities
ship = Ship()

# Assets loading - we try to do that from here
ship_assets = Path('assets/ship')
ship.load_assets(ship_assets)

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
            # TODO: add switch for keyboard input for console on/off
            # TODO: design console input system - we need to populate Console.command variable and process it
            # after pushing ENTER key

            # Turning debug on and off
            if pygame.key.get_mods() & pygame.KMOD_LCTRL and event.key == pygame.K_F11:
                ui_state.debug_text_out = not ui_state.debug_text_out
                render_info.debug_render = not render_info.debug_render

            if not console.ready:
                # Check for Q - quit the game
                if event.key == pygame.K_q:
                    CNTRL_ENGINE_RUNNING = False

                # DEBUG - pygame.K_w is here to resize chunk
                if event.key == pygame.K_w:
                    GRID_CHUNK = resize_grid_chunk(GRID_CHUNK, 20, 20)

            else:
                # FIXME I think we do think badly here about appending characters to string - but fuck that for now
                if event.unicode == '\x08':
                    console.command = console.command[:-1]
                elif event.unicode == '\r':
                    print("[CONSOLE] Pressed enter! Validate command")  # TODO: create validation logic for console input command
                else:
                    console.command += event.unicode

            if event.key == pygame.K_BACKQUOTE:
                ui_state.console_out = not ui_state.console_out
                console.ready = not console.ready  # TODO console will be ready after animation - right now we are ready immediately
                console.command = ''

        # Checking for mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_BUTTONS = pygame.mouse.get_pressed()
            MOUSE_SELECTION_GAME_AREA = True  # There are no UI elements right now

        elif event.type == pygame.MOUSEBUTTONUP:
            if MOUSE_SELECTION_GAME_AREA and not MOUSE_DRAGGING:
                # We clicked stuff and we are not dragging - right now we try to look for a grid tile to select
                # TODO: possible bug - we might not have click position data here but I might be wrong
                #                      I think only when one have button down and button down in the same frame???
                # print("Clicking!")
                # FIXME: This global state is still not working
                if MOUSE_BUTTONS[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    get_tile_from_grid(GRID_CHUNK, render_info, game_state, mouse_pos)

            MOUSE_BUTTONS = pygame.mouse.get_pressed()

            MOUSE_SELECTION_GAME_AREA = False

    # After events - still processing controls!
    # Dragging check start
    # TODO: Move mousing to it's own class
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
    # Render isometric grid of water
    draw_grid_chunk(screen, render_info, game_state, GRID_CHUNK)

    # Render objects
    ship.render_ship(screen, render_info)

    # UI stuff
    if ui_state.console_out:
        draw_console(screen, console, ui_state, dt)

    # Debug text
    # TODO: Move this functions to debug_text.py
    if ui_state.debug_text_out:
        debug_text.draw_debug_text(screen, f"Delta Time: {dt: .4f} sec")
        debug_text.draw_debug_text(screen, f"Camera offset --> x: {render_info.cam_offset_x}, y: {render_info.cam_offset_y}")
        debug_text.draw_debug_text(screen, f"Pressed mouse buttons: {MOUSE_BUTTONS}")
        debug_text.draw_debug_text(screen, f"Current mouse position: {pygame.mouse.get_pos()}")
        if MOUSE_DRAGGING:
            debug_text.draw_debug_text(screen, f"Mouse dragging distance --> x: {MOUSE_DRAGGING_FRAME_DISTANCE[0]}, y: {MOUSE_DRAGGING_FRAME_DISTANCE[1]}")

    debug_text.reset_debug_ui();  # TODO: calling this is required every end of the frame - don't know how to tackle that yet

    # Update FPS counter in window title
    pygame.display.set_caption(f"{CONF_WINDOW_TITLE} FPS: {clock.get_fps(): .2f}")

    # Update the display
    pygame.display.flip()

# Out of the loop - exit stuff
pygame.quit()

