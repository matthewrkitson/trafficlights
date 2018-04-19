from gpiozero import LED
from config import get_config

def get_pinout():
    # Dictionary of pinouts of different hardware units. 
    # Order of pins is: U1 green, U1 red, U2 green, U2 red, ... U6 green, U6 red, D1 green, D1 red, etc...
    pinouts = {
        'blackbox': [10, 22, 27, 17, 4, 3, 2, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21, 26, 19, 13, 6],
        'floorplan': [22, 10, 17, 27, 3, 4, 14, 2, 18, 15, 24, 23, 8, 25, 1, 7, 16, 12, 21, 20, 19, 26, 6, 13]
    }

    config = get_config()
    return pinouts[config['pinout']]

def get_lights(initialise = True):
    leds = get_pinout()

    if (initialise):
        initial_value = False
    else:
        initial_value = None

    # A dictionary of light pairs. Key is row.column
    lights = {
        '0.0': (LED(leds[0], initial_value=initial_value), LED(leds[1], initial_value=initial_value)),
        '0.1': (LED(leds[2], initial_value=initial_value), LED(leds[3], initial_value=initial_value)),
        '0.2': (LED(leds[4], initial_value=initial_value), LED(leds[5], initial_value=initial_value)),
        '0.3': (LED(leds[6], initial_value=initial_value), LED(leds[7], initial_value=initial_value)),
        '0.4': (LED(leds[8], initial_value=initial_value), LED(leds[9], initial_value=initial_value)),
        '0.5': (LED(leds[10], initial_value=initial_value), LED(leds[11], initial_value=initial_value)),
        '1.0': (LED(leds[12], initial_value=initial_value), LED(leds[13], initial_value=initial_value)),
        '1.1': (LED(leds[14], initial_value=initial_value), LED(leds[15], initial_value=initial_value)),
        '1.2': (LED(leds[16], initial_value=initial_value), LED(leds[17], initial_value=initial_value)),
        '1.3': (LED(leds[18], initial_value=initial_value), LED(leds[19], initial_value=initial_value)),
        '1.4': (LED(leds[20], initial_value=initial_value), LED(leds[21], initial_value=initial_value)),
        '1.5': (LED(leds[22], initial_value=initial_value), LED(leds[23], initial_value=initial_value))
    }

    return lights

def green(pair):
        pair[0].on()
        pair[1].off()

def red(pair):
        pair[0].off()
        pair[1].on()

def on(pair):
        pair[0].on()
        pair[1].on()

def off(pair):
        pair[0].off()
        pair[1].off()

def all_on():
        for room in rooms:
                on(rooms[room])


