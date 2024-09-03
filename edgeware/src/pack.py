import json
import os
import random
from pathlib import Path

from paths import PACK_PATH, Assets


# TODO: Handle cases where resources are not present
# TODO: Validate JSON formats
class Pack:
    # Directories
    AUDIO = PACK_PATH / "aud"
    IMAGE = PACK_PATH / "img"
    SUBLIMINALS = PACK_PATH / "subliminals"
    VIDEO = PACK_PATH / "vid"

    # Files
    CAPTIONS = PACK_PATH / "captions.json"
    CONFIG = PACK_PATH / "config.json"  # TODO
    CORRUPTION = PACK_PATH / "corruption.json"  # TODO
    DISCORD = PACK_PATH / "discord.dat"
    ICON = PACK_PATH / "icon.ico"
    INFO = PACK_PATH / "info.json"
    SPLASH = PACK_PATH / "loading_splash"
    MEDIA = PACK_PATH / "media.json"  # TODO
    PROMPT = PACK_PATH / "prompt.json"
    WALLPAPER = PACK_PATH / "wallpaper.png"
    WEB = PACK_PATH / "web.json"
    WEB_RESOURCE = PACK_PATH / "webResource.json"  # TODO

    def __init__(self):
        def list_resources(dir: Path) -> list[Path]:
            return [dir / file for file in os.listdir(dir)] if dir.is_dir() else []

        self.images = list_resources(self.IMAGE)
        self.videos = list_resources(self.VIDEO)
        self.audio = list_resources(self.AUDIO)
        self.subliminals = list_resources(self.SUBLIMINALS)

        self.icon = self.ICON if self.ICON.is_file() else Assets.DEFAULT_ICON
        self.wallpaper = self.WALLPAPER if self.WALLPAPER.is_file() else Assets.DEFAULT_WALLPAPER

        splash_paths = [self.SPLASH.with_suffix(suffix) for suffix in [".png", ".gif", ".jpg", ".jpeg", ".bmp"]]
        self.startup_splash = next((path for path in splash_paths if path.is_file()), Assets.DEFAULT_STARTUP_SPLASH)

        with open(self.CAPTIONS) as f:
            self.captions = json.loads(f.read())
            self.denial = self.captions.get("denial", "Not for you~")
            self.close_text = self.captions.get("subtext", "I Submit <3")

        with open(self.DISCORD) as f:
            image_ids = ["furcock_img", "blacked_img", "censored_img", "goon_img", "goon2_img", "hypno_img", "futa_img", "healslut_img", "gross_img"]

            discord = f.read().split("\n")
            self.discord_text = discord[0]
            self.discord_image = discord[1] if (len(discord) > 1 and discord[1] in image_ids) else "default"

        with open(self.PROMPT) as f:
            self.prompts = json.loads(f.read())
            self.prompt_command_text = self.prompts.get("commandtext", "Type for me, slut~")
            self.prompt_submit_text = self.prompts.get("subtext", "I Submit <3")

        with open(self.WEB) as f:
            self.web = json.loads(f.read())
            for i in range(len(self.web["args"])):
                self.web["args"][i] = self.web["args"][i].split(",")

    def random_image(self) -> Path:
        return random.choice(self.images)

    def random_video(self) -> Path:
        return random.choice(self.videos)

    def random_audio(self) -> Path:
        return random.choice(self.audio)

    def random_subliminal(self) -> Path:
        if len(self.subliminals) > 0:
            return random.choice(self.subliminals)
        return Assets.DEFAULT_SUBLIMINAL

    def random_caption(self) -> str:
        return random.choice(self.captions["default"])  # TODO: Moods

    def random_denial(self) -> str:
        return random.choice(self.denial)

    def random_prompt(self) -> str:
        mood = random.choices(self.prompts["moods"], self.prompts["freqList"], k=1)[0]
        length = random.randint(self.prompts["minLen"], self.prompts["maxLen"])

        prompt = ""
        for n in range(length):
            prompt += random.choice(self.prompts[mood]) + " "

        return prompt.strip()

    def random_web(self) -> str:
        i = random.randrange(len(self.web["urls"]))
        return self.web["urls"][i] + random.choice(self.web["args"][i])
