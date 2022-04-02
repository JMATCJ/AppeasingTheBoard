import pygame
import sys
from pathlib import Path
from pygame.locals import QUIT

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")


# Main
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Updating
    # TODO

    # Drawing
    # Draw everything white
    screen.fill((255, 255, 255))
    # Create a small black square
    surf = pygame.Surface((50, 50))
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    rect.top = 100
    rect.left = 100
    # Draw ("blit") the surface to the screen, position it with the rect
    screen.blit(surf, rect)
    pygame.display.flip()
