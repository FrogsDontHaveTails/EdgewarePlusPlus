import webbrowser
from tkinter import (
    CENTER,
    GROOVE,
    RAISED,
    Button,
    Checkbutton,
    Event,
    Frame,
    Label,
    Message,
    OptionMenu,
    Scale,
    StringVar,
    Text,
    Toplevel,
)
from tkinter.font import Font

from config_window.utils import BUTTON_FACE, all_children, set_widget_states
from config_window.vars import Vars
from panic import send_panic
from paths import CustomAssets
from PIL import ImageTk
from pynput import keyboard
from widgets.scroll_frame import ScrollFrame
from widgets.tooltip import CreateToolTip

INTRO_TEXT = 'Welcome to Edgeware++!\nYou can use the tabs at the top of this window to navigate the various config settings for the main program. Annoyance/Runtime is for how the program works while running, Modes is for more complicated and involved settings that change how Edgeware works drastically, and Troubleshooting and About are for learning this program better and fixing errors should anything go wrong.\n\nAside from these helper memos, there are also tooltips on several buttons and sliders. If you see your mouse cursor change to a "question mark", hover for a second or two to see more information on the setting.'
PANIC_TEXT = '"Panic" is a feature that allows you to instantly halt the program and revert your desktop background back to the "panic background" set in the wallpaper sub-tab. (found in the annoyance tab)\n\nThere are a few ways to initiate panic, but one of the easiest to access is setting a hotkey here. You should also make sure to change your panic wallpaper to your currently used wallpaper before using Edgeware!'


class KeyListenerWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.title("Key Listener")
        self.wm_attributes("-topmost", 1)
        self.geometry("250x250")
        self.focus_force()
        Label(self, text="Press any key or exit").pack(expand=1, fill="both")


def request_legacy_panic_key(button: Button, var: StringVar) -> None:
    window = KeyListenerWindow()

    def assign_panic_key(event: Event) -> None:
        button.configure(text=f"Set Legacy\nPanic Key\n<{event.keysym}>")
        var.set(str(event.keysym))
        window.destroy()

    window.bind("<KeyPress>", assign_panic_key)


def request_global_panic_key(button: Button, var: StringVar) -> None:
    window = KeyListenerWindow()

    def close() -> None:
        window.destroy()
        listener.stop()

    def assign_panic_key(key: keyboard.Key) -> None:
        button.configure(text=f"Set Global\nPanic Key\n<{str(key)}>")
        var.set(str(key))
        close()

    listener = keyboard.Listener(on_release=assign_panic_key)
    listener.start()
    window.protocol("WM_DELETE_WINDOW", close)


class StartTab(ScrollFrame):
    def __init__(self, vars: Vars, title_font: Font, message_group: list[Message], local_version: str, live_version: str):
        super().__init__()

        intro_message = Message(self.viewPort, text=INTRO_TEXT, justify=CENTER, width=675)
        intro_message.pack(fill="both")
        message_group.append(intro_message)

        # Information
        Label(self.viewPort, text="Information", font=title_font, relief=GROOVE).pack(pady=2)

        information_frame = Frame(self.viewPort, borderwidth=5, relief=RAISED)
        information_frame.pack(fill="x")

        github_frame = Frame(information_frame)
        github_frame.pack(fill="both", side="left", expand=1)
        github_url = "https://github.com/araten10/EdgewarePlusPlus"
        download_url = "https://github.com/araten10/EdgewarePlusPlus/archive/refs/heads/main.zip"
        Button(github_frame, text="Open Edgeware++ Github", command=lambda: webbrowser.open(github_url)).pack(fill="both", expand=1)
        Button(github_frame, text="Download Newest Update", command=lambda: webbrowser.open(download_url)).pack(fill="both", expand=1)

        version_frame = Frame(information_frame)
        version_frame.pack(fill="both", side="left", expand=1)
        Label(version_frame, text=f"Edgeware++ Local Version:\n{local_version}").pack(fill="x")
        Label(version_frame, text=f"Edgeware++ Github Version:\n{live_version}", bg=(BUTTON_FACE if (local_version == live_version) else "red")).pack(fill="x")

        # Theme
        Label(self.viewPort, text="Theme", font=title_font, relief=GROOVE).pack(pady=2)

        # TODO: Use Theme object
        def theme_helper(theme):
            skiplist = [
                theme_demo_frame,
                theme_demo_popup_frame,
                theme_demo_prompt_frame,
                theme_demo_config_frame,
                theme_demo_popup_title,
                theme_demo_prompt_title,
                theme_demo_config_title,
            ]
            if theme == "Original":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="#f0f0f0")
                    if isinstance(widget, Button):
                        widget.configure(bg="#f0f0f0", fg="black", font="TkDefaultFont", activebackground="#f0f0f0", activeforeground="black")
                    if isinstance(widget, Label):
                        widget.configure(bg="#f0f0f0", fg="black", font="TkDefaultFont")
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="#f0f0f0", fg="black", font="TkDefaultFont", activebackground="#f0f0f0", activeforeground="black")
                    if isinstance(widget, Text):
                        widget.configure(bg="white", fg="black")
                    if isinstance(widget, Scale):
                        widget.configure(bg="#f0f0f0", fg="black", font="TkDefaultFont", activebackground="#f0f0f0", troughcolor="#c8c8c8")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="#f0f0f0", fg="black", font="TkDefaultFont", selectcolor="white", activebackground="#f0f0f0", activeforeground="black"
                        )
                theme_demo_popup_tooltip.background = "#ffffff"
                theme_demo_popup_tooltip.foreground = "#000000"
                theme_demo_popup_tooltip.bordercolor = "#000000"
            if theme == "Dark":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="#282c34")
                    if isinstance(widget, Button):
                        widget.configure(bg="#282c34", fg="ghost white", font=("Segoe UI", 9), activebackground="#282c34", activeforeground="ghost white")
                    if isinstance(widget, Label):
                        widget.configure(bg="#282c34", fg="ghost white", font=("Segoe UI", 9))
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="#282c34", fg="ghost white", font=("Segoe UI", 9), activebackground="#282c34", activeforeground="ghost white")
                    if isinstance(widget, Text):
                        widget.configure(bg="#1b1d23", fg="ghost white")
                    if isinstance(widget, Scale):
                        widget.configure(bg="#282c34", fg="ghost white", font=("Segoe UI", 9), activebackground="#282c34", troughcolor="#c8c8c8")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="#282c34",
                            fg="ghost white",
                            font=("Segoe UI", 9),
                            selectcolor="#1b1d23",
                            activebackground="#282c34",
                            activeforeground="ghost white",
                        )
                theme_demo_popup_tooltip.background = "#1b1d23"
                theme_demo_popup_tooltip.foreground = "#ffffff"
                theme_demo_popup_tooltip.bordercolor = "#ffffff"
            if theme == "The One":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="#282c34")
                    if isinstance(widget, Button):
                        widget.configure(bg="#282c34", fg="#00ff41", font=("Consolas", 8), activebackground="#1b1d23", activeforeground="#00ff41")
                    if isinstance(widget, Label):
                        widget.configure(bg="#282c34", fg="#00ff41", font=("Consolas", 8))
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="#282c34", fg="#00ff41", font=("Consolas", 8), activebackground="#282c34", activeforeground="#00ff41")
                    if isinstance(widget, Text):
                        widget.configure(bg="#1b1d23", fg="#00ff41")
                    if isinstance(widget, Scale):
                        widget.configure(bg="#282c34", fg="#00ff41", font=("Consolas", 8), activebackground="#282c34", troughcolor="#009a22")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="#282c34", fg="#00ff41", font=("Consolas", 8), selectcolor="#1b1d23", activebackground="#282c34", activeforeground="#00ff41"
                        )
                theme_demo_popup_tooltip.background = "#1b1d23"
                theme_demo_popup_tooltip.foreground = "#00ff41"
                theme_demo_popup_tooltip.bordercolor = "#00ff41"
            if theme == "Ransom":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="#841212")
                    if isinstance(widget, Button):
                        widget.configure(bg="#841212", fg="yellow", font=("Arial", 9), activebackground="#841212", activeforeground="yellow")
                    if isinstance(widget, Label):
                        widget.configure(bg="#841212", fg="white", font=("Arial Bold", 9))
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="#841212", fg="white", font=("Arial Bold", 9), activebackground="#841212", activeforeground="white")
                    if isinstance(widget, Text):
                        widget.configure(bg="white", fg="black")
                    if isinstance(widget, Scale):
                        widget.configure(bg="#841212", fg="white", font=("Arial", 9), activebackground="#841212", troughcolor="#c8c8c8")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="#841212", fg="white", font=("Arial", 9), selectcolor="#5c0d0d", activebackground="#841212", activeforeground="white"
                        )
                theme_demo_popup_tooltip.background = "#ff2600"
                theme_demo_popup_tooltip.foreground = "#ffffff"
                theme_demo_popup_tooltip.bordercolor = "#000000"
            if theme == "Goth":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="#282c34")
                    if isinstance(widget, Button):
                        widget.configure(bg="#282c34", fg="MediumPurple1", font=("Constantia", 9), activebackground="#282c34", activeforeground="MediumPurple1")
                    if isinstance(widget, Label):
                        widget.configure(bg="#282c34", fg="MediumPurple1", font=("Constantia", 9))
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="#282c34", fg="MediumPurple1", font=("Constantia", 9), activebackground="#282c34", activeforeground="MediumPurple1")
                    if isinstance(widget, Text):
                        widget.configure(bg="MediumOrchid2", fg="purple4")
                    if isinstance(widget, Scale):
                        widget.configure(bg="#282c34", fg="MediumPurple1", font=("Constantia", 9), activebackground="#282c34", troughcolor="MediumOrchid2")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="#282c34",
                            fg="MediumPurple1",
                            font=("Constantia", 9),
                            selectcolor="#1b1d23",
                            activebackground="#282c34",
                            activeforeground="MediumPurple1",
                        )
                theme_demo_popup_tooltip.background = "#1b1d23"
                theme_demo_popup_tooltip.foreground = "#cc60ff"
                theme_demo_popup_tooltip.bordercolor = "#b999fe"
            if theme == "Bimbo":
                for widget in all_children(theme_demo_frame):
                    if widget in skiplist:
                        continue
                    if isinstance(widget, Frame):
                        widget.configure(bg="pink")
                    if isinstance(widget, Button):
                        widget.configure(bg="pink", fg="deep pink", font=("Constantia", 9), activebackground="hot pink", activeforeground="deep pink")
                    if isinstance(widget, Label):
                        widget.configure(bg="pink", fg="deep pink", font=("Constantia", 9))
                    if isinstance(widget, OptionMenu):
                        widget.configure(bg="pink", fg="deep pink", font=("Constantia", 9), activebackground="hot pink", activeforeground="deep pink")
                    if isinstance(widget, Text):
                        widget.configure(bg="light pink", fg="magenta2")
                    if isinstance(widget, Scale):
                        widget.configure(bg="pink", fg="deep pink", font=("Constantia", 9), activebackground="pink", troughcolor="hot pink")
                    if isinstance(widget, Checkbutton):
                        widget.configure(
                            bg="pink", fg="deep pink", font=("Constantia", 9), selectcolor="light pink", activebackground="pink", activeforeground="deep pink"
                        )
                theme_demo_popup_tooltip.background = "#ffc5cd"
                theme_demo_popup_tooltip.foreground = "#ff3aa3"
                theme_demo_popup_tooltip.bordercolor = "#ff84c1"
            set_widget_states(False, test_group, theme)

        theme_types = ["Original", "Dark", "The One", "Ransom", "Goth", "Bimbo"]

        theme_frame = Frame(self.viewPort, borderwidth=5, relief=RAISED)
        theme_frame.pack(fill="x")

        theme_selection_frame = Frame(theme_frame)
        theme_selection_frame.pack(fill="both", side="left")
        theme_dropdown = OptionMenu(theme_selection_frame, vars.theme, *theme_types, command=lambda key: theme_helper(key))
        theme_dropdown.configure(width=12)
        theme_dropdown.pack(fill="both", side="top")
        ignore_config_toggle = Checkbutton(theme_selection_frame, text="Ignore Config", variable=vars.theme_ignore_config, cursor="question_arrow")
        ignore_config_toggle.pack(fill="both", side="top")
        CreateToolTip(ignore_config_toggle, "When enabled, the selected theme does not apply to the config window.")

        theme_demo_frame = Frame(theme_frame)
        theme_demo_frame.pack(fill="both", side="left", expand=1)

        theme_demo_popup_frame = Frame(theme_demo_frame)
        theme_demo_popup_frame.pack(fill="both", side="left", padx=1)
        theme_demo_popup_title = Label(theme_demo_popup_frame, text="Popup")
        theme_demo_popup_title.pack(side="top")
        self.viewPort.demo_popup_image = ImageTk.PhotoImage(file=CustomAssets.theme_demo())  # Stored to avoid garbage collection
        theme_demo_popup_label = Label(
            theme_demo_popup_frame, image=self.viewPort.demo_popup_image, width=150, height=75, borderwidth=2, relief=GROOVE, cursor="question_arrow"
        )
        theme_demo_popup_label.pack(side="top", ipadx=1, ipady=1)
        theme_demo_popup_tooltip = CreateToolTip(
            theme_demo_popup_label,
            "NOTE: the test image is very small, buttons and captions will appear proportionally larger here!\n\nAlso, look! The tooltip changed too!",
        )
        Button(theme_demo_popup_label, text="Test~").place(x=-10, y=-10, relx=1, rely=1, anchor="se")
        Label(theme_demo_popup_label, text="Lewd Caption Here!").place(x=5, y=5)

        theme_demo_prompt_frame = Frame(theme_demo_frame)
        theme_demo_prompt_frame.pack(fill="both", side="left", padx=1)
        theme_demo_prompt_title = Label(theme_demo_prompt_frame, text="Prompt")
        theme_demo_prompt_title.pack()
        theme_demo_prompt_body = Frame(theme_demo_prompt_frame, borderwidth=2, relief=GROOVE, width=150, height=75)
        theme_demo_prompt_body.pack(fill="both", expand=1)
        Label(theme_demo_prompt_body, text="Do as I say~").pack(fill="both", expand=1)
        Text(theme_demo_prompt_body, width=18, height=1).pack(fill="both")
        Button(theme_demo_prompt_body, text="Sure!").pack(expand=1)

        theme_demo_config_frame = Frame(theme_demo_frame)
        theme_demo_config_frame.pack(fill="both", side="left", padx=1)
        theme_demo_config_title = Label(theme_demo_config_frame, text="Config")
        theme_demo_config_title.pack(side="top")
        theme_demo_config_body = Frame(theme_demo_config_frame, borderwidth=2, relief=GROOVE)
        theme_demo_config_body.pack(fill="both", expand=1)

        theme_demo_config_col_1 = Frame(theme_demo_config_body)
        theme_demo_config_col_1.pack(side="left", fill="both", expand=1)
        Button(theme_demo_config_col_1, text="Activated").pack(fill="y")
        Scale(theme_demo_config_col_1, orient="horizontal", from_=1, to=100, highlightthickness=0).pack(fill="y", expand=1)

        theme_demo_config_col_2 = Frame(theme_demo_config_body)
        theme_demo_config_col_2.pack(side="left", fill="both", expand=1)
        theme_demo_config_button_deactivated = Button(theme_demo_config_col_2, text="Deactivated")
        theme_demo_config_button_deactivated.pack(fill="y")
        theme_demo_button_scale_deactivated = Scale(theme_demo_config_col_2, orient="horizontal", from_=1, to=100, highlightthickness=0)
        theme_demo_button_scale_deactivated.pack(fill="y", expand=1)
        test_group = [theme_demo_button_scale_deactivated, theme_demo_config_button_deactivated]
        set_widget_states(False, test_group)

        Checkbutton(theme_demo_config_body, text="Check").pack(fill="y")
        theme_demo_config_dropdown = OptionMenu(theme_demo_config_body, StringVar(self.viewPort, "Option"), *["Option", "Menu"])
        theme_demo_config_dropdown.config(highlightthickness=0)
        theme_demo_config_dropdown.pack(fill="y")

        theme_helper(vars.theme.get())

        # Other
        Label(self.viewPort, text="Other", font=title_font, relief=GROOVE).pack(pady=2)

        other_frame = Frame(self.viewPort, borderwidth=5, relief=RAISED)
        other_frame.pack(fill="x")

        other_col_1 = Frame(other_frame)
        other_col_1.pack(fill="both", side="left", expand=1)
        toggle_flair_button = Checkbutton(other_col_1, text="Show Loading Flair", variable=vars.startup_splash, cursor="question_arrow")
        toggle_flair_button.pack(fill="x")
        CreateToolTip(toggle_flair_button, 'Displays a brief "loading" image before Edgeware startup, which can be set per-pack by the pack creator.')
        Checkbutton(other_col_1, text="Run Edgeware on Save & Exit", variable=vars.run_on_save_quit).pack(fill="x")

        other_col_2 = Frame(other_frame)
        other_col_2.pack(fill="both", side="left", expand=1)
        Checkbutton(other_col_2, text="Create Desktop Icons", variable=vars.desktop_icons).pack(fill="x")
        toggle_safe_mode_button = Checkbutton(other_col_2, text='Warn if "Dangerous" Settings Active', variable=vars.safe_mode, cursor="question_arrow")
        toggle_safe_mode_button.pack(fill="x")
        CreateToolTip(
            toggle_safe_mode_button,
            "Asks you to confirm before saving if certain settings are enabled.\n"
            "Things defined as Dangerous Settings:\n\n"
            "Extreme (code red! code red! make sure you fully understand what these do before using!):\n"
            "Replace Images\n\n"
            "Major (very dangerous, can affect your computer):\n"
            "Launch on Startup, Fill Drive\n\n"
            "Medium (can lead to embarassment or reduced control over Edgeware):\n"
            "Timer Mode, Mitosis Mode, Show on Discord, short hibernate cooldown\n\n"
            "Minor (low risk but could lead to unwanted interactions):\n"
            "Disable Panic Hotkey, Run on Save & Exit",
        )

        Checkbutton(other_frame, text="Disable Config Help Messages\n(requires save & restart)", variable=vars.message_off).pack(fill="both", expand=1)

        # Panic
        Label(self.viewPort, text="Panic Settings", font=title_font, relief=GROOVE).pack(pady=2)

        panic_message = Message(self.viewPort, text=PANIC_TEXT, justify=CENTER, width=675)
        panic_message.pack(fill="both")
        message_group.append(panic_message)

        panic_frame = Frame(self.viewPort, borderwidth=5, relief=RAISED)
        panic_frame.pack(fill="x")

        set_global_panic_button = Button(
            panic_frame,
            text=f"Set Global\nPanic Key\n<{vars.global_panic_key.get()}>",
            command=lambda: request_global_panic_key(set_global_panic_button, vars.global_panic_key),
            cursor="question_arrow",
        )
        set_global_panic_button.pack(fill="x", side="left", expand=1)
        CreateToolTip(set_global_panic_button, "This is a global key that does not require focus to activate. Press the key at any time to perform panic.")
        set_legacy_panic_button = Button(
            panic_frame,
            text=f"Set Legacy\nPanic Key\n<{vars.panic_key.get()}>",
            command=lambda: request_legacy_panic_key(set_legacy_panic_button, vars.panic_key),
            cursor="question_arrow",
        )
        set_legacy_panic_button.pack(fill="x", side="left", expand=1)
        CreateToolTip(
            set_legacy_panic_button,
            'This is the old panic key. To use this hotkey you must be "focused" on an Edgeware image or video popup. Click on a popup before using.',
        )
        Button(panic_frame, text="Perform Panic", command=send_panic).pack(fill="both", side="left", expand=1)
        
        # Other
        Label(self.viewPort, text="Xtoys", font=title_font, relief=GROOVE).pack(pady=2)
