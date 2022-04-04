import enum
import json
import random

import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEMOTION, QUIT

from consts import *
from sprites import ButtonGroup, GameOverButton, Meter, NextRound, TextArea, TextAreaWrapped


class GameState:
    class States(enum.Enum):
        TITLE_SCREEN = enum.auto()
        GAMEPLAY = enum.auto()
        GAME_OVER = enum.auto()

    def __init__(self, state: States):
        self.year = 1
        self.quarter = 1
        self.meters = {
            METER_CASH: 50,
            METER_MORALE: 50,
            METER_PROD: 50,
            METER_REP: 50
        }
        self.meters_delta = {
            METER_CASH: 0,
            METER_MORALE: 0,
            METER_PROD: 0,
            METER_REP: 0
        }
        self.button_states = [False] * 8
        self.screen_state = state
        self.all_sprites = pygame.sprite.Group()
        self.chance_of_being_fired = 0
        self.calc_fire_chance()

        with (ASSETS_DIR / "scenarios.json").open() as fp:
            self.scenarios = json.load(fp)

    def build_screen(self):
        self.all_sprites.empty()
        if self.screen_state == GameState.States.TITLE_SCREEN:
            title = TextArea((270, 125), "Box Explorer 2: Home", 72)
            title_font = pygame.font.SysFont("verdana", 28)
            instructions = TextAreaWrapped(pygame.Rect(340, 225, 600, 200), TITLE_SCREEN_INSTRUCTIONS, title_font, FONT_COLOR)
            start_game_button = GameOverButton((528, 450), "playagain", playgame)
            self.all_sprites.add(title, instructions, start_game_button)
        elif self.screen_state == GameState.States.GAMEPLAY:
            # Build meters
            company_cash_meter = Meter((10, 385), METER_CASH, "Company Cash", "cash.png")
            employee_morale_meter = Meter((10, 470), METER_MORALE, "Employee Morale", "morale.png")
            employee_productivity_meter = Meter((10, 555), METER_PROD, "Employee Productivity", "productivity.png")
            company_reputation_meter = Meter((10, 640), METER_REP, "Company Reputation", "reputation.png")

            four_scenarios = random.sample(self.scenarios, 4)

            # Build ButtonGroups
            button_group_1 = ButtonGroup((712, 10), 0, four_scenarios[0])
            button_group_2 = ButtonGroup((712, 189), 2, four_scenarios[1])
            button_group_3 = ButtonGroup((712, 366), 4, four_scenarios[2])
            button_group_4 = ButtonGroup((712, 543), 6, four_scenarios[3])

            # Build TextAreas
            round_text = TextArea((20, 10), f"Y{self.year} Q{self.quarter}", 36)
            prompt_font = pygame.font.SysFont("verdana", 20)
            prompt_1 = TextAreaWrapped(pygame.Rect(380, 10, 300, button_group_1.rect.h), four_scenarios[0][SCENARIO_TEXT], prompt_font, FONT_COLOR)
            prompt_2 = TextAreaWrapped(pygame.Rect(380, 189, 300, button_group_2.rect.h), four_scenarios[1][SCENARIO_TEXT], prompt_font, FONT_COLOR)
            prompt_3 = TextAreaWrapped(pygame.Rect(380, 366, 300, button_group_3.rect.h), four_scenarios[2][SCENARIO_TEXT], prompt_font, FONT_COLOR)
            prompt_4 = TextAreaWrapped(pygame.Rect(380, 543, 300, button_group_4.rect.h), four_scenarios[3][SCENARIO_TEXT], prompt_font, FONT_COLOR)

            # Chance to be fired text
            ctbf_text = TextArea((10, 300), f"Chance to be fired: {min(self.chance_of_being_fired, 100):.2f}%", 24)

            # Build NextRound
            next_round = NextRound()

            # Add all sprites to the main group
            self.all_sprites.add(company_cash_meter, employee_morale_meter, employee_productivity_meter,
                                 company_reputation_meter, button_group_1, button_group_2, button_group_3,
                                 button_group_4, round_text, prompt_1, prompt_2, prompt_3, prompt_4, ctbf_text, next_round)

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)  # Loop forever
        elif self.screen_state == GameState.States.GAME_OVER:
            prompt_1 = TextArea((456, 210), "Game Over", 72)

            play_again = GameOverButton((350, 400), "playagain", reset)
            exit_btn = GameOverButton((700, 400), "exit", game_exit)

            self.all_sprites.add(prompt_1, play_again, exit_btn)

            pygame.mixer.music.stop()

    def transition_round(self):
        if self.ready_for_next_round():
            # Update the meters and reset the deltas
            for meter in self.meters:
                # Clamp function: sorts the values, gets the one in the middle.
                self.meters[meter] = min(self.meters[meter] + self.meters_delta[meter], 100)
                self.meters_delta[meter] = 0
            # Reset all the button states
            self.button_states = [False] * 8
            # Move to the next quarter
            self.quarter += 1
            self.calc_fire_chance()
            if self.quarter >= 5:
                if random.random() < self.chance_of_being_fired / 100:
                    self.screen_state = GameState.States.GAME_OVER

                self.quarter = 1
                self.year += 1

            # Setup the next screen
            self.build_screen()

    def calc_fire_chance(self):
        self.chance_of_being_fired = 0
        for meter in self.meters:
            if self.meters[meter] < METER_CUTOFFS[meter]:
                self.chance_of_being_fired += (METER_CUTOFFS[meter] - self.meters[meter]) * FIRE_STEPS[meter]

    def ready_for_next_round(self) -> bool:
        return self.button_states.count(True) == 4

    def draw(self, screen):
        for sprite in self.all_sprites:
            sprite.draw(screen, self)


def reset():
    global game
    game = GameState(GameState.States.GAMEPLAY)
    game.build_screen()


def game_exit():
    global running
    running = False

def playgame():
    global game
    game.screen_state = GameState.States.GAMEPLAY
    game.build_screen()


# Init pygame and the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup background music
pygame.mixer.music.load(ASSETS_DIR / "sounds" / "background.ogg")
pygame.mixer.music.set_volume(0.20)

# Make the game
game = GameState(GameState.States.TITLE_SCREEN)
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
