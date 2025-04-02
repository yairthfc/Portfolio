#################################################################
# FILE : boggle.py
# WRITERS : David Zvi Kadish (davidzvi), Yair Mahfud (yairthfc)
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: The user interface and "control center" of the game.
# WEBSITES I USED: www.w3schools.com, www.programiz.com
#################################################################

import tkinter as tki
from tkinter import ttk
import threading
from boggle_model import BoggleModel
from typing import List, Dict
from ex11_utils import format_words, game_over_text
BUTTON_STYLE = {"font": ("Courier", 40), "borderwidth": 1,
                "relief": tki.RAISED, "bg": "#E0E0FF"}
ON = "on"
OFF = "off"
PLEASE_WAIT: str = "Please wait..."


class GameGui:
    _buttons = {}

    def __init__(self) -> None:
        """initiating a tkinter program with all the windows, frames, lables and starting buttons"""
        root = tki.Tk()
        root.title("Boogle")
        root.resizable(False, False)
        root.geometry('830x472')
        self.current_word = ""
        self._main_window = root
        self._game_running: bool = False
        self._opening = True

        self._left_frame = tki.Frame(root, bg='lightgray')
        self._left_frame.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
        self._left_frame.pack_propagate(0)

        self._right_frame = tki.Frame(root, bg='SlateGray1')
        self._right_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)
        self._right_frame.pack_propagate(0)

        self._score_n_time_display = tki.Frame(
            self._right_frame, bg="lightgray", relief="ridge", height=47)
        self._score_n_time_display.pack(
            side=tki.TOP, padx=5, pady=5, fill=tki.X)

        self._score_display = tki.Frame(
            self._score_n_time_display, bg='gray', relief="ridge")
        self._score_display.pack(
            side=tki.RIGHT, padx=2, pady=2, fill=tki.BOTH, expand=True)

        self._score_title = tki.Label(
            self._score_display, bg='gray', text="SCORE", relief="ridge", font=("Courier", 20), width=2)
        self._score_title.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)

        self._score_value = tki.Label(
            self._score_display, bg='lightblue', relief="ridge", font=("Courier", 20), text="0")
        self._score_value.pack(
            side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self._time_display = tki.Frame(
            self._score_n_time_display, bg='gray', relief="ridge")
        self._time_display.pack(side=tki.LEFT, padx=2,
                                pady=2, fill=tki.BOTH, expand=True)

        self._time_title = tki.Label(self._time_display, font=(
            "Courier", 20), bg="gray", text="TIME", relief="ridge", width=2)
        self._time_title.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)

        self._time_value = tki.Label(self._time_display, font=(
            "Courier", 20), bg="lightblue", relief="ridge", text="03:00")
        self._time_value.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self._upleft_display = tki.Frame(
            self._left_frame, bg='blue', relief="ridge", height=47)
        self._upleft_display.pack(
            side=tki.TOP, fill=tki.X, padx=5, pady=5)

        self._word_display = tki.Label(
            self._upleft_display, bg='gray', relief="ridge", font=("Courier", 20), height=1)
        self._word_display.pack(side=tki.LEFT, padx=6,
                                pady=6, fill=tki.BOTH, expand=True)

        self._left_for_buttons = tki.Frame(
            self._left_frame, bg='lightpink', relief="ridge")
        self._left_for_buttons.pack(
            side=tki.TOP, fill=tki.BOTH, expand=True)

        self._left_label = tki.Label(
            self._left_for_buttons, bg="#E0E0FF", relief="ridge",
            text="DZ and Yairi\nproductions present:\nBoggle!", font=("Courier", 20),
            justify="center")
        self._left_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._word_did_display_frame = tki.Frame(
            self._right_frame, bg="lightblue")
        self._word_did_display_frame.pack(
            side=tki.TOP, fill=tki.BOTH, expand=True)

        self._found_words = tki.Text(
            self._word_did_display_frame, bg="lightblue", state="disabled", cursor="arrow", font=("Courier", 15))
        self._found_words.bind('<Button-1>', lambda event: 'break')
        self._found_words.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._word_display_scrollbar = ttk.Scrollbar(
            self._found_words, command=self._found_words.yview)
        self._found_words.config(
            yscrollcommand=self._word_display_scrollbar.set)
        self._word_display_scrollbar.pack(side=tki.RIGHT, fill="y")

        self._start_button = tki.Button(self._right_frame, text="Start Game", bg='gray', relief="groove", font=(
            "Courier", 30), width=1)
        self._start_button.pack(side=tki.BOTTOM, expand=False, fill="x")

        self._enter_button = tki.Button(
            self._upleft_display, text="ENTER", bg='lightblue', relief="groove", font=("Courier", 25), width=5)
        self._enter_button.pack(side=tki.RIGHT, expand=False, fill="x")

    def delete_opening_lablel(self):
        """deletes the opening label"""
        self._left_label.destroy()
        self._opening = False

    def is_opening(self):
        return self._opening

    def set_start_command(self, cmd):
        """setting the start button command"""
        self._start_button.configure(command=cmd)

    def set_enter_command(self, cmd):
        """setting the enter button command"""
        self._enter_button.configure(command=cmd)

    def is_game_running(self):
        """returns if the game is running(bool)"""
        return self._game_running

    def update_words(self, words: str):
        """updating the words given on the words found frame"""
        self._found_words["state"] = "normal"
        self._found_words.delete(1.0, tki.END)
        self._found_words.insert(1.0, words)
        self._found_words.update()
        self._found_words["state"] = "disabled"

    def run(self) -> None:
        """run the tkinter program"""
        self._main_window.mainloop()

    def set_score_display(self, score_value: str):
        """set the score value display"""
        self._score_value["text"] = score_value

    def set_word_display(self, word_display: str):
        """set the current word display"""
        self._word_display["text"] = word_display

    def set_button_command(self, button_name: str, cmd) -> None:
        """setting the letters button command"""
        self._buttons[button_name].configure(command=cmd)

    def create_buttons_on_left_frame(self, let_lst):
        """creating the buttons on the left frame according to the list given"""
        for i in range(4):
            tki.Grid.columnconfigure(self._left_frame, i, weight=1)
        for i in range(4):
            tki.Grid.rowconfigure(self._left_frame, i, weight=1)
        counter = 0
        for i in range(4):
            for j in range(4):
                self._make_button(let_lst[counter], counter, i, j)
                counter += 1

    def set_button_letters(self, letter_list: List):
        for index, button in enumerate(self._buttons.values()):
            button.configure(text=letter_list[index])

    def disable_buttons(self):
        """disabling the buttons"""
        for key in self._buttons.values():
            key.configure(state="disabled")
        self._enter_button.configure(state="disabled")

    def enable_buttons(self):
        """enabling the buttons"""
        for key in self._buttons.values():
            key.configure(state="normal")
        self._enter_button.configure(state="normal")

    def _make_button(self, button_letter: str, counter, row: int, column: int, rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """setting a button according to the parameters given"""
        button = tki.Button(
            self._left_for_buttons, text=button_letter, **BUTTON_STYLE, height=1, width=3)
        button.grid(row=row, column=column, rowspan=rowspan,
                    columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[counter] = button

        def _on_enter(event: any) -> None:
            """defining what happens when the pointer goes over the button"""
            button['background'] = 'lightgreen'

        def _on_leave(event: any) -> None:
            """defining what happens when the pointer goes off the button"""
            button['bg'] = '#E0E0FF'
        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def game_over(self, text: str) -> None:
        """finishes the game and updating the update words text"""
        self.disable_buttons()
        self.update_words(text)
        self._start_button.configure(state="normal")

    def get_buttons(self):
        """get the dict of the current buttons"""
        """Returns the buttons on the left side of the board."""
        return self._buttons

    def toggle_game(self, mode: str):
        """Toggels the game "on" or "off"."""
        self._game_running = True if mode == "on" else False

    def is_game_running(self):
        """checks if the game is running"""
        return self._game_running

    def set_time_value(self, clock_time):
        """setting the time value"""
        total_minutes, total_seconds = divmod(clock_time, 60_000)
        total_seconds //= 1000
        self._time_value.config(
            text=f'{total_minutes:02}:{total_seconds:02}')

    def get_time_value(self):
        """getting the time value"""
        return self._time_value["text"]

    def update_time_value(self):
        """updating the time value"""
        self._time_value.update_idletasks()

    def change_start_text(self, text: str):
        """changing the start button text"""
        self._start_button["text"] = text

    def toggle_start(self, mode: str):
        self._start_button["state"] = "normal" if mode == ON else "disabled"


class boogle_main:
    def __init__(self, words) -> None:
        """initiating a boggle game with creating its gui and model in order to 
        combine them into the full program"""
        self._gui = GameGui()
        self._model = BoggleModel(words)
        self._gui.set_start_command(self.set_start_action)
        self._valid_words: List[str] = []

    def load(self) -> None:
        """'Loads' up the game finding the max score and valid words for the game
            to display when it's over."""
        self._gui.toggle_game(ON)
        self._gui.toggle_start(OFF)
        self._gui.update_words(PLEASE_WAIT)
        self.get_all_valid_words_and_max_score()
        self._gui.update_words("")
        self._gui.toggle_start(ON)
        self._gui.change_start_text("End Game")

    def set_start_action(self):
        """setting the actions that are happening when the start button is beng pressed
        including starting the time, defining the buttons and load the game management"""
        if self._gui.get_buttons() != {}:
            self._model.reset()
        self.load()
        self.run_timer(self._model.get_start_time())
        self._gui.enable_buttons()
        if self._gui.is_opening():
            self._gui.delete_opening_lablel()
        letters = self._model.get_letter_list()
        if self._gui.get_buttons() == {}:
            self._gui.create_buttons_on_left_frame(letters)
        else:
            self._gui.set_button_letters(letters)
        for button in self._gui._buttons:
            cell_loc = self._model.get_cell_loc(button)
            action = self.set_button_action(cell_loc)
            self._gui.set_button_command(button, action)
        self._gui.enable_buttons()
        self.set_end_game_command()
        self._gui.set_enter_command(self.set_enter_action)

    def set_end_game_command(self):
        """setting end game command"""
        self._gui.set_start_command(self.set_end_game_action)

    def set_end_game_action(self):
        """setting what happens when the game ends and the user presses on the button"""
        self._gui.set_time_value(0)
        self._gui.update_time_value()
        self._gui.change_start_text("Start Game")
        self._gui.toggle_game(OFF)
        self.end_game()

    def set_enter_action(self):
        """setting the actions that are happening when you press enter including
        changing displays of words and score"""
        self._model.add_word()
        self._gui.update_words(format_words(self._model.get_words()))
        self._gui.set_score_display(self._model.get_score())
        self._gui.set_word_display("")

    def set_button_action(self, letter_loc):
        """setting a button action for a letter button"""
        def fun():
            self._model.add_letter(letter_loc)
            word = self._model.get_current_word()
            self._gui.set_word_display(word)
        return fun

    def run(self):
        """running the gui"""
        self._gui.run()

    def get_all_valid_words_and_max_score(self):
        """getting all of the valid words and the max possible score for the game"""
        self._valid_words: List[str] = self._model.all_valid_words()
        self._max_score = len(self._valid_words)

    def end_game(self):
        """ending the game and restarting all the values"""
        self._gui.set_start_command(self.set_start_action)
        max_score = len(self._valid_words)
        found_words = len(self._model.get_words())
        words = [
            word for word in self._valid_words if word not in self._model.get_words()]
        self._gui.game_over(game_over_text(
            words, max_score, found_words, len(self._valid_words)))
        self._gui.set_time_value(0)
        self._gui.update_time_value()

    def run_timer(self, clock_time):
        """running the timer of the game"""
        if self._gui.is_game_running():
            self._gui.set_time_value(clock_time)
            self._gui.update_time_value()
        if clock_time <= 0 and self._gui.is_game_running() == True or \
                self._gui.get_time_value() == "00:00":
            self._gui.toggle_game(OFF)
            self.end_game()
            return
        clock_time -= 1000
        return self._gui._main_window.after(1000, self.run_timer, clock_time)

####your boggle_dict.txt location under
with open("\\boggle_dict.txt") as f:
    words = [word.strip("\n") for word in f]
boogle_main(words).run()

