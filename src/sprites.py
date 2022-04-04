from typing import Any, Callable, Dict, Tuple, Union

from pygame import image, mouse, Rect, Surface
from pygame.font import Font, SysFont
from pygame.locals import SRCALPHA
from pygame.mixer import init, Sound
from pygame.sprite import Sprite

from consts import *

# Setup the click sound effect
init()  # Make sure mixer is initialized before doing this
button_click_sound = Sound(ASSETS_DIR / "sounds" / "click.ogg")
button_click_sound.set_volume(0.3)


class Meter(Sprite):
    def __init__(self, meter_pos: Tuple[int, int], meter_type: str, meter_text: str, meter_image: str):
        super().__init__()

        # Meter surfaces
        self.bg_surf = image.load(ASSETS_DIR / "meters" / "background.png").convert()
        self.fg_surf = image.load(ASSETS_DIR / "meters" / meter_image).convert()

        # Meter position
        self.rect = self.bg_surf.get_rect(topleft=meter_pos)  # bg_rect, called rect for external use purposes
        self.fg_rect = self.fg_surf.get_rect(topleft=meter_pos)

        # Meter title
        self.font = SysFont(VERDANA, 24)
        self.text = self.font.render(meter_text, True, FONT_COLOR)
        self.text_rect = self.text.get_rect(topleft=(meter_pos[0], meter_pos[1] + self.rect.h))

        # Meter type
        self.type = meter_type

    def draw(self, screen, gamestate):
        # Blit the meter
        screen.blit(self.bg_surf, self.rect)
        screen.blit(self.fg_surf, self.fg_rect, self.fg_surf.get_rect(
            w=self.fg_surf.get_width() * (gamestate.meters[self.type] / 100)
        ))

        # Blit the title
        screen.blit(self.text, self.text_rect)

        # Build and blit the current value and delta of the meter
        meter_text = f"{gamestate.meters[self.type]} / 100"
        if gamestate.meters_delta[self.type] > 0:
            meter_text += f" (+{gamestate.meters_delta[self.type]})"
        elif gamestate.meters_delta[self.type] < 0:
            meter_text += f" ({gamestate.meters_delta[self.type]})"
        meter_text_surf = self.font.render(meter_text, True, FONT_COLOR)
        screen.blit(meter_text_surf, meter_text_surf.get_rect(center=self.rect.center))


class PromptChoice(Sprite):
    def __init__(self, button_pos: Tuple[int, int], id: int, scenario_text: str, scenario_res: Dict[str, int]):
        super().__init__()

        # Used to index into the GameState.button_states array later
        self.id = id

        # The surfaces for the three button states
        self.unselected_surf = image.load(ASSETS_DIR / "buttons" / "prompt_up.png").convert()
        self.hovered_surf = image.load(ASSETS_DIR / "buttons" / "prompt_hover.png").convert()
        self.selected_surf = image.load(ASSETS_DIR / "buttons" / "prompt_select.png").convert()

        # Position of button (same for all three states)
        self.rect = self.unselected_surf.get_rect(topleft=button_pos)

        # Whether prompt is selected or not
        self.hovered = False

        # Prompt text attached to buttons
        font = SysFont(VERDANA, 16)
        inner_rect = self.rect.inflate(-36, -36)  # Shrink by 18px on all sides, still centered on button
        text_rect = inner_rect.inflate(0, -48).move(0, -18)  # Create gap on bottom, move to keep it centered
        self.text = TextAreaWrapped(text_rect, scenario_text, font, DARKER_FONT_COLOR)

        # Scenario results
        self.res = scenario_res
        res_rect = Rect(inner_rect.left, text_rect.bottom, inner_rect.width, inner_rect.height - text_rect.height)
        res_str = ", ".join(f"{METERS_SHORTHAND[k]}: {'+' if v > 0 else ''}{v}" for k, v in self.res.items() if v != 0)
        self.res_textarea = TextAreaWrapped(res_rect, res_str, font, WHITE, centered=True)

    def draw(self, screen, gamestate):
        # Blit the button
        if gamestate.button_states[self.id]:
            screen.blit(self.selected_surf, self.rect)
        elif self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unselected_surf, self.rect)

        # Blit the texts onto the button
        self.text.draw(screen, gamestate)
        self.res_textarea.draw(screen, gamestate)

    def set_selected(self, gamestate, state):
        if gamestate.button_states[self.id] != state:  # Only do work if we are actually changing our state
            if gamestate.button_states[self.id]:       # If we were originally selected
                gamestate.button_states[self.id] = False
                for meter in gamestate.meters:
                    gamestate.meters_delta[meter] -= self.res[meter]
            else:
                gamestate.button_states[self.id] = True
                for meter in gamestate.meters:
                    gamestate.meters_delta[meter] += self.res[meter]


class Prompt(Sprite):
    def __init__(self, y_pos: int, left_btn_id: int, scenario: Dict[str, Union[str, Dict[str, int]]]):
        super().__init__()

        # Build the buttons
        self.left_button = PromptChoice((CHOICE_BTN_X_POS, y_pos), left_btn_id, scenario[CHOICE_ONE],
                                        scenario[CHOICE_ONE_RESULTS])
        self.right_button = PromptChoice((self.left_button.rect.right + 10, y_pos), left_btn_id + 1,
                                         scenario[CHOICE_TWO], scenario[CHOICE_TWO_RESULTS])
        self.buttons_rect = self.left_button.rect.union(self.right_button.rect)

        # Build the text area
        prompt_font = SysFont(VERDANA, 20)
        self.prompt_text = TextAreaWrapped(
            Rect(PROMPT_X_POS, y_pos, self.buttons_rect.left - 10 - PROMPT_X_POS, self.buttons_rect.h),
            scenario[SCENARIO_TEXT], prompt_font, FONT_COLOR
        )

        # Union their rects together to make an all-encompassing rect
        self.rect = self.buttons_rect.union(self.prompt_text.rect)

    def draw(self, screen, gamestate):
        self.prompt_text.draw(screen, gamestate)
        self.left_button.draw(screen, gamestate)
        self.right_button.draw(screen, gamestate)

    def handle_click(self, gamestate, pos: Tuple[int, int]):
        if self.buttons_rect.collidepoint(pos):
            self.left_button.set_selected(gamestate, self.left_button.rect.collidepoint(pos))
            self.right_button.set_selected(gamestate, self.right_button.rect.collidepoint(pos))
            button_click_sound.play()

    def handle_hover(self, pos: Tuple[int, int]):
        self.left_button.hovered = self.left_button.rect.collidepoint(pos)
        self.right_button.hovered = self.right_button.rect.collidepoint(pos)


class NextRound(Sprite):
    def __init__(self):
        super().__init__()

        # Next round buttons
        self.disabled_surf = image.load(ASSETS_DIR / "buttons" / "nextquarter_disabled.png").convert()
        self.unhovered_surf = image.load(ASSETS_DIR / "buttons" / "nextquarter_up.png").convert()
        self.hovered_surf = image.load(ASSETS_DIR / "buttons" / "nextquarter_hover.png").convert()

        self.rect = self.unhovered_surf.get_rect(topleft=(10, 75))  # Next round position
        self.hovered = self.rect.collidepoint(mouse.get_pos())  # Whether or not the player is hovering over the button

    def draw(self, screen, gamestate):
        if gamestate.ready_for_next_round():
            if self.hovered:
                screen.blit(self.hovered_surf, self.rect)
            else:
                screen.blit(self.unhovered_surf, self.rect)
        else:
            screen.blit(self.disabled_surf, self.rect)

    def handle_click(self, gamestate, _: Tuple[int, int]):
        if gamestate.ready_for_next_round():  # Only move on if we've made a choice for each prompt
            button_click_sound.play()
            gamestate.transition_round()


class GenericButton(Sprite):
    def __init__(self, button_pos: Tuple[int, int], file_basename: str, handle_click_func: Callable[[], Any]):
        super().__init__()

        # Button states
        self.unhovered_surf = image.load(ASSETS_DIR / "buttons" / f"{file_basename}_up.png").convert()
        self.hovered_surf = image.load(ASSETS_DIR / "buttons" / f"{file_basename}_hover.png").convert()

        self.rect = self.unhovered_surf.get_rect(topleft=button_pos)  # Button position
        self.hovered = self.rect.collidepoint(mouse.get_pos())  # Whether or not the player is hovering over the button
        self.click_func = handle_click_func

    def draw(self, screen, _):
        if self.hovered:
            screen.blit(self.hovered_surf, self.rect)
        else:
            screen.blit(self.unhovered_surf, self.rect)

    def handle_click(self, _1, _2: Tuple[int, int]):
        button_click_sound.play()
        self.click_func()


class TextArea(Sprite):
    def __init__(self, position, value, font_size):
        super().__init__()
        font = SysFont(COMIC_SANS, font_size)
        self.text = font.render(value, True, FONT_COLOR)
        self.rect = self.text.get_rect(topleft=position)

    def draw(self, screen, _):
        screen.blit(self.text, self.rect)


class TextAreaWrapped(Sprite):
    def __init__(self, area: Rect, value: str, font: Font, color: Tuple[int, int, int], centered=False):
        super().__init__()
        self.surf = Surface(area.size, SRCALPHA)
        self.rect = area
        draw_text_wrapped(self.surf, value, color, Rect((0, 0), area.size), font, centered)

    def draw(self, screen, _):
        screen.blit(self.surf, self.rect)


# Totally not stolen from the internet
def draw_text_wrapped(surface, text, color, rect, font, centered=False):
    rect = Rect(rect)
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
        while font.size(text[:i])[0] < rect.width and i <= len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i <= len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        text_surf = font.render(text[:i], True, color)

        # Do text centering
        line_left = rect.left
        if centered:
            line_left += (rect.w - text_surf.get_width()) // 2

        # Do the blit
        surface.blit(text_surf, (line_left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text
