import time
from lights import get_lights
import curses

_row_offset = 1
_red = "red"
_green = "green"
_width = 9
_height = 3

def green_column(column): return column * _width + int((_width - len(_green)) / 2)
def green_row(row): return _row_offset + row * _height
def red_column(column): return column * _width + int((_width - len(_red)) / 2)
def red_row(row): return _row_offset + row * _height + 1

def main(stdscr):

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    lights = get_lights(initialise=False)

    while True:
        for row in range(2):
            for column in range(6):
                key = str(row) + "." + str(column)
                
                green_led = lights[key][0]
                row_index = green_row(row)
                column_index = green_column(column)
                if (green_led.is_lit): 
                    text = _green.upper()
                    color = curses.A_REVERSE | curses.color_pair(1)
                else:
                    text = _green.lower()
                    color = curses.color_pair(1)
                stdscr.addstr(row_index, column_index, text, color)

                red_led = lights[key][1]
                row_index = red_row(row)
                column_index = red_column(column)
                if (red_led.is_lit): 
                        text = _red.upper()
                        color = curses.A_REVERSE | curses.color_pair(2)
                else: 
                    text = _red.lower()
                    color = curses.color_pair(2)
                stdscr.addstr(row_index, column_index, text, color)

        stdscr.refresh()
        time.sleep(0.5)

curses.wrapper(main)
