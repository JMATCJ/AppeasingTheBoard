import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.locals import QUIT

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_color: Tuple[int, int, int]):
        super().__init__()
        self.surf = pygame.Surface((300, 25))
        self.surf.fill(meter_color)
        self.rect = self.surf.get_rect(topleft=meter_pos)


# Main
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate the Meter
company_cash_meter = Meter((0, 0), (60, 182, 252))
employee_morale_meter = Meter((0, 50), (98, 242, 72))
employee_productivity_meter = Meter((0, 100), (239, 62, 62))
company_reputation_meter = Meter((0, 150), (240, 247, 46))

# Create meter group
meters = pygame.sprite.Group()
meters.add(company_cash_meter, employee_morale_meter, employee_productivity_meter, company_reputation_meter)

running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Updating
    # TODO

    # Drawing
    # Draw everything gray
    screen.fill((100, 100, 100))
    # Draw ("blit") the meters to the screen, position it with the rect
    for meter in meters:
        screen.blit(meter.surf, meter.rect)

    pygame.display.flip()
