```markdown
# 📘 Function & Class Documentation

This document provides detailed descriptions of all functions, classes, and entry points used in the Typing Master application.

---

## Class: `UI`

The main class that builds and manages the Typing Master application interface.

### **Constructor**
```python
UI()
```
- **Description:** Initializes the Tkinter root window, sets up frames, loads assets, and prepares game state variables.  
- **Returns:** `UI` instance.

---

### **Methods**

#### `insert_keys()`
- **Description:** Builds the on‑screen keyboard layout with images.  
- **Parameters:** None  
- **Returns:** None  

#### `key_handler(event)`
- **Description:** Handles key press events and updates key visuals.  
- **Parameters:** `event` (Tkinter event)  
- **Returns:** None  

#### `on_key_release_event(event)`
- **Description:** Handles key release events and resets key visuals.  
- **Parameters:** `event`  
- **Returns:** None  

#### `change_keys(index, state)`
- **Description:** Updates key image based on press/release state.  
- **Parameters:**  
  - `index` (int): Key index in layout  
  - `state` (bool): True for pressed, False for released  
- **Returns:** None  

#### `play_sound(sound_type="error")`
- **Description:** Plays success/error beep sounds with cooldown.  
- **Parameters:**  
  - `sound_type` (str): `"error"` or `"success"`  
- **Returns:** None  

#### `toggle_mute()`
- **Description:** Toggles mute state for sounds and updates button UI.  
- **Parameters:** None  
- **Returns:** None  

#### `on_key_input(event=None)`
- **Description:** Starts timer on first input and checks typed text.  
- **Parameters:** `event` (optional)  
- **Returns:** None  

#### `check_the_input(event=None)`
- **Description:** Compares typed text with sample, updates score and highlights.  
- **Parameters:** `event` (optional)  
- **Returns:** None  

#### `update_paragraph_highlight(typed_count)`
- **Description:** Highlights correct/incorrect characters in sample text.  
- **Parameters:** `typed_count` (int)  
- **Returns:** None  

#### `pause_time()`
- **Description:** Pauses/resumes timer and disables/enables typing.  
- **Parameters:** None  
- **Returns:** None  

#### `start_timer(event=None)`
- **Description:** Starts or continues the elapsed time counter.  
- **Parameters:** `event` (optional)  
- **Returns:** None  

#### `score_card()`
- **Description:** Displays accuracy, time taken, and WPM stats.  
- **Parameters:** None  
- **Returns:** None  

#### `update_score()`
- **Description:** Increases score when correct key is pressed.  
- **Parameters:** None  
- **Returns:** None  

#### `reduce_score(event=None)`
- **Description:** Decreases score when backspace is pressed.  
- **Parameters:** `event` (optional)  
- **Returns:** None  

#### `reset_game()`
- **Description:** Resets all game state, UI labels, and keyboard visuals.  
- **Parameters:** None  
- **Returns:** None  

---

## Function: `main()`
```python
def main():
    instance.insert_keys()
    instance.root.mainloop()
```
- **Description:** Entry point of the application. Builds the keyboard layout and starts the Tkinter event loop.  
- **Parameters:** None  
- **Returns:** None  

---

## 📄 Requirements

Dependencies required to run the application:

```txt
pygame==2.5.2
numpy==1.26.4
pillow==10.3.0
# tkinter is included with Python on most systems
```

---

## 📑 Notes
- `paragraph` is a list of sample texts used for typing practice.  
- Sounds are generated dynamically using `numpy` and `pygame`.  
- GUI is built with **Tkinter** and styled with custom assets.  

---
```