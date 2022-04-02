import random
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


def randcolor() -> Tuple[int, int, int]:
    """A very integral part of the gameplay :)"""
    return random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_color: Tuple[int, int, int]):
        super().__init__()
        self.surf = pygame.Surface((300, 25))
        self.surf.fill(meter_color)
        self.rect = self.surf.get_rect(topleft=meter_pos)

# 1280 x 720 | 9 prompts
# 400px wide
# Leave 50px at the top for the meters? Leaves 670px
# Leave 100px after that for status next and next round button? Leaves 570px


class Prompt(pygame.sprite.Sprite):
    def __init__(self, prompt_pos: Tuple[int, int]):
        super().__init__()
        self.surf = pygame.Surface((400, 180))
        self.surf.fill(randcolor())  # (184, 127, 59)
        self.rect = self.surf.get_rect(topleft=prompt_pos)


class NextRound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((150, 50))
        self.surf.fill(randcolor())  # (255, 0, 212)
        self.rect = self.surf.get_rect(topright=(1270, 60))


# Main
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("comic sans ms", 36)
img = font.render('Y1, Q1', True, randcolor())  # (111, 38, 166) # TODO: move this to "Drawing"

# Instantiate the Meter
company_cash_meter = Meter((10, 10), randcolor())  # (60, 182, 252)
employee_morale_meter = Meter((330, 10), randcolor())  # (98, 242, 72)
employee_productivity_meter = Meter((650, 10), randcolor())  # (239, 62, 62)
company_reputation_meter = Meter((970, 10), randcolor())  # (240, 247, 46)
# Prompts
prompt_1 = Prompt((10, 130))
prompt_2 = Prompt((430, 130))
prompt_3 = Prompt((850, 130))
prompt_4 = Prompt((10, 330))
prompt_5 = Prompt((430, 330))
prompt_6 = Prompt((850, 330))
prompt_7 = Prompt((10, 530))
prompt_8 = Prompt((430, 530))
prompt_9 = Prompt((850, 530))
# Next Round
next_round = NextRound()

# Create meter group
meters = pygame.sprite.Group()
meters.add(company_cash_meter, employee_morale_meter, employee_productivity_meter, company_reputation_meter)
# Prompts group
prompts = pygame.sprite.Group()
prompts.add(prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6, prompt_7, prompt_8, prompt_9)

# Setup the clock that will be used to cap the framerate
clock = pygame.time.Clock()

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
    # Draw ("blit") the meters to the screen, position them with their rect
    for meter in meters:
        screen.blit(meter.surf, meter.rect)
    screen.blit(img, (20, 50))  # Text
    for prompt in prompts:
        screen.blit(prompt.surf, prompt.rect)
    screen.blit(next_round.surf, next_round.rect)

    pygame.display.flip()

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
