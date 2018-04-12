#!/usr/bin/python3

import time
import urllib.request
import json
from gpiozero import LED, Button
from subprocess import check_call

from log import logger
from lights import red, green, on, off, all_on

def get_config():
    # Read the configuration file (pinout.config)
    with open('meetingrooms.config') as json_file:
        config = json.load(json_file)

    return config

def get_pinout():
    # Dictionary of pinouts of different hardware units. 
    # Order of pins is: U1 green, U1 red, U2 green, U2 red, ... U6 green, U6 red, D1 green, D1 red, etc...
    pinouts = {
        'blackbox': [10, 22, 27, 17, 4, 3, 2, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21, 26, 19, 13, 6],
        'floorplan': [22, 10, 17, 27, 3, 4, 14, 2, 18, 15, 24, 23, 8, 25, 1, 7, 16, 12, 21, 20, 19, 26, 6, 13]
    }

    config = get_config()
    return pinouts[config['pinout']]

# Choose the appropriate pinout here. 
leds = get_pinout()

rooms = {
        'U1': (LED(leds[0]), LED(leds[1])),
        'U2': (LED(leds[2]), LED(leds[3])),
        'U3': (LED(leds[4]), LED(leds[5])),
        'U4': (LED(leds[6]), LED(leds[7])),
        'U5': (LED(leds[8]), LED(leds[9])),
        'U6': (LED(leds[10]), LED(leds[11])),
        'D1': (LED(leds[12]), LED(leds[13])),
        'D2': (LED(leds[14]), LED(leds[15])),
        'D3': (LED(leds[16]), LED(leds[17])),
        'D4': (LED(leds[18]), LED(leds[19])),
        'D5': (LED(leds[20]), LED(leds[21])),
        'D6': (LED(leds[22]), LED(leds[23]))
}

def poweroff():
        all_on()
        check_call(['sudo', 'poweroff'])

def reboot():
        all_on()
        check_call(['sudo', 'reboot'])

button = Button(5, hold_time=2)
button.when_held = poweroff
button.when_released = reboot

def format_room(room, busy):
    if busy:
        return "(*) " + room + "   "
    else:
        return "( ) " + room + "   "

def update_with_single_call():
    with urllib.request.urlopen("http://meeting-server:9000/api/meetingroom", timeout=20) as contents:
            jsontext = contents.read()
            results = json.loads(jsontext.decode("utf-8"))
            room_statuses = ""
            for result in results:
                    room = result["room"]
                    busy = result["busy"]
                    room_statuses += format_room(room, busy)
                    if busy:
                            red(rooms[room])
                    else:
                            green(rooms[room])
            logger.info(room_statuses)

               
while True:
    try:
        update_with_single_call()

    except Exception as e:
        logger.error(str(e))

    time.sleep(5)

