import math
import tkinter as tk
from tkinter import ttk, Tk, PhotoImage
import random
import sys
import threading
import time
from paragraph import paragraph

# Sound support (Windows)
if sys.platform == "win32":
    import winsound

SAMPLE = random.choice(paragraph)

YELLOWISH = "#FCFFE0"
GREEN = "#BACD92"
GREY = "#D1D4DC"

KEYBOARD_SWITCH_ORDER = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L",
                         "semicolon", "apostrophe", "Z", "X", "C", "V", "B", "N", "M", "comma", "period", "question"]


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
        self.first_frame.pack()
        self.first_frame.config(pady=5)
        self.second_frame = tk.Frame(self.root, background=GREEN)
        self.second_frame.pack()
        self.third_frame = tk.Frame(self.root, background=YELLOWISH)
        self.third_frame.pack()
        self.third_frame.config(pady=10)
        self.fourth_frame = tk.Frame(self.root, background=GREY)
        self.fourth_frame.pack()
        self.points = 0
        self.sample_list = [i for i in SAMPLE]
        self.COUNT = 0
        self.timer_id = None
        self.is_timer_running = False
        self.last_sound_time = 0
        self.sound_cooldown = 0.05  # 50ms cooldown between sounds
        self.typing_started = False

        # first frame
        # points label
        self.play_button_img = PhotoImage(file="assets/play_key.png")
        self.pause_button_img = PhotoImage(file="assets/pause_key.png")
        self.points_label = ttk.Label(self.first_frame, text=f"Score: {self.points}")
        self.points_label.config(background=YELLOWISH)
        self.points_label.grid(column=0, row=0)

        # pause button
        pause_button = PhotoImage(file="assets/pause_key.png")
        self.pause_button = tk.Button(self.first_frame, image=pause_button, highlightthickness=0, border=0,
                                      cursor="hand2", command=self.pause_time)
        self.pause_button.image = pause_button
        self.pause_button.grid(column=1, row=0)

        # reset button
        reset_button = PhotoImage(file="assets/reset_key.png")
        self.reset_button = tk.Button(self.first_frame, image=reset_button, highlightthickness=0, border=0,
                                      cursor="hand2", command=self.reset_game)
        self.reset_button.image = reset_button
        self.reset_button.grid(column=2, row=0)

        # timer label
        self.count = 0
        self.timer_label = tk.Label(self.first_frame, text=f"Time elapsed: {self.count}")
        self.timer_label.config(background=YELLOWISH)
        self.timer_label.grid(column=3, row=0)

        # Second Frame elements
        # paragraph label with highlighting
        self.para_text = tk.Text(self.second_frame, height=6, width=80, font=("Courier", 12), wrap=tk.WORD)
        self.para_text.config(bg=YELLOWISH, fg="black")
        self.para_text.insert(tk.END, SAMPLE)
        self.para_text.config(state=tk.DISABLED)  # Read-only
        
        # Create tag for highlighting correct characters
        self.para_text.tag_config("correct", foreground="green", background="lightyellow", font=("Courier", 12, "bold"))
        self.para_text.tag_config("incorrect", foreground="red", background="lightcoral")
        
        self.para_text.pack(padx=5, pady=5)

        # Third Frame elements
        self.input_field = ttk.Entry(self.third_frame)
        self.input_field.config(width=80)
        self.input_field.bind("<Key>", self.on_key_input)
        self.input_field.bind("<BackSpace>", self.reduce_score)
        self.input_field.pack()
        
        # Auto focus on input field
        self.root.after(100, self.input_field.focus)

        # Fourth frame
        # Keys
        self.keys = []
        # self.keys_pressed = []
        ## to be changed
        self.root.bind("<Key>", self.key_handler)
        self.root.bind("<KeyRelease>", self.on_key_release_event)

    # keyboards event listener
    def key_handler(self, event):
        special_char = [186, 188, 190, 191, 222]
        if event.keycode == 32 or event.keycode == 13:
            pass
            # self.keys_pressed.append(" ")
        elif 65 <= event.keycode <= 90:
            # self.keys_pressed.append(event.keysym)
            for i in range(0, len(KEYBOARD_SWITCH_ORDER)):
                if event.char == KEYBOARD_SWITCH_ORDER[i].lower() or event.char == KEYBOARD_SWITCH_ORDER[i]:
                    self.change_keys(i, True)
        elif event.keycode in special_char:
            # self.keys_pressed.append(event.char)
            # print(event.keysym)
            for i in range(0, len(KEYBOARD_SWITCH_ORDER)):
                if event.keysym == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, True)
        elif event.keycode == 8:
            # try:
            #     self.keys_pressed.pop()
            # except IndexError:
            #     pass
            pass
        else:
            pass
        # print(self.keys_pressed)
        # print(event.char, event.keysym, event.keycode)

    # def keys_listen(self):
    #     self.root.bind("a", lambda event: self.change_keys(10))

    def change_keys(self, index, state):
        if state:
            img = PhotoImage(file=f"assets/keys_pressed/{KEYBOARD_SWITCH_ORDER[index]}.png")
            self.keys[index].config(image=img)
            self.keys[index].image = img
        elif not state:
            img = PhotoImage(file=f"assets/keys/{KEYBOARD_SWITCH_ORDER[index]}.png")
            self.keys[index].config(image=img)
            self.keys[index].image = img

    def on_key_release_event(self, event):
        special_char = [186, 188, 190, 191, 222]
        if event.keycode == 32 or event.keycode == 13:
            pass
        elif 65 <= event.keycode <= 90:
            for i in range(0, len(KEYBOARD_SWITCH_ORDER)):
                if event.char == KEYBOARD_SWITCH_ORDER[i].lower() or event.char == KEYBOARD_SWITCH_ORDER[i]:
                    self.change_keys(i, False)
        elif event.keycode in special_char:
            # print(event.keysym)
            for i in range(0, len(KEYBOARD_SWITCH_ORDER)):
                if event.keysym == KEYBOARD_SWITCH_ORDER[i].lower():
                    self.change_keys(i, False)
        else:
            pass

    def insert_keys(self):
        row = 0
        column = 0
        for i in range(0, len(KEYBOARD_SWITCH_ORDER)):
            if i == 10:
                row = 1
                column = 0
            elif i == 21:
                row = 2
                column = 0
            img = PhotoImage(file=f"assets/keys/{KEYBOARD_SWITCH_ORDER[i]}.png")
            self.A_label = ttk.Label(self.fourth_frame, image=img, background=GREY)
            self.A_label.grid(row=row, column=column)
            self.A_label.image = img
            self.keys.append(self.A_label)
            column += 1

    def play_sound(self, sound_type="error"):
        """Play error or success sound asynchronously (non-blocking)"""
        # Prevent sound spam with cooldown
        current_time = time.time()
        if current_time - self.last_sound_time < self.sound_cooldown:
            return
        
        self.last_sound_time = current_time
        
        # Run sound in separate thread to avoid blocking UI
        if sys.platform == "win32":
            thread = threading.Thread(target=self._play_beep, args=(sound_type,), daemon=True)
            thread.start()
    
    def _play_beep(self, sound_type):
        """Internal method to play beep in separate thread"""
        try:
            if sound_type == "error":
                # Error sound: lower frequency, shorter duration
                winsound.Beep(300, 50)
            elif sound_type == "success":
                # Success sound: higher frequency, shorter duration
                winsound.Beep(700, 50)
        except:
            pass

    def on_key_input(self, event=None):
        """Handle key input - start timer on first keystroke and check input"""
        # Start timer on first keystroke
        if not self.typing_started and self.input_field.get():
            self.typing_started = True
            self.start_timer()
        
        self.check_the_input(event)

    def check_the_input(self, event=None):
        text = [i for i in self.input_field.get()]
        if len(text) == len(self.sample_list):
            self.score_card()
        
        # Update paragraph highlighting
        self.update_paragraph_highlight(len(text))
        
        # Only check the last character to reduce lag
        if len(text) > 0 and len(text) == self.COUNT + 1:
            i = len(text) - 1
            try:
                if text[i] == self.sample_list[i]:
                    self.update_score()
                    self.COUNT += 1
                else:
                    pass  # No sound to reduce lag
            except IndexError:
                pass

    def update_paragraph_highlight(self, typed_count):
        """Update paragraph highlighting based on number of characters typed"""
        self.para_text.config(state=tk.NORMAL)
        
        # Remove all previous tags
        self.para_text.tag_remove("correct", "1.0", tk.END)
        self.para_text.tag_remove("incorrect", "1.0", tk.END)
        
        # Highlight typed characters
        typed_text = self.input_field.get()
        for i in range(len(typed_text)):
            if i < len(self.sample_list):
                # Calculate character position in Text widget (line.column format)
                char_index = f"1.{i}"
                next_char_index = f"1.{i+1}"
                
                if typed_text[i] == self.sample_list[i]:
                    # Correct character - green highlight
                    self.para_text.tag_add("correct", char_index, next_char_index)
                else:
                    # Wrong character - red highlight
                    self.para_text.tag_add("incorrect", char_index, next_char_index)
        
        self.para_text.config(state=tk.DISABLED)

    def score_card(self):
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=YELLOWISH)

        accuracy_label = ttk.Label(self.fourth_frame, text=f"Accuracy: {math.floor((self.points/len(self.sample_list))*100)}%",
                                padding=10, background=YELLOWISH)
        accuracy_label.config(font=("Courier", 20))
        accuracy_label.pack()
        
        time_label = ttk.Label(self.fourth_frame, text=f"Time Taken: {self.count}s", padding=10, background=YELLOWISH)
        time_label.config(font=("Courier", 20))
        time_label.pack()
        
        # Fix: Prevent division by zero and ensure proper WPM calculation
        wpm = 0
        if self.count > 0:
            wpm = math.floor((len(self.sample_list) / 5) / (self.count / 60))  # Standard: 5 chars = 1 word
        
        wpm_label = ttk.Label(self.fourth_frame, text=f"WPM: {wpm}", padding=10, background=YELLOWISH)
        wpm_label.config(font=("Courier", 20))
        wpm_label.pack()
        
        self.pause_time()

    def reduce_score(self, event=None):
        self.points -= 1
        self.points_label.config(text=f"Score: {self.points}")

    def update_score(self):
        self.points += 1
        self.points_label.config(text=f"Score: {self.points}")

    def start_timer(self, event=None):
        if not self.is_timer_running:
            self.is_timer_running = True
        self.count += 1
        self.timer_label.config(text=f"Time elapsed: {self.count}s")
        self.timer_id = self.root.after(1000, self.start_timer)

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
        
        # Reset UI
        self.timer_label.config(text=f"Time elapsed: {self.count}s")
        self.points_label.config(text=f"Score: {self.points}")
        
        # Reset paragraph
        self.para_text.config(state=tk.NORMAL)
        self.para_text.delete("1.0", tk.END)
        self.para_text.insert(tk.END, SAMPLE)
        self.para_text.tag_remove("correct", "1.0", tk.END)
        self.para_text.tag_remove("incorrect", "1.0", tk.END)
        self.para_text.config(state=tk.DISABLED)
        
        self.pause_button.config(image=self.pause_button_img)
        self.pause_button.image = self.pause_button_img
        
        # Rebuild keyboard display
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=GREY)
        self.keys = []
        self.insert_keys()
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=GREY)
        self.keys = []
        self.insert_keys()
