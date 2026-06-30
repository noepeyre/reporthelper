# Project: Hotkey-Controlled Python UI Automation Tool

Create a standalone Python program that automates a repeated sequence of actions in a graphical application.

## General Behavior

When the program starts:

- The script remains completely inactive.
- No action is performed until the user opens the configuration menu and starts automation.

The script is controlled only through global keyboard shortcuts.

## Hotkeys

- **F8**: open the configuration menu.
- **F10**: start or stop automation immediately (Start/Stop toggle).
- **F9**: quit the program completely.

---

# Configurable Settings

Each time the F8 menu is opened, the following settings can be changed.

## 1. Target Slot

Choose a numbered slot from **1 to 10**.

This number is used to automatically calculate the vertical position of the first click.

---

## 2. Number of Context Menu Options

Possible values:

- 4
- 5

This setting indicates how many entries the context menu contains.

---

## 3. Option to Select

The user chooses which entry to select.

- If the menu has 4 options, choose between 1 and 4.
- If the menu has 5 options, choose between 1 and 5.

The script automatically calculates the vertical position of this option.

---

## 4. Loop Count

Number of repetitions.

Values:

- positive integer
- **0 = infinite**

---

# Loop Sequence

Each iteration performs exactly:

1. Move to the selected slot.
2. Click to open the context menu.
3. Move to the selected option.
4. Click.
5. Move to the confirmation button.
6. Click.
7. Repeat until the loop count is reached.

---

# Automatic Screen Adaptation

The script must work independently of:

- resolution;
- screen aspect ratio;
- Windows DPI scaling.

Coordinates are calculated automatically from references so the behavior remains identical across different configurations.

Mouse movement must never use hard-coded absolute coordinates.

---

# Performance

Goals:

- fastest possible execution;
- minimal delay between the three clicks;
- nearly instant movement.

---

# Ergonomics

- On startup, the script is completely inactive.
- F8 opens the configuration menu, only when the script is stopped.
- F10 starts or stops the loop immediately.
- F9 closes the program cleanly, even if a loop is running.

---

# Architecture

The project must be organized cleanly.

Separate the code into multiple modules:

- main file;
- configuration;
- coordinate calculation;
- hotkey handling;
- automation loop;
- click and movement functions.
