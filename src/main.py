import random
import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")


def randcolor() -> Tuple[int, int, int]:
    """A very integral part of the gameplay :)"""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_text: str,  meter_color: Tuple[int, int, int]):
        super().__init__()
        FONT = pygame.font.SysFont("comic sans ms", 24)
        # Background meter surface
        self.bg_surf = pygame.Surface((300, 25))
        self.bg_surf.fill(meter_color)

        # Foreground meter surface
        self.fg_surf = pygame.Surface((300, 25))
        self.fg_surf.fill(randcolor())

        # Meter position
        self.rect = self.bg_surf.get_rect(topleft=meter_pos)
    
        # Meter text
        self.text = FONT.render(meter_text, True, randcolor())
        self.bg_surf.blit(self.text, self.text.get_rect(center=(150, 12)))
        self.fg_surf.blit(self.text, self.text.get_rect(center=(150, 12)))

    def draw(self, screen):
        screen.blit(self.bg_surf, self.rect)
        screen.blit(self.fg_surf, self.rect)

    def handle_click(self):
        pass

# 1280 x 720 | 9 prompts
# 400px wide
# Leave 50px at the top for the meters? Leaves 670px
# Leave 100px after that for status next and next round button? Leaves 570px


class Prompt(pygame.sprite.Sprite):
    def __init__(self, prompt_pos: Tuple[int, int], prompt_text: str):
        super().__init__()
        FONT = pygame.font.SysFont("comic sans ms", 36)
        # Unselected prompt button
        self.surf = pygame.Surface((400, 180))
        self.surf.fill(randcolor())  # (184, 127, 59)
        
        # Selected prompt button (different color to show selected)
        self.selected_surf = pygame.Surface((400, 180))
        self.selected_surf.fill(randcolor())

        # Prompt position
        self.rect = self.surf.get_rect(topleft=prompt_pos)
        
        # Prompt text attached to buttons
        self.text = FONT.render(prompt_text, True, randcolor())
        self.surf.blit(self.text, self.text.get_rect(center=(200, 90)))
        self.selected_surf.blit(self.text, self.text.get_rect(center=(200, 90)))

        # Whether prompt is selected or not
        self.selected = False


    def draw(self, screen):
        if self.selected:
            screen.blit(self.selected_surf, self.rect)
        else:
            screen.blit(self.surf, self.rect)


    def handle_click(self):
        self.selected = not self.selected


class Round(pygame.sprite.Sprite):
    def __init__(self, round_text: str):
        super().__init__()
        FONT = pygame.font.SysFont("comic sans ms", 36)
        # Rendering round text
        self.round_ind = FONT.render(round_text, True, randcolor())  # (111, 38, 166)
        
        # Round text position
        self.rect = self.round_ind.get_rect(topleft=(20, 50))

    def draw(self, screen):
        screen.blit(self.round_ind, self.rect)

    def handle_click(self):
        pass


class NextRound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        FONT = pygame.font.SysFont("comic sans ms", 24)
        # Next round button
        self.surf = pygame.Surface((150, 50))
        self.surf.fill(randcolor())  # (255, 0, 212)

        # Next round position
        self.rect = self.surf.get_rect(topright=(1270, 60))

        # Next round text attached to button
        self.text = FONT.render("Next Round", True, randcolor())
        self.surf.blit(self.text, self.text.get_rect(center=(75, 25)))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def handle_click(self):
        pass


# Main
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MOUSE_LEFT_CLICK = 1

# Instantiate the Meter
company_cash_meter = Meter((10, 10), "Company Cash", randcolor())  # (60, 182, 252)
employee_morale_meter = Meter((330, 10), "Employee Morale", randcolor())  # (98, 242, 72)
employee_productivity_meter = Meter((650, 10), "Employee Productivity", randcolor())  # (239, 62, 62)
company_reputation_meter = Meter((970, 10), "Company Reputation", randcolor())  # (240, 247, 46)

# Prompts
prompt_1 = Prompt((10, 130), "one")
prompt_2 = Prompt((430, 130), "two")
prompt_3 = Prompt((850, 130), "three")
prompt_4 = Prompt((10, 330), "four")
prompt_5 = Prompt((430, 330), "five")
prompt_6 = Prompt((850, 330), "six")
prompt_7 = Prompt((10, 530), "seven")
prompt_8 = Prompt((430, 530), "eight")
prompt_9 = Prompt((850, 530), "nine")

# Round indicator
round = Round("Y1, Q1")

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
        if event.type == MOUSEBUTTONUP and event.button == MOUSE_LEFT_CLICK:
            clicked_sprite = next((s for s in prompts if s.rect.collidepoint(event.pos)), None)
            if clicked_sprite is not None:
                clicked_sprite.handle_click()
    # Updating
    # TODO

    # Drawing
    # Draw everything gray
    screen.fill((100, 100, 100))

    # Draw ("blit") the meters to the screen, position them with their rect
    for meter in meters:
        meter.draw(screen)

    # Draw prompt buttons to screen
    for prompt in prompts:
        prompt.draw(screen)

    # Draw round indicator to screen
    round.draw(screen)  
    
    # Draw next round button to screen
    next_round.draw(screen)

    pygame.display.flip()

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
