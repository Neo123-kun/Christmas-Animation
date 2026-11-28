import math
import random
import pygame
from settings import *


class Snowflake:
    def __init__(self, rng):
        self.rng = rng
        self.far = rng.random() < SNOW_FAR_FRACTION

        if self.far:
            self.speed = rng.uniform(*SNOW_SPEED_FAR)
            self.size = 1
            self.color = SNOW_COLOR_FAR
        else:
            self.speed = rng.uniform(*SNOW_SPEED_NEAR)
            self.size = rng.choice(SNOW_SIZE_NEAR)
            self.color = SNOW_COLOR_NEAR

        self.sway_amp = rng.uniform(*SNOW_SWAY_AMP)
        self.sway_speed = rng.uniform(*SNOW_SWAY_SPEED)
        self.sway_phase = rng.uniform(0, math.tau)

        self.reset(anywhere=True)

    def reset(self, anywhere=False):
        self.base_x = self.rng.uniform(0, CANVAS_W)
        self.y = self.rng.uniform(-10, GROUND_Y) if anywhere else self.rng.uniform(-10, -2)

    def current_x(self, elapsed):
        """Where the flake actually is, including the side-to-side sway."""
        sway = math.sin(elapsed * self.sway_speed + self.sway_phase) * self.sway_amp
        return (self.base_x + sway) % CANVAS_W

    def update(self, dt, elapsed, pile):
        self.y += self.speed * dt
        wind = SNOW_WIND * (0.5 if self.far else 1.0)
        self.base_x = (self.base_x + wind * dt) % CANVAS_W

        x = self.current_x(elapsed)
        surface_y = GROUND_Y - pile.height_at(x)
        if self.y + self.size >= surface_y:
            pile.add(x)
            self.reset()

    def draw(self, surface, elapsed):
        x = self.current_x(elapsed)
        surface.fill(self.color, (round(x), round(self.y), self.size, self.size))


def create_snow():
    rng = random.Random()
    return [Snowflake(rng) for _ in range(SNOW_COUNT)]


def update_snow(flakes, dt, elapsed, pile):
    for flake in flakes:
        flake.update(dt, elapsed, pile)


def draw_snow(surface, flakes, elapsed, far):
    for flake in flakes:
        if flake.far == far:
            flake.draw(surface, elapsed)