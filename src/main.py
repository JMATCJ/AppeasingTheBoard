import enum
import json
import random

import pygame
from pygame.event import Event
from pygame.locals import MOUSEBUTTONUP, MOUSEMOTION, QUIT

from consts import *
from sprites import GenericButton, Meter, MuteButton, NextRound, Prompt, TextArea, TextAreaWrapped, Title


class GameState:
    class States(enum.Enum):
        TITLE_SCREEN = enum.auto()
        INSTRUCTIONS = enum.auto()
        GAMEPLAY = enum.auto()
        GAME_OVER = enum.auto()

    def __init__(self, state: States, muted: bool):
        # Set initial values for game states
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
        self.chance_of_being_fired = self.get_fire_chance()
        self.muted = muted

        # Load the scenarios in
        with (ASSETS_DIR / "scenarios.json").open() as fp:
            self.scenarios = json.load(fp)

        # Build the initial screen
        self.all_sprites = pygame.sprite.Group()
        self.build_screen()

    def transition_state(self, new_state: States):
        self.screen_state = new_state
        self.build_screen()

    def build_screen(self):
        self.all_sprites.empty()
        if self.screen_state == GameState.States.TITLE_SCREEN:
            title = Title()
            start_game_button = GenericButton((528, 600), "play",
                                              lambda: self.transition_state(GameState.States.INSTRUCTIONS))
            mute_button = MuteButton((10, 10))

            self.all_sprites.add(title, start_game_button, mute_button)

            if not self.muted and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)  # Loop forever
        elif self.screen_state == GameState.States.INSTRUCTIONS:
            instructions_font = pygame.font.SysFont(VERDANA, 28)
            title = TextArea("Instructions", 72, center=(640, 125))
            instructions = TextAreaWrapped(pygame.Rect(280, 200, 720, 350), TITLE_SCREEN_INSTRUCTIONS,
                                           instructions_font, FONT_COLOR)
            start_game_button = GenericButton((528, 600), "play",
                                              lambda: self.transition_state(GameState.States.GAMEPLAY))

            mute_button = MuteButton((10, 10))
            self.all_sprites.add(title, instructions, start_game_button, mute_button)

            if not self.muted and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)  # Loop forever
        elif self.screen_state == GameState.States.GAMEPLAY:
            # Build meters
            cash_meter = Meter((10, 385), METER_CASH, "Company Cash", "cash.png")
            morale_meter = Meter((10, 470), METER_MORALE, "Employee Morale", "morale.png")
            productivity_meter = Meter((10, 555), METER_PROD, "Employee Productivity", "productivity.png")
            reputation_meter = Meter((10, 640), METER_REP, "Company Reputation", "reputation.png")

            # Select scenarios
            four_scenarios = random.sample(self.scenarios, 4)

            # Build Prompts
            prompt_1 = Prompt(10, 0, four_scenarios[0])
            prompt_2 = Prompt(189, 2, four_scenarios[1])
            prompt_3 = Prompt(366, 4, four_scenarios[2])
            prompt_4 = Prompt(543, 6, four_scenarios[3])

            # Build text areas
            round_text = TextArea(f"Y{self.year} Q{self.quarter}", 36, topleft=(20, 10))
            ctbf_text = TextArea(f"Chance to be fired: {sorted((0, self.chance_of_being_fired, 100))[1]:.0f}%", 24,
                                 topleft=(10, 330))

            # Build NextRound Button
            next_round = NextRound()

            # Mute button
            mute_button = MuteButton((10, 260))

            # Add all sprites to the main group
            self.all_sprites.add(cash_meter, morale_meter, productivity_meter, reputation_meter,
                                 prompt_1, prompt_2, prompt_3, prompt_4,
                                 round_text, ctbf_text, next_round, mute_button)

            # Play the music
            if not self.muted and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)  # Loop forever
        elif self.screen_state == GameState.States.GAME_OVER:
            prompt_1 = TextArea("Game Over", 72, center=(640, 210))

            text_font = pygame.font.SysFont(VERDANA, 28)
            description = TextAreaWrapped(pygame.Rect(280, 275, 720, 150), GAME_OVER_FLAVORTEXT,
                                          text_font, FONT_COLOR, centered=True)

            play_again = GenericButton((350, 450), "playagain", lambda: pygame.event.post(Event(NEWGAME)))
            exit_btn = GenericButton((700, 450), "exit", lambda: pygame.event.post(Event(QUIT)))

            self.all_sprites.add(prompt_1, description, play_again, exit_btn)

            pygame.mixer.music.pause()
            pygame.mixer.music.rewind()

    def transition_round(self):
        # Update the meters and reset the deltas
        for meter in self.meters:
            self.meters[meter] = min(self.meters[meter] + self.meters_delta[meter], 100)
            self.meters_delta[meter] = 0

        self.chance_of_being_fired = self.get_fire_chance()  # Recalculate the chance to be fired
        self.button_states = [False] * 8  # Reset all the button states
        # Move to the next quarter
        self.quarter += 1
        if self.quarter >= 5:
            # Roll the dice!
            if random.random() < self.chance_of_being_fired / 100 and self.year != 1:
                self.screen_state = GameState.States.GAME_OVER
            self.quarter = 1
            self.year += 1
        # Setup the next screen, whichever one that might be
        self.build_screen()

    def get_fire_chance(self) -> float:
        result = 0
        for meter in self.meters:
            if self.meters[meter] < METER_CUTOFFS[meter]:
                result += (METER_CUTOFFS[meter] - self.meters[meter]) * FIRE_STEPS[meter]
            else:
                result -= (self.meters[meter] - METER_CUTOFFS[meter]) * (FIRE_STEPS[meter] / 2)
        return result

    def ready_for_next_round(self) -> bool:
        return self.button_states.count(True) == 4

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def draw(self, screen):
        for sprite in self.all_sprites:
            sprite.draw(screen, self)


# Init pygame and the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(ASSETS_DIR / "icon.png")
pygame.display.set_icon(icon)

# Setup background music
pygame.mixer.music.load(ASSETS_DIR / "sounds" / "background.ogg")
pygame.mixer.music.set_volume(0.20)

# Make the game
game = GameState(GameState.States.TITLE_SCREEN, False)

# Setup the clock that will be used to cap the framerate
clock = pygame.time.Clock()

running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == NEWGAME:
            game = GameState(GameState.States.GAMEPLAY, game.muted)
        elif event.type == MOUSEBUTTONUP and event.button == MOUSE_LEFT_CLICK:
            clicked_sprites = [s for s in game.all_sprites if s.rect.collidepoint(event.pos)]
            for sprite in clicked_sprites:
                if hasattr(sprite, "handle_click"):
                    sprite.handle_click(game, event.pos)
        elif event.type == MOUSEMOTION:
            for sprite in game.all_sprites:
                if hasattr(sprite, "hovered"):
                    sprite.hovered = sprite.rect.collidepoint(event.pos)
                elif hasattr(sprite, "handle_hover"):
                    sprite.handle_hover(event.pos)

    # Drawing
    bg_surf = pygame.image.load(ASSETS_DIR / "background.png").convert()
    screen.blit(bg_surf, bg_surf.get_rect())
    game.draw(screen)      # Draw...everything
    pygame.display.flip()  # Show the frame

    # Wait until next frame
    clock.tick(60)  # Lock at 60 FPS
