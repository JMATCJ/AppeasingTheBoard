from pathlib import Path
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MOUSE_LEFT_CLICK = 1
FONT_COLOR = (222, 222, 222)

# Meters keys
METER_CASH = "cash"
METER_MORALE = "morale"
METER_PROD = "productivity"
METER_REP = "reputation"

# Check if we are in a pyinstaller "onefile" binary. Different path prefix in that case:
if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSETS_DIR = Path("assets")
