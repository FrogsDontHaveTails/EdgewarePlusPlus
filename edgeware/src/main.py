if __name__ == "__main__":
    import os

    from paths import Data

    # Required on Windows
    os.environ["PATH"] += os.pathsep + str(Data.ROOT)

from threading import Thread
from tkinter import Tk

import pygame
import utils
from features.corruption import corruption_danger_check, handle_corruption
from features.drive import fill_drive, replace_images
from features.hibernate import main_hibernate, start_main_hibernate
from features.image_popup import ImagePopup
from features.misc import (
    display_notification,
    handle_booru_download,
    handle_discord,
    handle_keyboard,
    handle_mitosis_mode,
    handle_timer_mode,
    handle_wallpaper,
    make_desktop_icons,
    make_tray_icon,
    open_web,
    play_audio,
)
from features.prompt import Prompt
from features.startup_splash import StartupSplash
from features.subliminal_message_popup import SubliminalMessagePopup
from features.video_popup import VideoPopup
from pack import Pack
from panic import start_panic_listener
from roll import RollTarget, roll_targets
from settings import Settings, first_launch_configure
from state import State
from xtoys_event_handler import XToysEventHandler
import asyncio


def main(root: Tk, settings: Settings, pack: Pack, targets: list[RollTarget]) -> None:
    roll_targets(settings, targets)
    Thread(target=lambda: fill_drive(root, settings, pack, state), daemon=True).start()  # Thread for performance reasons
    root.after(settings.delay, lambda: main(root, settings, pack, targets))


if __name__ == "__main__":
    utils.init_logging("main")

    first_launch_configure()

    root = Tk()
    root.withdraw()
    settings = Settings()
    pack = Pack(settings.pack_path)
    state = State()
    pygame.init()

    xtoys_event_handler = XToysEventHandler(settings, pack)
    asyncio.run(xtoys_event_handler.start())

    settings.corruption_mode = settings.corruption_mode and pack.corruption_levels

    # if sound is laggy or strange try changing buffer size (doc: https://www.pygame.org/docs/ref/mixer.html)
    # TODO: check if pygame.mixer.quit() is preferable to use in panic? seems fine without it
    pygame.mixer.init()
    pygame.mixer.set_num_channels(settings.max_audio)

    corruption_danger_check(settings, pack)

    # TODO: Use a dict?
    targets = [
        RollTarget(lambda: ImagePopup(root, settings, pack, state), settings.image_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: VideoPopup(root, settings, pack, state), settings.video_chance if not settings.mitosis_mode else 0),
        RollTarget(lambda: SubliminalMessagePopup(settings, pack), settings.subliminal_message_popup_chance),
        RollTarget(lambda: Prompt(settings, pack, state), settings.prompt_chance),
        RollTarget(lambda: play_audio(pack), settings.audio_chance),
        RollTarget(lambda: open_web(pack), settings.web_chance),
        RollTarget(lambda: display_notification(settings, pack), settings.notification_chance),
    ]

    def start_main() -> None:
        Thread(target=lambda: replace_images(root, settings, pack), daemon=True).start()  # Thread for performance reasons
        make_tray_icon(root, settings, pack, state, lambda: main_hibernate(root, settings, pack, state, targets))
        make_desktop_icons(settings)
        handle_corruption(root, settings, pack, state)
        handle_booru_download(settings, state)
        handle_discord(root, settings, pack)
        handle_timer_mode(root, settings, state)
        handle_mitosis_mode(root, settings, pack, state)
        handle_keyboard(root, settings, state)
        start_panic_listener(root, settings, state)

        if settings.hibernate_mode:
            start_main_hibernate(root, settings, pack, state, targets)
        else:
            handle_wallpaper(root, settings, pack, state)
            main(root, settings, pack, targets)

    if settings.startup_splash:
        StartupSplash(settings, pack, start_main)
    else:
        start_main()

    root.mainloop()
