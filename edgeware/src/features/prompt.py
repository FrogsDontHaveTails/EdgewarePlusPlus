from tkinter import Button, Label, Text, Toplevel

import os_utils
import utils
from features.theme import get_theme
from pack import Pack
from settings import Settings
from state import State
from eventmanager.eventmanager import EventManager


class Prompt(Toplevel):
    def __init__(self, settings: Settings, pack: Pack, state: State):
        self.prompt = pack.random_prompt()
        self.state = state
        if not self.should_init():
            return
        super().__init__()

        self.theme = get_theme(settings)

        self.attributes("-topmost", True)
        os_utils.set_borderless(self)
        self.configure(background=self.theme.bg)

        monitor = utils.primary_monitor()
        width = monitor.width // 4
        height = monitor.height // 2
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        Label(self, text="\n" + pack.index.default.prompt_command + "\n", fg=self.theme.fg, bg=self.theme.bg).pack()

        Label(self, text=self.prompt, wraplength=width, fg=self.theme.fg, bg=self.theme.bg).pack()

        input = Text(self, fg=self.theme.text_fg, bg=self.theme.text_bg)
        input.pack()
        button = Button(
            self,
            text=pack.index.default.prompt_submit,
            command=lambda: self.submit(settings.prompt_max_mistakes, self.prompt, input.get(1.0, "end-1c")),
            fg=self.theme.fg,
            bg=self.theme.bg,
            activeforeground=self.theme.fg,
            activebackground=self.theme.bg,
        )
        button.place(x=-10, y=-10, relx=1, rely=1, anchor="se")

    def should_init(self) -> bool:
        if not self.state.prompt_active and self.prompt:
            self.state.prompt_active = True
            return True
        return False

    # Checks that the number of mistakes is at most max_mistakes and if so,
    # closes the prompt window. The number of mistakes is computed as the edit
    # (Levenshtein) distance between a and b.
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    def submit(self, max_mistakes: int, a: str, b: str) -> None:
        d = [[j for j in range(0, len(b) + 1)]] + [[i] for i in range(1, len(a) + 1)]

        for j in range(1, len(b) + 1):
            for i in range(1, len(a) + 1):
                d[i].append(
                    min(
                        d[i - 1][j] + 1,
                        d[i][j - 1] + 1,
                        d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
                    )
                )  # fmt: skip

        if d[len(a)][len(b)] <= max_mistakes:
            EventManager().trigger("prompt_submit_success", d[len(a)][len(b)])
            self.destroy()
            self.state.prompt_active = False
        else:
            EventManager().trigger("prompt_submit_failed", d[len(a)][len(b)])
