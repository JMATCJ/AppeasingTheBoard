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
        # print(f"{meter_text}: w: {self.text.get_width()}, h: {self.text.get_height()}")
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
        FONT = pygame.font.SysFont("verdana", 30)
        # Unselected prompt button
        self.unselected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_up.png").convert()

        # Hovered prompt button
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_hover.png").convert()

        # Selected prompt button
        self.selected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_select.png").convert()

        # Prompt position
        self.rect = self.unselected_surf.get_rect(topleft=prompt_pos)

        # Prompt text attached to buttons
        self.text = FONT.render(prompt_text, True, (51, 51, 51))

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
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))

    def handle_click(self):
        self.selected = not self.selected


class Round(pygame.sprite.Sprite):
    def __init__(self, year, quarter):
        super().__init__()
        self.year = year
        self.quarter = quarter

        # Rendering round text
        self.round_ind = ROUND_FONT.render(f"{self.year} Q{self.quarter}", True, FONT_COLOR)  # (111, 38, 166)

        # Round text position
        self.rect = self.round_ind.get_rect(topleft=(20, 10))

    def draw(self, screen):
        screen.blit(self.round_ind, self.rect)

    def handle_click(self):
        self.quarter += 1
        if self.quarter >= 5:
            self.quarter = 1
            self.year += 1
        self.round_ind = ROUND_FONT.render(f"{self.year} Q{self.quarter}", True, FONT_COLOR)  # (111, 38, 166)
        for prompt in prompts:
            prompt.selected = False


class NextRound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Next round buttons
        self.unhovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_up.png").convert()
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_hover.png").convert()

        # Next round position
        self.rect = self.unhovered_surf.get_rect(topright=(1270, 10))

        # Whether or not the player is hovering over the button
        self.hovered = False

    def draw(self, screen):
        if self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unhovered_surf, self.rect)

    def handle_click(self):
        round.handle_click()


# Main
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MOUSE_LEFT_CLICK = 1
FONT_COLOR = (222, 222, 222)
ROUND_FONT = pygame.font.SysFont("comic sans ms", 36)


# Instantiate the Meter
company_cash_meter = Meter((10, 385), "Company Cash", "cash.png")
employee_morale_meter = Meter((10, 470), "Employee Morale", "morale.png")
employee_productivity_meter = Meter((10, 555), "Employee Productivity", "productivity.png")
company_reputation_meter = Meter((10, 640), "Company Reputation", "reputation.png")

# Prompts
prompt_1 = Prompt((408, 169), "one")
prompt_2 = Prompt((702, 169), "two")
prompt_3 = Prompt((996, 169), "three")
prompt_4 = Prompt((408, 356), "four")
prompt_5 = Prompt((702, 356), "five")
prompt_6 = Prompt((996, 356), "six")
prompt_7 = Prompt((408, 543), "seven")
prompt_8 = Prompt((702, 543), "eight")
prompt_9 = Prompt((996, 543), "nine")

# Round indicator
round = Round(2022, 1)

# Next Round
next_round = NextRound()

# Create meter group
meters = pygame.sprite.Group()
meters.add(company_cash_meter, employee_morale_meter, employee_productivity_meter, company_reputation_meter)
# Buttons group
buttons = pygame.sprite.Group()
buttons.add(prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6, prompt_7, prompt_8, prompt_9, next_round)

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
            clicked_sprite = next((s for s in buttons if s.rect.collidepoint(event.pos)), None)
            if clicked_sprite is not None:
                clicked_sprite.handle_click()
        elif event.type == MOUSEMOTION:
            for button in buttons:
                button.hovered = button.rect.collidepoint(event.pos)
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
    for button in buttons:
        button.draw(screen)

    # # Draw round indicator to screen
    round.draw(screen)

    pygame.display.flip()

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
