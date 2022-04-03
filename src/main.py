import enum
import random
from typing import Tuple

import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEMOTION
from sprites import ButtonGroup, Meter, NextRound, TextArea
from consts import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def randcolor() -> Tuple[int, int, int]:
    """A very integral part of the gameplay :)"""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class GameState:
    class States(enum.Enum):
        COMMON = enum.auto()
        RAND_EVENT = enum.auto()
        GAME_OVER = enum.auto()

    def __init__(self):
        self.year = 1
        self.quarter = 1
        self.meters = {  # TODO: Different starting values based on difficulty
            METER_CASH: 50,
            METER_MORALE: 50,
            METER_PROD: 50,
            METER_REP: 50
        }
        self.button_states = [False] * 8
        self.screen_state = GameState.States.COMMON
        self.all_sprites = pygame.sprite.Group()

    def build_screen(self):
        self.all_sprites.empty()
        if self.screen_state == GameState.States.COMMON:
            # Build meters
            company_cash_meter = Meter((10, 385), METER_CASH, "Company Cash", "cash.png")
            employee_morale_meter = Meter((10, 470), METER_MORALE, "Employee Morale", "morale.png")
            employee_productivity_meter = Meter((10, 555), METER_PROD, "Employee Productivity", "productivity.png")
            company_reputation_meter = Meter((10, 640), METER_REP, "Company Reputation", "reputation.png")

            # Build ButtonGroups
            button_group_1 = ButtonGroup((702, 10), 0, "one", "two")
            button_group_2 = ButtonGroup((702, 169), 2, "three", "four")
            button_group_3 = ButtonGroup((702, 356), 4, "five", "six")
            button_group_4 = ButtonGroup((702, 543), 6, "seven", "eight")

            # Build TextAreas
            round_text = TextArea((20, 10), f"Y{self.year} Q{self.quarter}")
            prompt_1 = TextArea((408, 10), "test")
            prompt_2 = TextArea((408, 169), "test")
            prompt_3 = TextArea((408, 365), "test")
            prompt_4 = TextArea((408, 543), "test")

            # Build NextRound
            next_round = NextRound()

            # Add all sprites to the main group
            self.all_sprites.add(company_cash_meter, employee_morale_meter, employee_productivity_meter,
                                 company_reputation_meter, button_group_1, button_group_2, button_group_3,
                                 button_group_4, round_text, prompt_1, prompt_2, prompt_3, prompt_4, next_round)
        elif self.screen_state == GameState.States.RAND_EVENT:
            pass  # TODO
        elif self.screen_state == GameState.States.GAME_OVER:
            pass  # TODO

    def transition_round(self):
        # TODO: Actually change the meters here
        self.button_states = [False] * 8
        self.quarter += 1
        if self.quarter >= 5:
            self.quarter = 1
            self.year += 1
        # TODO: Determine if we change screen state here
        self.build_screen()

    def draw(self, screen):
        for sprite in self.all_sprites:
            sprite.draw(screen, self)


# Make the game
game = GameState()
game.build_screen()

# Setup the clock that will be used to cap the framerate
clock = pygame.time.Clock()

running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONUP and event.button == MOUSE_LEFT_CLICK:
            clicked_sprite = next((s for s in game.all_sprites if s.rect.collidepoint(event.pos)), None)
            if clicked_sprite is not None and hasattr(clicked_sprite, "handle_click"):
                clicked_sprite.handle_click(game, event.pos)
        elif event.type == MOUSEMOTION:
            for sprite in game.all_sprites:
                if hasattr(sprite, "hovered"):
                    sprite.hovered = sprite.rect.collidepoint(event.pos)
                elif hasattr(sprite, "handle_hover"):
                    sprite.handle_hover(event.pos)

    # Drawing
    # Draw everything gray
    screen.fill((100, 100, 100))

    # Draw...everything
    game.draw(screen)

    # Show the frame
    pygame.display.flip()

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
