import time
from settings import *


class ShakeDetector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_pos = None
        self.last_dir = [0, 0]
        self.travel = [0, 0]
        self.reversals = 0
        self.last_time = 0.0

    def on_moved(self, x, y):
        """Call with the window's new position. Returns True when a shake is detected."""
        now = time.time()
        if now - self.last_time > SHAKE_TIMEOUT:
            self.reversals = 0
        self.last_time = now

        if self.last_pos is None:
            self.last_pos = (x, y)
            return False

        for axis, new in enumerate((x, y)):
            delta = new - self.last_pos[axis]
            if delta == 0:
                continue
            direction = 1 if delta > 0 else -1

            if direction != self.last_dir[axis]:
                if self.last_dir[axis] != 0 and self.travel[axis] >= SHAKE_MIN_TRAVEL:
                    self.reversals += 1
                self.travel[axis] = 0
                self.last_dir[axis] = direction

            self.travel[axis] += abs(delta)

        self.last_pos = (x, y)

        if self.reversals >= SHAKE_REVERSALS:
            self.reset()
            return True
        return False