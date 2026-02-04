"""Tkinter GUI wrapper for the Vigilant TBA game."""

from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk, simpledialog

import labels as L
from game import Game


class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game."""

    IMAGE_WIDTH = 1000
    IMAGE_HEIGHT = 460
    TITLE_BAR_HEIGHT = 36
    FOOTER_HEIGHT = 36
    GRADIENT_HEIGHT = 90
    BG_COLOR = "#15171a"
    PANEL_COLOR = "#101214"
    TEXT_BG = "#0e1012"
    TEXT_FG = "#e6e6e6"
    ACCENT = "#4ba3c3"
    BTN_BG = "#2a2f35"
    BTN_ACTIVE = "#39414a"
    CONSOLE_BG = "#0c1015"
    CONSOLE_HEADER = "#141a21"
    CONSOLE_TEXT = "#d4d9de"

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("1200x820")
        self.minsize(1000, 700)
        self.configure(bg=self.BG_COLOR)

        self.game = Game()
        self.game.room_change_callback = self._update_room_image
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Overlay.Vertical.TScrollbar",
            background="#1b2026",
            troughcolor=self.CONSOLE_BG,
            bordercolor=self.CONSOLE_BG,
            lightcolor=self.CONSOLE_BG,
            darkcolor=self.CONSOLE_BG,
            arrowcolor="#2a2f35",
        )
        style.map(
            "Overlay.Vertical.TScrollbar",
            background=[("active", "#2a2f35")],
        )

        self._build_layout()
        self._show_starting_image()

        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        self.game.set_input_provider(self._prompt_input)

        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = L.DEFAULT_PLAYER_NAME

        self.game.setup(player_name=name)
        self.game.choice_intro()

        self._update_room_image()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _show_starting_image(self):
        assets_dir = Path(__file__).parent / "assets"
        image_path = assets_dir / "starting_picture.png"
        if not image_path.exists():
            return

        self._image_ref = tk.PhotoImage(file=str(image_path))
        self._current_image_name = image_path.name
        self._room_title = "Vigilant"
        self._room_exits = ""
        self._draw_canvas_image()

    def _build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        image_frame = tk.Frame(
            self,
            bg=self.PANEL_COLOR,
            height=self.IMAGE_HEIGHT,
        )
        image_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 6))
        image_frame.grid_propagate(False)
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(
            image_frame,
            bg="#0b0d10",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self._image_ref = None
        self._current_image_name = None
        self._room_title = ""
        self._room_exits = ""

        overlay_frame = tk.Frame(
            image_frame,
            bg=self.CONSOLE_BG,
            highlightthickness=1,
            highlightbackground="#1e242b",
        )
        overlay_frame.place(relx=0.04, rely=0.62, relwidth=0.92, relheight=0.26)
        overlay_frame.grid_rowconfigure(1, weight=1)
        overlay_frame.grid_columnconfigure(0, weight=1)

        header = tk.Frame(overlay_frame, bg=self.CONSOLE_HEADER)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Journal de bord",
            bg=self.CONSOLE_HEADER,
            fg=self.CONSOLE_TEXT,
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=2,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        scrollbar = ttk.Scrollbar(
            overlay_frame,
            orient="vertical",
            style="Overlay.Vertical.TScrollbar",
        )
        self.text_output = tk.Text(
            overlay_frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            state="disabled",
            bg=self.CONSOLE_BG,
            fg=self.CONSOLE_TEXT,
            insertbackground=self.TEXT_FG,
            font=("Cascadia Mono", 10),
            padx=10,
            pady=6,
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
        )
        self.text_output.configure(spacing1=3, spacing2=2, spacing3=3)
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        overlay_frame.lift()

        bottom_frame = tk.Frame(self, bg=self.BG_COLOR)
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        bottom_frame.grid_columnconfigure(0, weight=1)

        controls_frame = tk.Frame(bottom_frame, bg=self.BG_COLOR)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        controls_frame.grid_columnconfigure(1, weight=1)

        move_frame = tk.LabelFrame(
            controls_frame,
            text="Déplacements",
            bg=self.BG_COLOR,
            fg=self.TEXT_FG,
            bd=0,
            labelanchor="n",
        )
        move_frame.grid(row=0, column=0, sticky="w", padx=(0, 10))

        assets_dir = Path(__file__).parent / "assets"
        self._btn_left = tk.PhotoImage(file=str(assets_dir / "left-arrow-50.png"))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / "right-arrow-50.png"))

        tk.Button(
            move_frame,
            image=self._btn_left,
            command=lambda: self._send_command("go O"),
            bd=0,
            bg=self.BTN_BG,
            activebackground=self.BTN_ACTIVE,
        ).grid(row=0, column=0, padx=4, pady=4)
        tk.Button(
            move_frame,
            image=self._btn_right,
            command=lambda: self._send_command("go E"),
            bd=0,
            bg=self.BTN_BG,
            activebackground=self.BTN_ACTIVE,
        ).grid(row=0, column=1, padx=4, pady=4)

        actions_frame = tk.Frame(controls_frame, bg=self.BG_COLOR)
        actions_frame.grid(row=0, column=1, sticky="ew")
        actions_frame.grid_columnconfigure(0, weight=1)

        command_frame = tk.Frame(actions_frame, bg=self.BG_COLOR)
        command_frame.grid(row=0, column=0, sticky="ew")
        for col in range(9):
            command_frame.grid_columnconfigure(col, weight=1, uniform="command")

        command_buttons = [
            ("Observer", "look", None),
            ("Invent.", "check", None),
            ("Map", "map", None),
            ("Statut", "status", None),
            ("Quêtes", "quests", None),
            ("Quête", "quest", "Numéro de quête"),
            ("Activer", "activate", "Numéro de quête"),
            ("Récomp.", "rewards", None),
            ("Aide", "help", None),
            ("Parler", "talk", "Numéro du personnage"),
            ("Prendre", "take", "Numéro de l'objet"),
            ("Déposer", "drop", "Numéro de l'objet"),
            ("Utiliser", "use", "Numéro de l'objet"),
            ("Attaquer", "attack", "Nom de l'ennemi"),
            ("Aller", "go", "Direction (N/E/S/O)"),
            ("Retour", "back", None),
            ("Histor.", "history", None),
            ("Quitter", "quit", None),
        ]

        for index, (label, command, prompt) in enumerate(command_buttons):
            row = index // 9
            col = index % 9
            if prompt:
                action = lambda cmd=command, pr=prompt: self._prompt_command(cmd, pr)
            else:
                action = lambda cmd=command: self._send_command(cmd)
            tk.Button(
                command_frame,
                text=label,
                command=action,
                bd=0,
                bg=self.BTN_BG,
                fg=self.TEXT_FG,
                activebackground=self.BTN_ACTIVE,
                activeforeground=self.TEXT_FG,
                padx=6,
                pady=3,
                font=("Segoe UI", 8, "bold"),
                width=8,
            ).grid(row=row, column=col, padx=3, pady=2, sticky="ew")

        entry_frame = tk.Frame(bottom_frame, bg=self.BG_COLOR)
        entry_frame.grid(row=1, column=0, sticky="ew")
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_frame,
            textvariable=self.entry_var,
            bg=self.TEXT_BG,
            fg=self.TEXT_FG,
            insertbackground=self.TEXT_FG,
            font=("Segoe UI", 12),
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BTN_BG,
            highlightcolor=self.ACCENT,
        )
        self.entry.grid(row=0, column=0, sticky="ew", ipady=6, padx=(0, 6))
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

        tk.Button(
            entry_frame,
            text="Envoyer",
            command=lambda: self._on_enter(),
            bd=0,
            bg=self.ACCENT,
            fg="#0b0d10",
            activebackground="#6bbad3",
            activeforeground="#0b0d10",
            padx=16,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=1, sticky="e")

    def _prompt_input(self, prompt):
        self.update_idletasks()
        response = simpledialog.askstring("Entrée", prompt, parent=self)
        if self.entry:
            self.entry.focus_set()
        return response.strip() if response else ""

    def _prompt_command(self, command, prompt):
        response = simpledialog.askstring("Commande", prompt, parent=self)
        if response:
            self._send_command(f"{command} {response.strip()}")

    def _update_room_image(self):
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / "assets"
        image_path = assets_dir / (room.image or "scene.png")
        if not image_path.exists():
            image_path = assets_dir / "scene.png"

        self._room_title = room.name
        self._room_exits = room.get_exit_string()

        if image_path.exists() and image_path.name != self._current_image_name:
            self._image_ref = tk.PhotoImage(file=str(image_path))
            self._current_image_name = image_path.name

        if self._image_ref and image_path.exists():
            self._draw_canvas_image()
            self.update_idletasks()
            return

        self._image_ref = None
        self._current_image_name = None

        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text=f"Image: {room.name}",
            fill=self.TEXT_FG,
            font=("Segoe UI", 18, "bold"),
        )
        self.update_idletasks()

    def _draw_canvas_image(self):
        self.canvas.delete("all")
        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        self.canvas.create_image(width / 2, height / 2, image=self._image_ref)

        self.canvas.create_rectangle(
            0,
            0,
            width,
            self.TITLE_BAR_HEIGHT,
            fill="#0b0d10",
            outline="",
        )
        self.canvas.create_text(
            16,
            self.TITLE_BAR_HEIGHT / 2,
            text=self._room_title,
            fill=self.TEXT_FG,
            anchor="w",
            font=("Segoe UI", 12, "bold"),
        )

        gradient_colors = ["#0b0d10", "#0f1216", "#12161a", "#15171a"]
        step_height = self.GRADIENT_HEIGHT // len(gradient_colors)
        for index, color in enumerate(gradient_colors):
            y1 = height - self.GRADIENT_HEIGHT + (index * step_height)
            y2 = y1 + step_height
            self.canvas.create_rectangle(0, y1, width, y2, fill=color, outline="")

        self.canvas.create_rectangle(
            0,
            height - self.FOOTER_HEIGHT,
            width,
            height,
            fill="#0b0d10",
            outline="",
        )
        self.canvas.create_text(
            16,
            height - (self.FOOTER_HEIGHT / 2),
            text=self._room_exits,
            fill=self.TEXT_FG,
            anchor="w",
            font=("Segoe UI", 10),
        )

    def _on_canvas_resize(self, _event=None):
        if self._image_ref:
            self._draw_canvas_image()

    def _on_enter(self, _event=None):
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")

    def _send_command(self, command):
        if self.game.finished:
            return
        print(f"> {command}\n")
        self.game.process_command(command)
        self._update_room_image()
        if not self.game.finished:
            if self.game.win():
                print(L.GAME_WIN_TEXT)
                self.game.finished = True
            elif self.game.lose():
                print(L.GAME_LOSE_TEXT)
                self.game.finished = True
            else:
                self.game.character_move()
        if not self.game.finished:
            self.entry.focus_set()
        if self.game.finished:
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)

    def _on_close(self):
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point for GUI or CLI."""
    args = sys.argv[1:]
    if "--cli" in args:
        Game().play()
        return
    app = GameGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
