import pygame
from typing import Tuple

from consts import *


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_type: str, meter_text: str, meter_image: str):
        super().__init__()
        font = pygame.font.SysFont("verdana", 24)
        # Background meter surface
        self.bg_surf = pygame.image.load(ASSETS_DIR / "meters" / "background.png").convert()

        # Foreground meter surface
        self.fg_surf = pygame.image.load(ASSETS_DIR / "meters" / meter_image).convert()

        # Meter position
        self.rect = self.bg_surf.get_rect(topleft=meter_pos)
        self.fg_rect = self.fg_surf.get_rect(topleft=meter_pos)

        # Meter text
        self.text = font.render(meter_text, True, FONT_COLOR)
        self.text_rect = self.text.get_rect(topleft=(meter_pos[0], meter_pos[1] + self.rect.h))

        # Meter type
        self.type = meter_type

    def draw(self, screen, gamestate):
        screen.blit(self.bg_surf, self.rect)
        screen.blit(self.fg_surf, self.fg_rect, self.fg_surf.get_rect(
            w=self.fg_surf.get_width() * (gamestate.meters[self.type] / 100)
        ))
        screen.blit(self.text, self.text_rect)

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, prompt_pos: Tuple[int, int], id: int, prompt_text: str):
        super().__init__()
        font = pygame.font.SysFont("verdana", 30)
        self.id = id
        # Unselected prompt button
        self.unselected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_up.png").convert()

        # Hovered prompt button
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_hover.png").convert()

        # Selected prompt button
        self.selected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_select.png").convert()

        # Prompt position
        self.rect = self.unselected_surf.get_rect(topleft=prompt_pos)

        # Prompt text attached to buttons
        self.text = font.render(prompt_text, True, (51, 51, 51))

        # Whether prompt is selected or not
        self.hovered = False

    def draw(self, screen, gamestate):
        if gamestate.button_states[self.id]:
            screen.blit(self.selected_surf, self.rect)
        elif self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unselected_surf, self.rect)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        pass


class ButtonGroup(pygame.sprite.Sprite):
    def __init__(self, group_pos: Tuple[int, int], left_button_id: int, left_text: str, right_text: str):
        super().__init__()
        self.left_button = Button(group_pos, left_button_id, left_text)
        # TODO: Make this 294 not a magic number
        self.right_button = Button((group_pos[0] + 294, group_pos[1]), left_button_id + 1, right_text)

        self.rect = pygame.Rect(group_pos, (self.left_button.rect.width + self.right_button.rect.width + 20,
                                            self.left_button.rect.height))

    def draw(self, screen, gamestate):
        self.left_button.draw(screen, gamestate)
        self.right_button.draw(screen, gamestate)

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        if self.left_button.rect.collidepoint(pos):
            gamestate.button_states[self.left_button.id] = True
            gamestate.button_states[self.right_button.id] = False
        elif self.right_button.rect.collidepoint(pos):
            gamestate.button_states[self.right_button.id] = True
            gamestate.button_states[self.left_button.id] = False

    def handle_hover(self, pos: Tuple[int, int]):
        self.left_button.hovered = self.left_button.rect.collidepoint(pos)
        self.right_button.hovered = self.right_button.rect.collidepoint(pos)


class NextRound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Next round buttons
        self.unhovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_up.png").convert()
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_hover.png").convert()

        # Next round position
        self.rect = self.unhovered_surf.get_rect(topleft=(10, 75))

        # Whether or not the player is hovering over the button
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, _):
        if self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unhovered_surf, self.rect)

    def handle_click(self, gamestate, _: Tuple[int, int]):
        gamestate.transition_round()


class TextArea(pygame.sprite.Sprite):
    def __init__(self, position, value):
        super().__init__()
        font = pygame.font.SysFont("comic sans ms", 36)
        self.text = font.render(value, True, FONT_COLOR)
        self.rect = self.text.get_rect(topleft=position)

    def draw(self, screen, _):
        screen.blit(self.text, self.rect)

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        pass
