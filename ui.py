import math
import tkinter as tk
from tkinter import ttk, Tk, PhotoImage
import random
import sys
import time
import pygame
from paragraph import paragraph
import numpy as np

# Initialize pygame mixer
pygame.mixer.init()

SAMPLE = random.choice(paragraph)

YELLOWISH = "#FCFFE0"
GREEN = "#BACD92"
GREY = "#D1D4DC"

KEYBOARD_SWITCH_ORDER = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                         "A", "S", "D", "F", "G", "H", "J", "K", "L",
                         "semicolon", "apostrophe",
                         "Z", "X", "C", "V", "B", "N", "M", "comma", "period", "question"]


def generate_beep(frequency=440, duration_ms=100, volume=0.5):
    """Generate a beep sound using numpy and pygame."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    # Create sine wave
    buf = (np.sin(2 * np.pi * np.arange(n_samples) * frequency / sample_rate) * 32767 * volume).astype(np.int16)
    sound = pygame.mixer.Sound(buffer=buf)
    return sound


class UI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.title("Type Master")
        app_icon = tk.PhotoImage(file="assets/water_mark.png")
        self.root.iconphoto(True, app_icon)
        self.root.config(background="#FCFFE0")

        self.first_frame = tk.Frame(self.root, background=YELLOWISH)
        self.first_frame.pack(pady=5)

        self.second_frame = tk.Frame(self.root, background=GREEN)
        self.second_frame.pack()

        self.third_frame = tk.Frame(self.root, background=YELLOWISH)
        self.third_frame.pack(pady=10)

        self.fourth_frame = tk.Frame(self.root, background=GREY)
        self.fourth_frame.pack()

        self.points = 0
        self.sample_list = [i for i in SAMPLE]
        self.COUNT = 0
        self.timer_id = None
        self.is_timer_running = False
        self.last_sound_time = 0
        self.sound_cooldown = 0.05
        self.typing_started = False

        # Load sounds
        self.error_sound = generate_beep(300, 100)   # low frequency, short duration
        self.success_sound = generate_beep(700, 100) # high frequency, short duration

        # First frame
        self.play_button_img = PhotoImage(file="assets/play_key.png")
        self.pause_button_img = PhotoImage(file="assets/pause_key.png")
        self.points_label = ttk.Label(self.first_frame, text=f"Score: {self.points}", background=YELLOWISH)
        self.points_label.grid(column=0, row=0)

        pause_button = PhotoImage(file="assets/pause_key.png")
        self.pause_button = tk.Button(self.first_frame, image=pause_button, highlightthickness=0, border=0,
                                      cursor="hand2", command=self.pause_time)
        self.pause_button.image = pause_button
        self.pause_button.grid(column=1, row=0)

        reset_button = PhotoImage(file="assets/reset_key.png")
        self.reset_button = tk.Button(self.first_frame, image=reset_button, highlightthickness=0, border=0,
                                      cursor="hand2", command=self.reset_game)
        self.reset_button.image = reset_button
        self.reset_button.grid(column=2, row=0)

        # Beep button
        self.beep_button = tk.Button(self.first_frame, text="Mute Beep", cursor="hand2",
                                     command=self.toggle_mute)
        self.beep_button.grid(column=4, row=0, padx=10)

        #beep_button = tk.Button(self.first_frame, text="Beep", cursor="hand2",
        #                        command=lambda: self.play_sound("error"))
        #beep_button.grid(column=4, row=0, padx=10)
        self.muted = False  # new flag for muting sounds


        self.count = 0
        self.timer_label = tk.Label(self.first_frame, text=f"Time elapsed: {self.count}s", background=YELLOWISH)
        self.timer_label.grid(column=3, row=0)

        # Second frame
        self.para_text = tk.Text(self.second_frame, height=6, width=80, font=("Courier", 12), wrap=tk.WORD,
                                 bg=YELLOWISH, fg="black")
        self.para_text.insert(tk.END, SAMPLE)
        self.para_text.config(state=tk.DISABLED)
        self.para_text.tag_config("correct", foreground="green", background="lightyellow", font=("Courier", 12, "bold"))
        self.para_text.tag_config("incorrect", foreground="red", background="lightcoral")
        self.para_text.pack(padx=5, pady=5)

        # Third frame
        self.input_field = ttk.Entry(self.third_frame, width=80)
        self.input_field.bind("<Key>", self.on_key_input)
        self.input_field.bind("<BackSpace>", self.reduce_score)
        self.input_field.pack()
        self.root.after(100, self.input_field.focus)

        # Fourth frame
        self.keys = []
        self.root.bind("<Key>", self.key_handler)
        self.root.bind("<KeyRelease>", self.on_key_release_event)

    def key_handler(self, event):
        special_char = [186, 188, 190, 191, 222]
        if 65 <= event.keycode <= 90:
            for i in range(len(KEYBOARD_SWITCH_ORDER)):
                if event.char.lower() == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, True)
        elif event.keycode in special_char:
            for i in range(len(KEYBOARD_SWITCH_ORDER)):
                if event.keysym.lower() == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, True)

    def change_keys(self, index, state):
        img_file = f"assets/keys_pressed/{KEYBOARD_SWITCH_ORDER[index]}.png" if state else f"assets/keys/{KEYBOARD_SWITCH_ORDER[index]}.png"
        img = PhotoImage(file=img_file)
        self.keys[index].config(image=img)
        self.keys[index].image = img

    def on_key_release_event(self, event):
        special_char = [186, 188, 190, 191, 222]
        if 65 <= event.keycode <= 90:
            for i in range(len(KEYBOARD_SWITCH_ORDER)):
                if event.char.lower() == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, False)
        elif event.keycode in special_char:
            for i in range(len(KEYBOARD_SWITCH_ORDER)):
                if event.keysym.lower() == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, False)

    def insert_keys(self):
        row, column = 0, 0
        for i in range(len(KEYBOARD_SWITCH_ORDER)):
            if i == 10:
                row, column = 1, 0
            elif i == 21:
                row, column = 2, 0
            img = PhotoImage(file=f"assets/keys/{KEYBOARD_SWITCH_ORDER[i]}.png")
            label = ttk.Label(self.fourth_frame, image=img, background=GREY)
            label.grid(row=row, column=column)
            label.image = img
            self.keys.append(label)
            column += 1

    def play_sound(self, sound_type="error"):
        if self.muted:
            return  # do nothing if muted

        current_time = time.time()
        if current_time - self.last_sound_time < self.sound_cooldown:
            return
        self.last_sound_time = current_time

        if sound_type == "error":
            self.error_sound.play()
        elif sound_type == "success":
            self.success_sound.play()

    def toggle_mute(self):
        """Toggle muting of beep sounds with design feedback."""
        self.muted = not self.muted
        if self.muted:
            self.beep_button.config(text="Unmute Beep", bg="red", fg="white")
        else:
            self.beep_button.config(text="Mute Beep", bg="green", fg="white")
            self.play_sound("error")  # give feedback when unmuted


    def on_key_input(self, event=None):
        if not self.typing_started and self.input_field.get():
            self.typing_started = True
            self.start_timer()
        self.check_the_input(event)

    def check_the_input(self, event=None):
        text = [i for i in self.input_field.get()]
        if len(text) == len(self.sample_list):
            self.score_card()
        self.update_paragraph_highlight(len(text))
        if len(text) > 0 and len(text) == self.COUNT + 1:
            i = len(text) - 1
            if i < len(self.sample_list):
                if text[i] == self.sample_list[i]:
                    self.update_score()
                    self.play_sound("success")
                    self.COUNT += 1
                else:
                    self.play_sound("error")

    def update_paragraph_highlight(self, typed_count):
        self.para_text.config(state=tk.NORMAL)
        self.para_text.tag_remove("correct", "1.0", tk.END)
        self.para_text.tag_remove("incorrect", "1.0", tk.END)
        typed_text = self.input_field.get()
        for i in range(len(typed_text)):
            if i < len(self.sample_list):
                char_index = f"1.{i}"
                next_char_index = f"1.{i+1}"
                if typed_text[i] == self.sample_list[i]:
                    self.para_text.tag_add("correct", char_index, next_char_index)
                else:
                    self.para_text.tag_add("incorrect", char_index, next_char_index)
        self.para_text.config(state=tk.DISABLED)

    def pause_time(self):
        if self.is_timer_running:
            # Pause the timer
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.pause_button.config(image=self.play_button_img)
            self.pause_button.image = self.play_button_img
            self.is_timer_running = False
        else:
            # Resume the timer
            self.start_timer()
            self.pause_button.config(image=self.pause_button_img)
            self.pause_button.image = self.pause_button_img


    def score_card(self):
        # Clear the fourth frame
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=YELLOWISH)

        # Accuracy
        accuracy = 0
        if len(self.sample_list) > 0:
            accuracy = math.floor((self.points / len(self.sample_list)) * 100)
        accuracy_label = ttk.Label(
            self.fourth_frame,
            text=f"Accuracy: {accuracy}%",
            padding=10,
            background=YELLOWISH,
            font=("Courier", 20)
        )
        accuracy_label.pack()

        # Time taken
        time_label = ttk.Label(
            self.fourth_frame,
            text=f"Time Taken: {self.count}s",
            padding=10,
            background=YELLOWISH,
            font=("Courier", 20)
        )
        time_label.pack()

        # Words per minute
        wpm = 0
        if self.count > 0:
            wpm = math.floor((len(self.sample_list) / 5) / (self.count / 60))
        wpm_label = ttk.Label(
            self.fourth_frame,
            text=f"WPM: {wpm}",
            padding=10,
            background=YELLOWISH,
            font=("Courier", 20)
        )
        wpm_label.pack()

        # Pause timer when finished
        self.pause_time()

    def reduce_score(self, event=None):
        """Reduce score when backspace is pressed."""
        self.points -= 1
        self.points_label.config(text=f"Score: {self.points}")

    def start_timer(self, event=None):
        """Start or continue the timer that tracks elapsed time."""
        if not self.is_timer_running:
            self.is_timer_running = True
        self.count += 1
        self.timer_label.config(text=f"Time elapsed: {self.count}s")
        # Schedule the next tick after 1000 ms
        self.timer_id = self.root.after(1000, self.start_timer)
    
    def pause_time(self):
        """Pause or resume the timer, and disable/enable typing accordingly."""
        if self.is_timer_running:
            # Pause the timer
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.pause_button.config(image=self.play_button_img)
            self.pause_button.image = self.play_button_img
            self.is_timer_running = False

            # Disable typing when paused
            self.input_field.config(state=tk.DISABLED)
        else:
            # Resume the timer
            self.start_timer()
            self.pause_button.config(image=self.pause_button_img)
            self.pause_button.image = self.pause_button_img
            self.is_timer_running = True

            # Enable typing when resumed
            self.input_field.config(state=tk.NORMAL)
            self.input_field.focus()

    def update_score(self):
        """Increase score when a correct key is pressed."""
        self.points += 1
        self.points_label.config(text=f"Score: {self.points}")

    def reduce_score(self, event=None):
        """Reduce score when backspace is pressed."""
        self.points -= 1
        self.points_label.config(text=f"Score: {self.points}")

    def reset_game(self):
        # Cancel the timer if running
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Reset all game state
        self.count = 0
        self.points = 0
        self.COUNT = 0
        self.is_timer_running = False
        self.typing_started = False
        self.sample_list = [i for i in SAMPLE]
        self.input_field.delete(0, tk.END)
        self.input_field.focus()

        # Reset UI labels
        self.timer_label.config(text=f"Time elapsed: {self.count}s")
        self.points_label.config(text=f"Score: {self.points}")

        # Reset paragraph
        self.para_text.config(state=tk.NORMAL)
        self.para_text.delete("1.0", tk.END)
        self.para_text.insert(tk.END, SAMPLE)
        self.para_text.tag_remove("correct", "1.0", tk.END)
        self.para_text.tag_remove("incorrect", "1.0", tk.END)
        self.para_text.config(state=tk.DISABLED)

        # Reset pause button image
        self.pause_button.config(image=self.play_button_img)
        self.pause_button.image = self.play_button_img

        # Rebuild keyboard display
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=GREY)
        self.keys = []
        self.insert_keys()
