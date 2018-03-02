#!/usr/bin/python3

import time
import urllib.request
import json
from gpiozero import LED

# LED pinout for floorplan unit
leds = [10, 22, 27, 17, 4, 3, 2, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21, 26, 19, 13, 6]

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

def green(pair):
	pair[0].off()
	pair[1].on()

def red(pair):
	pair[0].on()
	pair[1].off()

def orange(pair):
	pair[0].on()
	pair[1].on()

def off(pair):
	pair[0].off()
	pair[1].off()

def update_with_single_call():
	contents = urllib.request.urlopen("http://localhost:9000/api/meetingroom")
	jsontext = contents.read()
	results = json.loads(jsontext.decode("utf-8"))
	for result in results:
		room = result["room"]
		busy = result["busy"]
		print(room + " " + str(busy))
		if busy:
			red(rooms[room])
		else:
			green(rooms[room])
	time.sleep(1)

def update_with_multiple_calls():
	contents = urllib.request.urlopen("http://localhost:9000/api/meetingroom/" + room)
	jsontext = contents.read()
	print(jsontext)
	result = json.loads(jsontext.decode("utf8"))
	busy = result["busy"]
	print(room + " " + str(busy))
	if busy:
		red(rooms[room])
	else:
		green(rooms[room])


while True:
	try:
		update_with_single_call()

		# for room in rooms:
			# update_with_multiple_calls()
	except Exception as e:
		print(e)
