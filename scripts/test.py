#!/usr/bin/python3

import RPi.GPIO as GPIO
import time as time

reds = [8, 7, 1, 12, 16]
greens = [14, 15, 18, 23, 24]
lights = greens + reds

def main():
  try:
    setup()

    while True:
      for _ in range(5):
        flash()

      for _ in range(5):
        chase()

  finally:
    GPIO.cleanup()

def flash():
      all_on()
      time.sleep(0.5)
      all_off()
      time.sleep(0.5)

def all(state):
  for light in lights:
    GPIO.output(light, state)

def all_on(): all(1)
def all_off(): all(0)

def chase():
  pairs = zip(lights, rotate(lights, -1))
  for current, prev in pairs:
    GPIO.output(prev, 0)
    GPIO.output(current, 1)
    time.sleep(0.5)

def rotate(list, n):
  return list[n:] + list[:n]

def setup():
  GPIO.setmode(GPIO.BCM)
  for light in lights:
    GPIO.setup(light, GPIO.OUT)
    GPIO.output(light, 0)

if __name__ == '__main__':
  main()

