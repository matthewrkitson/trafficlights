#!/usr/bin/python3

import time
import json
import urllib.request
from gpiozero import Button
from subprocess import check_call

from log import logger
from lights import get_lights, red, green, on, off, all_on

def poweroff():
        all_on()
        check_call(['sudo', 'poweroff'])

def reboot():
        all_on()
        check_call(['sudo', 'reboot'])

def format_room(room, busy):
    if busy:
        return "(*) " + room + "   "
    else:
        return "( ) " + room + "   "

def update_with_single_call(roomlights):
    with urllib.request.urlopen("http://meeting-server:9000/api/meetingroom", timeout=20) as contents:
            jsontext = contents.read()
            results = json.loads(jsontext.decode("utf-8"))
            room_statuses = ""
            for result in results:
                    room = result["room"]
                    busy = result["busy"]
                    room_statuses += format_room(room, busy)
                    if busy:
                            red(roomlights[room])
                    else:
                            green(roomlights[room])
            logger.info(room_statuses)



button = Button(5, hold_time=2)
button.when_held = poweroff
button.when_released = reboot

lights = get_lights()
roomlights = {
    'U1': lights['0.0'],
    'U2': lights['0.1'],          
    'U3': lights['0.2'],
    'U4': lights['0.3'],
    'U5': lights['0.4'],
    'U6': lights['0.5'],
    'D1': lights['1.0'],
    'D2': lights['1.1'],
    'D3': lights['1.2'],
    'D4': lights['1.3'],
    'D5': lights['1.4'],
    'D6': lights['1.5']
}

while True:
    try:
        update_with_single_call(roomlights)

    except Exception as e:
        logger.error(str(e))

    time.sleep(5)

