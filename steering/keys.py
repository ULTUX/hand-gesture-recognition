import threading
import time
import traceback

from pynput.keyboard import Controller, Key

from steering import config
from steering import icon
from steering import tray

keyMap = {
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "E": "e",
    "F": "f",
    "G": "g",
    "H": "h",
    "I": "i",
    "J": "j",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "O": "o",
    "P": "p",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "V": "v",
    "W": "w",
    "X": "x",
    "Y": "y",
    "Z": "z",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12,
    "L_CTRL": Key.ctrl_l,
    "R_CTRL": Key.ctrl_r,
    "L_ALT": Key.alt_l,
    "R_ALT": Key.alt_r,
    "L_SHIFT": Key.shift_l,
    "R_SHIFT": Key.shift_r,
    "SPACE": Key.space,
    "L_SUPER": Key.cmd_l,
    "R_SUPER": Key.cmd_r,
    "TAB": Key.tab,
    "BACKSPACE": Key.backspace,
    "PG_DOWN": Key.page_down,
    "PG_UP": Key.page_up,
    "DELETE": Key.delete,
    "END": Key.end,
    "HOME": Key.home,
    "INSERT": Key.insert,
    "ESC": Key.esc,
    "ARROW_LEFT": Key.left,
    "ARROW_RIGHT": Key.right,
    "ARROW_UP": Key.up,
    "ARROW_DOWN": Key.down,
    "PRINT_SCREEN": Key.print_screen
}

ignore_events = False


def set_ignore_events_to_false_after_delay():
    time.sleep(config.hold_time / 1000.0)
    set_ignore_events(False)


def set_ignore_events(value: bool):
    global ignore_events
    ignore_events = value
    try:
        if ignore_events:
            tray.tray_icon.icon = icon.red_circle
        else:
            tray.tray_icon.icon = icon.green_circle
    except:
        traceback.print_exc()
        print("Ignoring exception")


def press_keys(keys: str):
    global ignore_events
    if ignore_events:
        print("gesture ignored")
        # todo: delete this print (for debug only)
        return

    set_ignore_events(True)
    threading.Thread(target=set_ignore_events_to_false_after_delay).start()

    keyboard = Controller()
    keys_list = keys.split("+")

    press_keys_from_list(keyboard, keys_list)
    time.sleep(0.2)
    release_keys_from_list(keyboard, keys_list)


def release_keys_from_list(keyboard, keys_list):
    for key in reversed(keys_list):
        print(f'releasing {key}')
        # todo: delete print (for debugging only)
        keyboard.release(keyMap[key])


def press_keys_from_list(keyboard, keys_list):
    for key in keys_list:
        print(f'pressing {key}')
        # todo: delete print (for debugging only)
        keyboard.press(keyMap[key])
