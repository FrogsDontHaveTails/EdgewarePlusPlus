from tkinter import (
    GROOVE,
    RAISED,
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    messagebox,
)
from tkinter.font import Font
from config_window.utils import set_widget_states_with_colors
from config_window.vars import Vars
from widgets.scroll_frame import ScrollFrame


def validate_xtoys_websocket(name: str) -> bool:
    return True  # TODO: Check if websocket is valid and can connect to xtoys


class XToysTab(ScrollFrame):
    def __init__(self, vars: Vars, title_font: Font):
        super().__init__()

        Label(
            self.viewPort,
            text="XToys Settings",
            font=title_font,
            relief=GROOVE,
        ).pack(pady=2)

        download_frame = Frame(self.viewPort, borderwidth=5, relief=RAISED)
        download_frame.pack(fill="both")

        xtoys_frame = Frame(download_frame)
        xtoys_frame.pack(fill="y", side="left")
        Label(xtoys_frame, text="Websocket Adress").pack(fill="x")
        xtoys_name_entry = Entry(xtoys_frame, textvariable=vars.xtoys_websocket)
        xtoys_name_entry.pack(fill="x")
        xtoys_validate = Button(
            xtoys_frame,
            text="Validate",
            command=lambda: (
                messagebox.showinfo("Success!", "Websocket is valid.")
                if validate_xtoys_websocket(vars.booru_name.get())
                else messagebox.showerror("Failed", "Websocket is invalid.")
            ),
        )
        xtoys_validate.pack(fill="x")

        download_group = [
            xtoys_name_entry,
            xtoys_validate,
        ]
        # See comment above
        # download_group.append(min_score_slider)
        set_widget_states_with_colors(
            vars.xtoys_enabled.get(), download_group, "white", "gray25"
        )

        enable_frame = Frame(download_frame)
        enable_frame.pack(fill="both", side="right")
        Checkbutton(
            enable_frame,
            text="Enable XToys",
            variable=vars.xtoys_enabled,
            command=lambda: (
                set_widget_states_with_colors(
                    vars.xtoys_enabled.get(), download_group, "white", "gray25"
                )
            ),
        ).pack()
