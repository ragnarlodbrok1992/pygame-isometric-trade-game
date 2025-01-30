import pygame

from dataclasses import dataclass
from typing import List, Tuple

from .ui_state import *
from .config import *

@dataclass
class Console:
    command: str = ''
    ready: bool = False
    cursor_blink: float = 0.0
    cursor_width: int = CONF_CONSOLE_FONT_WIDTH
    cursor_height: int = CONF_CONSOLE_FONT_SIZE
    cursor_pos: Tuple[int, int] = (CONF_CONSOLE_POINTS_BOTTOM_LEFT[0], CONF_CONSOLE_POINTS_BOTTOM_LEFT[1] - CONF_CONSOLE_FONT_SIZE)  # Calculated dynamically every draw call
    

# TODO: use this to move (animate) console
def offset_console_points(console_points: List[Tuple[int, int]], offset: float) -> None:
    pass

def draw_console(screen: pygame.surface.Surface, console: Console, ui_state: UIState, dt: float) -> None:
    # Draw Console
    pygame.draw.polygon(screen, CONF_CONSOLE_COLOR, CONF_CONSOLE_POINTS)
    # Draw Input strip
    pygame.draw.polygon(screen, CONF_CONSOLE_INPUT_STRIP_COLOR, CONF_CONSOLE_INPUT_STRIP_POINTS)
    # Draw blinking cursor
    if console.cursor_blink < 0.5:
        # TODO: Calculate cursor pos based on command - for now we don't move it, because we don't support writing commands
        rel_cursor_pos = (console.cursor_pos[0] + (len(console.command) * console.cursor_width), console.cursor_pos[1])
        cursor_points = [
            rel_cursor_pos,
            (rel_cursor_pos[0] + console.cursor_width, rel_cursor_pos[1]),
            (rel_cursor_pos[0] + console.cursor_width, rel_cursor_pos[1] + console.cursor_height),
            (rel_cursor_pos[0], rel_cursor_pos[1] + console.cursor_height),
                ]
        pygame.draw.polygon(screen, CONF_CONSOLE_CURSOR_COLOR, cursor_points)
    elif console.cursor_blink > 1.0:
        console.cursor_blink = 0.0
    console.cursor_blink += dt
    # Draw input text
    console_input_text = DEBUG_FONT.render(console.command, True, CONF_CONSOLE_FONT_COLOR)
    screen.blit(console_input_text, (console.cursor_pos))
