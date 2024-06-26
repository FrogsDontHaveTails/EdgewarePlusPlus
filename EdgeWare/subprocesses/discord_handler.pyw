import sys
import time
from pathlib import Path

from pypresence import presence

sys.path.append(str(Path(__file__).parent.parent))
from utils.paths import Resource

text_obj = ["[No discord.dat resource]", "default"]

IMGID_CONSTS = ["furcock_img", "blacked_img", "censored_img", "goon_img", "goon2_img", "hypno_img", "futa_img", "healslut_img", "gross_img"]

txt = ""

try:
    # grab discord status from discord.dat, mark as having file
    with open(Resource.DISCORD, "r") as f:
        txt = f.read()
except Exception:
    print("failed text read")

if not txt == "":
    try:
        # if has file, tries to split at newline break
        #   uses first line as the string for text description
        #   uses second line as the image id for requesting image from discord api
        ls = txt.split("\n")
        text_obj[0] = ls[0]
        if ls[1] in IMGID_CONSTS:
            text_obj[1] = ls[1]
    except Exception:
        print("failed line split")


# open discord api pipe and such
def do_discord():
    conn = presence.Presence("820204081410736148")
    conn.connect()
    conn.update(state=text_obj[0], large_image=text_obj[1], start=int(time.time()))
    while True:
        time.sleep(15)


do_discord()
