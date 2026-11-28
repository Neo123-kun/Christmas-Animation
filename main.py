import pygame
from settings import *
from tree import draw_ground, draw_tree
from star import draw_star
from lights import create_lights, draw_lights
from snow import create_snow, update_snow, draw_snow
from pile import SnowPile
from shake import ShakeDetector

# Main
def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Feel the christmas spirit!")
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    clock = pygame.time.Clock()

    # Lights and Snow
    lights = create_lights()
    flakes = create_snow()
    pile = SnowPile()
    shaker = ShakeDetector()
    elapsed = 0.0

    # While running
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        
        # Event Close Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pile.clear()
            elif event.type == pygame.WINDOWMOVED:
                if shaker.on_moved(event.x, event.y):
                    pile.clear()
        # Update
        elapsed += dt
        update_snow(flakes, dt, elapsed, pile)

        # Draw Order
        canvas.fill(SKY_COLOR)
        draw_ground(canvas)
        draw_snow(canvas, flakes, elapsed, far=True)
        draw_tree(canvas)
        pile.draw(canvas)                                # covers the trunk base
        draw_lights(canvas, lights, elapsed)
        draw_star(canvas, elapsed)
        draw_snow(canvas, flakes, elapsed, far=False)

        #Scale up
        pygame.transform.scale(canvas, (WINDOW_W, WINDOW_H), window)
        pygame.display.flip()
    
    pygame.quit()

main()