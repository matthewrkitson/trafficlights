#!/usr/bin/python3

import time
from gpiozero import LED

# LED pinout for floorplan unit
leds = [10, 22, 27, 17, 4, 3, 2, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21, 26, 19, 13, 6]

rooms = { 
	'u1': (LED(leds[0]), LED(leds[1])),
	'u2': (LED(leds[2]), LED(leds[3])),
	'u3': (LED(leds[4]), LED(leds[5])),
	'u4': (LED(leds[6]), LED(leds[7])),
	'u5': (LED(leds[8]), LED(leds[9])),
	'u6': (LED(leds[10]), LED(leds[11])),
	'd1': (LED(leds[12]), LED(leds[13])),
	'd2': (LED(leds[14]), LED(leds[15])),
	'd3': (LED(leds[16]), LED(leds[17])),
	'd4': (LED(leds[18]), LED(leds[19])),
	'd5': (LED(leds[20]), LED(leds[21])),
	'd6': (LED(leds[22]), LED(leds[23]))
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

while True:
	for room in rooms:
		green(rooms[room])
		time.sleep(1)
		red(rooms[room])
		time.sleep(1)
		off(rooms[room])

