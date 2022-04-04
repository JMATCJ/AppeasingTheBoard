import sys
from pathlib import Path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MOUSE_LEFT_CLICK = 1
FONT_COLOR = (222, 222, 222)

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
    METER_CASH: 50,  # 80
    METER_MORALE: 50,  # 60
    METER_PROD: 50,  # 70
    METER_REP: 50  # 70
}

# Increase in chance of being fired
FIRE_STEPS = {
    METER_CASH: 100 / METER_CUTOFFS[METER_CASH],
    METER_MORALE: 50 / METER_CUTOFFS[METER_MORALE],
    METER_PROD: 70 / METER_CUTOFFS[METER_PROD],
    METER_REP: 60 / METER_CUTOFFS[METER_REP]
}

TITLE_SCREEN_INSTRUCTIONS = "You are a CEO tasked with keeping your company afloat. You will be given prompts and choices that affect your company's cash, morale, productivity, and reputation. Pump up your numbers, we don't need rookie numbers here."

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")
