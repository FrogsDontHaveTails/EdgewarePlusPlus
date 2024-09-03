from dataclasses import dataclass
from pathlib import Path

PATH = Path(__file__).parent.parent

PACK_PATH = PATH / "resource"


@dataclass
class Process:
    ROOT = PATH / "src"

    CONFIG = PATH / "config.py"
    MAIN = PATH / "main.py"


@dataclass
class Assets:
    ROOT = PATH / "assets"

    CORRUPTION_ABRUPT = ROOT / "corruption_abruptfade.png"
    CORRUPTION_DEFAULT = ROOT / "corruption_defaultfade.png"
    CORRUPTION_NOISE = ROOT / "corruption_noisefade.png"
    THEME_DEMO = ROOT / "theme_demo.png"

    DEFAULT_ICON = ROOT / "default_icon.ico"
    CONFIG_ICON = ROOT / "config_icon.ico"
    PANIC_ICON = ROOT / "panic_icon.ico"

    DEFAULT_CONFIG = ROOT / "default_config.json"
    DEFAULT_IMAGE = ROOT / "default_image.png"
    DEFAULT_STARTUP_SPLASH = ROOT / "loading_splash.png"
    DEFAULT_SUBLIMINAL = ROOT / "default_spiral.gif"
    DEFAULT_PANIC_WALLPAPER = ROOT / "default_win10.jpg"
    DEFAULT_WALLPAPER = ROOT / "default_wallpaper.png"


@dataclass
class Data:
    ROOT = PATH / "data"

    BACKUPS = ROOT / "backups"
    CONFIG = ROOT / "config.json"
    LOGS = ROOT / "logs"
    MOODS = ROOT / "moods"

    PRESETS = PATH / "presets"  # TODO: Proper location
