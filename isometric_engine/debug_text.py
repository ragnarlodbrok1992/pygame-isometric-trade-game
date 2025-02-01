import pygame

from .config import *

class DebugText:
    def __init__(self) -> None:
        self.debug_y = CONF_WINDOW_HEIGHT - 16
        self.debug_num_of_messages = 0
        self.debug_left_margin = 10
        self.debug_text_color = (255, 255, 255)
        self.debug_font = pygame.font.SysFont("Fira Code Medium", CONF_UI_FONT_SIZE, bold=True)

    def reset_debug_ui(self) -> None:
        self.debug_num_of_messages = 0

    def draw_debug_text(self, screen: pygame.Surface, text: str) -> None:
        text_texture = self.debug_font.render(text, True, self.debug_text_color)
        screen.blit(text_texture, (self.debug_left_margin, self.debug_y - 16 * self.debug_num_of_messages))
        self.debug_num_of_messages += 1

