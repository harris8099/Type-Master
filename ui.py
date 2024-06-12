import math
import tkinter as tk
from tkinter import ttk, Tk, PhotoImage
import random
from paragraph import paragraph

SAMPLE = random.choice(paragraph)

YELLOWISH = "#FCFFE0"
GREEN = "#BACD92"
GREY = "#D1D4DC"

KEYBOARD_SWITCH_ORDER = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L",
                         "semicolon", "apostrophe", "Z", "X", "C", "V", "B", "N", "M", "comma", "period", "question"]
sample_list = [i for i in SAMPLE]
COUNT = 0


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

        # first frame
        # points label
        self.play_button_img = PhotoImage(file="assets/play_key.png")
        self.pause_button_img = PhotoImage(file="assets/pause_key.png")
        self.points_label = ttk.Label(self.first_frame, text=f"Score: {self.points}")
        self.points_label.config(background=YELLOWISH)
        self.points_label.grid(column=0, row=0)

        # pause button
        pause_button = PhotoImage(file="assets/pause_key.png")
        self.pause_state = True
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
        # paragraph label
        self.para = ttk.Label(self.second_frame, text=SAMPLE, background=YELLOWISH)
        self.para.config(padding=15, wraplength=700, font=("Courier", 15))
        self.para.pack()

        # Third Frame elements
        self.input_field = ttk.Entry(self.third_frame)
        self.input_field.config(width=80)
        # self.input_field.focus()
        self.input_field.bind("<Key>", self.check_the_input)
        self.input_field.bind("<Button-1>", self.start_timer)
        self.input_field.bind("<BackSpace>", self.reduce_score)
        self.input_field.pack()

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

    def check_the_input(self, event=None):
        global sample_list, COUNT
        text = [i for i in self.input_field.get()]
        if len(text) == len(sample_list):
            self.score_card()
        for i in range(0, len(text)):
            try:
                if text[i] == sample_list[i] and COUNT == i:
                    self.update_score()
                    COUNT += 1
            except IndexError:
                pass

    def score_card(self):
        for widget in self.fourth_frame.winfo_children():
            widget.destroy()
        self.fourth_frame.config(background=YELLOWISH)

        accuracy_label = ttk.Label(self.fourth_frame, text=f"Accuracy: {math.floor((self.points/len(sample_list))*100)}",
                                padding=10, background=YELLOWISH)
        accuracy_label.config(font=("Courier", 20))
        accuracy_label.pack()
        time_label = ttk.Label(self.fourth_frame, text=f"Time Taken: {self.count}",padding=10, background=YELLOWISH)
        time_label.config(font=("Courier", 20))
        time_label.pack()
        wpm_label = ttk.Label(self.fourth_frame, text=f"wpm: {math.floor(len(sample_list)/(int(self.count)/60))}",padding=10, background=YELLOWISH)
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
        self.count = self.root.after(1000, self.start_timer).split("#")[1]
        self.timer_label.config(text=f"Time elapsed: {self.count}")

    def pause_time(self):
        # play_button = PhotoImage(file="assets/play_key.png")
        # pause_button = PhotoImage(file="assets/pause_key.png")
        if not self.pause_state:
            self.start_timer()
            self.pause_button.config(image=self.pause_button_img)
            self.pause_button.image = self.pause_button_img
            self.pause_state = True
        elif self.pause_state:
            self.root.after_cancel("after#" + str(self.count))
            self.pause_button.config(image=self.play_button_img)
            self.pause_button.image = self.play_button_img
            self.pause_state = False

    def reset_game(self):
        self.root.after_cancel("after#" + str(self.count))
        self.count = 0
        self.timer_label.config(text=f"Time elapsed: {self.count}")
