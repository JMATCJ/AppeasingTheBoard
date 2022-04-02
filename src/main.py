import random
import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEMOTION, K_UP, K_DOWN, KEYDOWN

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")


def randcolor() -> Tuple[int, int, int]:
    """A very integral part of the gameplay :)"""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_text: str, meter_image: str):
        super().__init__()
        FONT = pygame.font.SysFont("verdana", 24)
        # Background meter surface
        self.bg_surf = pygame.image.load(ASSETS_DIR / "meters" / "background.png").convert()

        # Foreground meter surface
        self.fg_surf = pygame.image.load(ASSETS_DIR / "meters" / meter_image).convert()

        # Meter position
        self.bg_rect = self.bg_surf.get_rect(topleft=meter_pos)
        self.fg_rect = self.fg_surf.get_rect(topleft=meter_pos)
    
        # Meter text
        self.text = FONT.render(meter_text, True, FONT_COLOR)
        print(f"{meter_text}: w: {self.text.get_width()}, h: {self.text.get_height()}")
        self.text_rect = self.text.get_rect(topleft=(meter_pos[0], meter_pos[1] + self.bg_rect.h))

        # Value
        self.value = 50  # [0-100], TODO: this should probably be a parameter eventually?

    def draw(self, screen):
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.fg_surf, self.fg_rect, self.fg_surf.get_rect(w=self.fg_surf.get_width() * (self.value / 100)))
        screen.blit(self.text, self.text_rect)

    def handle_click(self):
        pass

# 1280 x 720 | 9 prompts
# 400px wide
# Leave 50px at the top for the meters? Leaves 670px
# Leave 100px after that for status next and next round button? Leaves 570px


class Prompt(pygame.sprite.Sprite):
    def __init__(self, prompt_pos: Tuple[int, int], prompt_text: str):
        super().__init__()
        FONT = pygame.font.SysFont("verdana", 36)
        # Unselected prompt button
        self.unselected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_up.png").convert()

        # Hovered prompt button
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_hover.png").convert()

        # Selected prompt button
        self.selected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_select.png").convert()

        # Prompt position
        self.rect = self.unselected_surf.get_rect(topleft=prompt_pos)
        
        # Prompt text attached to buttons
        # self.text = FONT.render(prompt_text, True, FONT_COLOR)
        # self.surf.blit(self.text, self.text.get_rect(center=(200, 90)))
        # self.selected_surf.blit(self.text, self.text.get_rect(center=(200, 90)))

        # Whether prompt is selected or not
        self.hovered = False
        self.selected = False

    def draw(self, screen):
        if self.selected:
            screen.blit(self.selected_surf, self.rect)
        elif self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unselected_surf, self.rect)

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
FONT_COLOR = (222, 222, 222)

# Instantiate the Meter
company_cash_meter = Meter((10, 385), "Company Cash", "cash.png")
employee_morale_meter = Meter((10, 470), "Employee Morale", "morale.png")
employee_productivity_meter = Meter((10, 555), "Employee Productivity", "productivity.png")
company_reputation_meter = Meter((10, 640), "Company Reputation", "reputation.png")

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
        elif event.type == MOUSEBUTTONUP and event.button == MOUSE_LEFT_CLICK:
            clicked_sprite = next((s for s in prompts if s.rect.collidepoint(event.pos)), None)
            if clicked_sprite is not None:
                clicked_sprite.handle_click()
        elif event.type == MOUSEMOTION:
            for prompt in prompts:
                prompt.hovered = prompt.rect.collidepoint(event.pos)
        elif event.type == KEYDOWN:   # TEMP TESTING CODE
            if event.key == K_UP:
                for meter in meters:
                    meter.value += 10
            if event.key == K_DOWN:
                for meter in meters:
                    meter.value -= 10

    # Updating
    # TODO

    # Drawing
    # Draw everything gray
    screen.fill((100, 100, 100))

    # Draw ("blit") the meters to the screen, position them with their rect
    for meter in meters:
        meter.draw(screen)

    # Draw prompt buttons to screen
    # for prompt in prompts:
    #     prompt.draw(screen)

    # # Draw round indicator to screen
    # round.draw(screen)
    #
    # # Draw next round button to screen
    # next_round.draw(screen)

    pygame.display.flip()

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
