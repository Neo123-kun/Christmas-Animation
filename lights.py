import math
import random
import pygame
from settings import *
from tree import tier_geometry


def lerp_color(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Light:
    def __init__(self, x, y, color, rng):
        self.x = round(x)
        self.y = round(y)
        self.color = color
        self.dim_color = lerp_color((0, 0, 0), color, LIGHT_DIM)
        self.glow_color = lerp_color((0, 0, 0), color, 0.45)
        self.speed = rng.uniform(LIGHT_BLINK_MIN, LIGHT_BLINK_MAX)
        self.phase = rng.uniform(0, math.tau) 

    def draw(self, surface, elapsed):
        t = 0.5 + 0.5 * math.sin(elapsed * self.speed + self.phase)

        pygame.draw.rect(surface, lerp_color(self.dim_color, self.color, t),
                         (self.x, self.y, LIGHT_SIZE, LIGHT_SIZE))

        if t > 0.85: 
            s = LIGHT_SIZE
            for dx, dy in [(-1, 0), (s, 0), (0, -1), (0, s)]:
                surface.fill(self.glow_color, (self.x + dx, self.y + dy, 1, 1))


def create_lights():
    rng = random.Random(LIGHT_SEED)
    lights = []

    for apex_y, base_y, half_w in tier_geometry():
        placed = []
        tries = 0
        while len(placed) < LIGHTS_PER_TIER and tries < 300:
            tries += 1
            y = rng.uniform(base_y - LIGHT_BAND_H, base_y - 3)

            reach = half_w * (y - apex_y) / TIER_HEIGHT - LIGHT_EDGE_MARGIN
            if reach <= 0:
                continue
            x = TREE_CENTER_X + rng.uniform(-reach, reach)

            if any(math.hypot(x - px, y - py) < LIGHT_MIN_DIST for px, py in placed):
                continue
            placed.append((x, y))

        for x, y in placed:
            lights.append(Light(x, y, rng.choice(LIGHT_COLORS), rng))

    return lights


def draw_lights(surface, lights, elapsed):
    for light in lights:
        light.draw(surface, elapsed)