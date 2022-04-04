import pygame
from typing import Dict, Tuple, Union

from consts import *


class Meter(pygame.sprite.Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_type: str, meter_text: str, meter_image: str):
        super().__init__()
        self.font = pygame.font.SysFont("verdana", 24)
        # Background meter surface
        self.bg_surf = pygame.image.load(ASSETS_DIR / "meters" / "background.png").convert()

        # Foreground meter surface
        self.fg_surf = pygame.image.load(ASSETS_DIR / "meters" / meter_image).convert()

        # Meter position
        self.rect = self.bg_surf.get_rect(topleft=meter_pos)
        self.fg_rect = self.fg_surf.get_rect(topleft=meter_pos)

        # Meter title
        self.text = self.font.render(meter_text, True, FONT_COLOR)
        self.text_rect = self.text.get_rect(topleft=(meter_pos[0], meter_pos[1] + self.rect.h))

        # Meter type
        self.type = meter_type

    def draw(self, screen, gamestate):
        screen.blit(self.bg_surf, self.rect)
        screen.blit(self.fg_surf, self.fg_rect, self.fg_surf.get_rect(
            w=self.fg_surf.get_width() * (gamestate.meters[self.type] / 100)
        ))
        screen.blit(self.text, self.text_rect)
        meter_text = f"{gamestate.meters[self.type]} / 100"
        if gamestate.meters_delta[self.type] > 0:
            meter_text += f" (+{gamestate.meters_delta[self.type]})"
        elif gamestate.meters_delta[self.type] < 0:
            meter_text += f" ({gamestate.meters_delta[self.type]})"
        meter_text_surf = self.font.render(meter_text, True, FONT_COLOR)
        screen.blit(meter_text_surf, meter_text_surf.get_rect(center=self.rect.center))


class Button(pygame.sprite.Sprite):
    def __init__(self, button_pos: Tuple[int, int], id: int, scenario_text: str, scenario_res: Dict[str, int]):
        super().__init__()
        font = pygame.font.SysFont("verdana", 16)
        self.id = id
        # The surfaces for the three button states
        self.unselected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_up.png").convert()
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_hover.png").convert()
        self.selected_surf = pygame.image.load(ASSETS_DIR / "buttons" / "prompt_select.png").convert()

        # Position of button (same for all three states)
        self.rect = self.unselected_surf.get_rect(topleft=button_pos)

        # Prompt text attached to buttons
        self.text_rect = pygame.Rect(self.rect.left + 18, self.rect.top + 18, self.rect.w - 36, self.rect.h - 66)
        self.text = TextAreaWrapped(self.text_rect, scenario_text, font, (51, 51, 51))

        # Whether prompt is selected or not
        self.hovered = False

        # Scenario results
        self.res = scenario_res
        self.res_text = font.render(
            ' '.join(f"{METERS_SHORTHAND[k]}: {v}" for k, v in self.res.items() if v != 0), True, (255, 255, 255)
        )

    def draw(self, screen, gamestate):
        if gamestate.button_states[self.id]:
            screen.blit(self.selected_surf, self.rect)
        elif self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unselected_surf, self.rect)
        self.text.draw(screen, gamestate)
        screen.blit(self.res_text, self.res_text.get_rect(centerx=self.rect.centerx, centery=self.rect.centery + 45))

    def set_selected(self, gamestate, state):
        if gamestate.button_states[self.id] != state:  # Only do work if we are actually changing our state
            if gamestate.button_states[self.id]:  # If we were originally selected
                gamestate.button_states[self.id] = False
                for meter in gamestate.meters:
                    gamestate.meters_delta[meter] -= self.res[meter]
            else:
                gamestate.button_states[self.id] = True
                for meter in gamestate.meters:
                    gamestate.meters_delta[meter] += self.res[meter]


class ButtonGroup(pygame.sprite.Sprite):
    def __init__(self, group_pos: Tuple[int, int], left_button_id: int, scenarios: Dict[str, Union[str, Dict[str, int]]]):
        super().__init__()
        self.left_button = Button(group_pos, left_button_id, scenarios[CHOICE_ONE], scenarios[CHOICE_ONE_RESULTS])
        self.right_button = Button(
            (self.left_button.rect.right + 10, group_pos[1]),
            left_button_id + 1, scenarios[CHOICE_TWO], scenarios[CHOICE_TWO_RESULTS]
        )

        self.rect = pygame.Rect(group_pos, (self.left_button.rect.width + self.right_button.rect.width + 20,
                                            self.left_button.rect.height))

    def draw(self, screen, gamestate):
        self.left_button.draw(screen, gamestate)
        self.right_button.draw(screen, gamestate)

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        self.left_button.set_selected(gamestate, self.left_button.rect.collidepoint(pos))
        self.right_button.set_selected(gamestate, self.right_button.rect.collidepoint(pos))

    def handle_hover(self, pos: Tuple[int, int]):
        self.left_button.hovered = self.left_button.rect.collidepoint(pos)
        self.right_button.hovered = self.right_button.rect.collidepoint(pos)


class NextRound(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Next round buttons
        self.disabled_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_disabled.png").convert()
        self.unhovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_up.png").convert()
        self.hovered_surf = pygame.image.load(ASSETS_DIR / "buttons" / "nextquarter_hover.png").convert()

        # Next round position
        self.rect = self.unhovered_surf.get_rect(topleft=(10, 75))

        # Whether or not the player is hovering over the button
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, gamestate):
        if gamestate.ready_for_next_round():
            if self.hovered:
                screen.blit(self.hovered_surf, self.rect)
            else:
                screen.blit(self.unhovered_surf, self.rect)
        else:
            screen.blit(self.disabled_surf, self.rect)

    def handle_click(self, gamestate, _: Tuple[int, int]):
        gamestate.transition_round()


class TextArea(pygame.sprite.Sprite):
    def __init__(self, position, value, font_size):
        super().__init__()
        font = pygame.font.SysFont("comic sans ms", font_size)
        self.text = font.render(value, True, FONT_COLOR)
        self.rect = self.text.get_rect(topleft=position)

    def draw(self, screen, _):
        screen.blit(self.text, self.rect)


class TextAreaWrapped(pygame.sprite.Sprite):
    def __init__(self, area: pygame.Rect, value: str, font: pygame.font.Font, color: Tuple[int, int, int]):
        super().__init__()
        self.surf = pygame.Surface(area.size, pygame.SRCALPHA)
        self.rect = area
        draw_text_wrapped(self.surf, value, color, pygame.Rect((0, 0), area.size), font)

    def draw(self, screen, _):
        screen.blit(self.surf, self.rect)


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw_text_wrapped(surface, text, color, rect, font):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        image = font.render(text[:i], True, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text
