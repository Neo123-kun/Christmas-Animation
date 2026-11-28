import pygame
from settings import *


class SnowPile:
    def __init__(self):
        self.heights = [0.0] * CANVAS_W

    def height_at(self, x):
        return self.heights[int(x) % CANVAS_W]

    def add(self, x):
        """A flake landed at column x. Let it roll downhill, then stack."""
        x = int(x) % CANVAS_W

        for _ in range(6):
            here = self.heights[x]
            left = self.heights[(x - 1) % CANVAS_W]
            right = self.heights[(x + 1) % CANVAS_W]
            if left < here - PILE_SLOPE and left <= right:
                x = (x - 1) % CANVAS_W
            elif right < here - PILE_SLOPE:
                x = (x + 1) % CANVAS_W
            else:
                break

        self.heights[x] = min(self.heights[x] + PILE_GROW, PILE_MAX_H)

    def clear(self):
        self.heights = [0.0] * CANVAS_W

    def draw(self, surface):
        for x, h in enumerate(self.heights):
            h = int(h)
            if h > 0:
                surface.fill(PILE_COLOR, (x, GROUND_Y - h, 1, h))
                surface.fill(PILE_TOP_COLOR, (x, GROUND_Y - h, 1, 1))