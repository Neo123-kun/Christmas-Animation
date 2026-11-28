import math
import pygame
from lights import lerp_color
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

def draw_star(surface, elapsed):
    cx, cy = TREE_CENTER_X, STAR_CENTER_Y

    # 0..1 pulse, same sine trick as the lights
    t = 0.5 + 0.5 * math.sin(elapsed * STAR_TWINKLE_SPEED)

    # 1. gold body (never changes)
    body = star_points(cx, cy, STAR_OUTER_R, STAR_INNER_R)
    pygame.draw.polygon(surface, STAR_COLOR, body)

    # 2. sparkle rays, only near the peak of the pulse
    if t > STAR_SPARKLE_AT:
        fade = (t - STAR_SPARKLE_AT) / (1 - STAR_SPARKLE_AT)   # 0 to 1 within the peak
        ray = lerp_color(STAR_COLOR, STAR_RAY_COLOR, fade)
        reach = STAR_OUTER_R + STAR_SPARKLE_LEN
        down = round(STAR_OUTER_R * 0.8)                       # stop above the tree
        surface.fill(ray, (cx - reach, cy, reach * 2 + 1, 1))  # horizontal ray
        surface.fill(ray, (cx, cy - reach, 1, reach + down + 1))  # vertical ray

    # 3. pulsing shine on top (size and color both follow t)
    scale = STAR_SHINE_MIN + (STAR_SHINE_MAX - STAR_SHINE_MIN) * t
    shine = star_points(cx, cy, STAR_OUTER_R * scale, STAR_INNER_R * scale)
    pygame.draw.polygon(surface, lerp_color(STAR_COLOR, STAR_HIGHLIGHT, t), shine)