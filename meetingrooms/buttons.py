from gpiozero import Button
from config import get_config

buttons = None
def get_buttons():
    global buttons
    if buttons is not None:
        return buttons

    config = get_config("hardware")
    button_pins = config['buttons']
    buttons = [Button(b, hold_time=2) for b in button_pins]
    return buttons

