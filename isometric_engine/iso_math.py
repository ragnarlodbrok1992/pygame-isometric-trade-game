import pygame

type Vec2 = pygame.math.Vector2

def lerp_vec2(new_value: Vec2, old_value: Vec2, percent: float) -> Vec2:
    diff_x = pygame.math.lerp(new_value.x, old_value.x, percent)
    diff_y = pygame.math.lerp(new_value.y, old_value.y, percent)
    return pygame.math.Vector2(diff_x, diff_y)
