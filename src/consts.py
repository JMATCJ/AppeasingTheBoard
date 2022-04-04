import sys
from pathlib import Path

from pygame.event import custom_type

# Random stuff
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MOUSE_LEFT_CLICK = 1
FONT_COLOR = (222, 222, 222)
BACKGROUND_COLOR = (100, 100, 100)
DARKER_FONT_COLOR = (51, 51, 51)
WHITE = (255, 255, 255)
VERDANA = "Verdana"
COMIC_SANS = "Comic Sans"
NEWGAME = custom_type()
PROMPT_X_POS = 380
CHOICE_BTN_X_POS = 712

# Meters keys
METER_CASH = "CompanyCash"
METER_MORALE = "EmployeeMorale"
METER_PROD = "EmployeeProductivity"
METER_REP = "CompanyReputation"

# Meters keys->shorthand
METERS_SHORTHAND = {
    METER_CASH: "Cash",
    METER_MORALE: "Morale",
    METER_PROD: "Prod",
    METER_REP: "Rep"
}

# Scenarios keys
SCENARIO_TEXT = "Scenario"
CHOICE_ONE = "Choice1"
CHOICE_TWO = "Choice2"
CHOICE_ONE_RESULTS = "SelectChoice1"
CHOICE_TWO_RESULTS = "SelectChoice2"

# When your chance of being pushed out goes > 0
METER_CUTOFFS = {
    METER_CASH: 70,    # 80
    METER_MORALE: 50,  # 60
    METER_PROD: 60,    # 70
    METER_REP: 60      # 70
}

# Increase in chance of being fired
FIRE_STEPS = {
    METER_CASH: 100 / METER_CUTOFFS[METER_CASH],     # 100
    METER_MORALE: 50 / METER_CUTOFFS[METER_MORALE],  # 50
    METER_PROD: 70 / METER_CUTOFFS[METER_PROD],      # 70
    METER_REP: 60 / METER_CUTOFFS[METER_REP]         # 60
}

TITLE_SCREEN_INSTRUCTIONS = "You are a CEO tasked with keeping your company afloat. You will be given prompts and \
choices that affect your company's cash, morale, productivity, and reputation. At the end of each year, your Board of \
Directors will evaluate your performance and decide on whether or not to keep you. For your first year, the Board will \
go easier on you, but don't make the same mistake in the second year. Learn what makes them tick, and pump up your \
numbers, we don't need rookie numbers."
GAME_OVER_FLAVORTEXT = "The Board of Directors was not impressed by your performance, and they have relieved you of \
your duties."

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, "frozen", False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")
