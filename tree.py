import pygame
from settings import *

# Ground
def draw_ground(surface):
    pygame.draw.rect(surface, GROUND_COLOR, (0, GROUND_Y, CANVAS_W, CANVAS_H - GROUND_Y))

# Trunk
def draw_trunk(surface):
    x = TREE_CENTER_X - TRUNK_W // 2
    y = TREE_BASE_Y - 4
    h = TRUNK_H + 4
    half = TRUNK_W // 2

    pygame.draw.rect(surface, TRUNK_COLOR_LEFT, (x, y, half, h))
    pygame.draw.rect(surface, TRUNK_COLOR_RIGHT, (x + half, y, TRUNK_W - half, h))

# Tree
def draw_tree(surface):
    draw_trunk(surface)
   
    total_height = TREE_BASE_Y - TREE_TOP_Y
    step = (total_height - TIER_HEIGHT) / (TREE_TIERS - 1)
    cx = TREE_CENTER_X

# Overlap fix
    for i in reversed(range(TREE_TIERS)):
        t = i / (TREE_TIERS - 1)
        half_w = TREE_TOP_HALF_W + (TREE_BOTTOM_HALF_W - TREE_TOP_HALF_W) * t

        apex_y = TREE_TOP_Y + step * i
        base_y = apex_y + TIER_HEIGHT

        apex = (cx, round(apex_y))
        left = (round(cx - half_w), round(base_y))
        right = (round(cx + half_w), round(base_y))
        mid = (cx, round(base_y))

        pygame.draw.polygon(surface, LEAF_LIGHT, [apex, left, mid]) 
        pygame.draw.polygon(surface, LEAF_DARK, [apex, mid, right]) 
        pygame.draw.line(surface, LEAF_EDGE, left, right) 

# Helper for lights
def tier_geometry():
    """Return (apex_y, base_y, half_width) for each tier, top tier first."""
    total_height = TREE_BASE_Y - TREE_TOP_Y
    step = (total_height - TIER_HEIGHT) / (TREE_TIERS - 1)
    tiers = []
    for i in range(TREE_TIERS):
        t = i / (TREE_TIERS - 1)
        half_w = TREE_TOP_HALF_W + (TREE_BOTTOM_HALF_W - TREE_TOP_HALF_W) * t
        apex_y = TREE_TOP_Y + step * i
        tiers.append((apex_y, apex_y + TIER_HEIGHT, half_w))
    return tiers