#!/usr/bin/python3

import time
import urllib.request
import logging
import logging.handlers
import json
from gpiozero import LED, Button
from subprocess import check_call

# LED pinout for "black box" units
# Top row, green, red, green, red, then bottom row green, red, green, red, etc.
black_box_leds = [10, 22, 27, 17, 4, 3, 2, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21, 26, 19, 13, 6]

# LED pinout for "floorplan" unit
# U1 red, green, U2 red green, etc... then D1 red, green, D2 red, green, etc.
floorplan_leds = [22, 10, 17, 27, 3, 4, 14, 2, 18, 15, 24, 23, 8, 25, 1, 7, 16, 12, 21, 20, 19, 26, 6, 13]

# Choose the appropriate pinout here. 
leds = black_box_leds

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

def green(pair):
        pair[1].off()
        pair[0].on()

def red(pair):
        pair[1].on()
        pair[0].off()

def on(pair):
        pair[0].on()
        pair[1].on()

def off(pair):
        pair[0].off()
        pair[1].off()

def all_on():
        for room in rooms:
                on(rooms[room])

def format_room(room, busy):
        if busy:
                return "(*) " + room + "   "
        else:
                return "( ) " + room + "   "

def update_with_single_call():
        contents = urllib.request.urlopen("http://meeting-server:9000/api/meetingroom")
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

def update_with_multiple_calls():
        contents = urllib.request.urlopen("http://localhost:9000/api/meetingroom/" + room)
        jsontext = contents.read()
        print(jsontext)
        result = json.loads(jsontext.decode("utf8"))
        busy = result["busy"]
        logger.info(room + " " + str(busy))
        if busy:
                red(rooms[room])
        else:
                green(rooms[room])

logger = logging.getLogger('meetingrooms')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

fileHandler = logging.handlers.RotatingFileHandler('meetingrooms.log', maxBytes=1048576, backupCount=5)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

# StreamHandler defaults to stderr
consoleHandler = logging.StreamHandler()
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
                
while True:
        try:
                update_with_single_call()

                # for room in rooms:
                        # update_with_multiple_calls()
        except Exception as e:
                logger.error(str(e))

        time.sleep(5)

