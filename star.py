import math
import pygame
from settings import *

# Points
def star_points(cx, cy, outer_r, inner_r, points=STAR_POINTS):
    corners = []
    total = points * 2
    for i in range(total):
        r = outer_r if i % 2 == 0 else inner_r
        angle = math.radians(-90 + i * (360 / total))
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        corners.append((round(x), round(y)))
    return corners

def draw_star(surface):
    cx, cy = TREE_CENTER_X, STAR_CENTER_Y

    body = star_points(cx, cy, STAR_OUTER_R, STAR_INNER_R)
    shine = star_points(cx, cy, STAR_OUTER_R * 0.55, STAR_INNER_R * 0.55)

    pygame.draw.polygon(surface, STAR_COLOR, body)
    pygame.draw.polygon(surface, STAR_HIGHLIGHT, shine)