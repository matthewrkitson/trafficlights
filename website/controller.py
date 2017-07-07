import RPi.GPIO as GPIO
import collections

class ControllerConfiguration:
    def __init__(self, greens, reds, buzzers, inputs):
        self.greens = greens[:]
        self.reds = reds[:]
        self.buzzers = buzzers[:]
        self.inputs = inputs[:]  

class Controller:

    RED = 'red'
    GREEN = 'green'
    OFF = 'off'
    BOTH = 'both'

    def __init__(self, configuration):
        self.greens = configuration.greens[:]
        self.reds = configuration.reds[:]
        self.buzzers = configuration.buzzers[:]
        self.inputs = configuration.inputs[:]

        if len(self.reds) != len(self.greens):
            raise ValueError('Green/red light mismatch; there are {0} green lights and {1} red lights specified'.format(len(self.greens), len(self.reds)))

        self.num_indicators = len(self.greens)

        outputs = self.reds + self.greens + self.buzzers
        inputs = self.inputs

        all_io = outputs + inputs

        seen = set()
        duplicates = set()
        for item in all_io:
            if item in seen:
                duplicates.add(item)
            seen.add(item)

        if duplicates:
            raise ValueError('The following GPIO pins have been assigned to more than one purpose: ' + str(duplicates))
 
        GPIO.setmode(GPIO.BCM)

        for output in outputs:
            GPIO.setup(output, GPIO.OUT)
            GPIO.output(output, GPIO.LOW)

        for ip in inputs:
            GPIO.setup(ip, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def set_indicator(self, index, state):
        if state == Controller.RED:
            GPIO.output(self.reds[index], GPIO.HIGH)
            GPIO.output(self.greens[index], GPIO.LOW)
        elif state == Controller.GREEN:
            GPIO.output(self.reds[index], GPIO.LOW)
            GPIO.output(self.greens[index], GPIO.HIGH)
        elif state == Controller.OFF:
            GPIO.output(self.reds[index], GPIO.LOW)
            GPIO.output(self.greens[index], GPIO.LOW)
        elif state == Controller.BOTH:
            GPIO.output(self.reds[index], GPIO.HIGH)
            GPIO.output(self.greens[index], GPIO.HIGH)


FULLSIZE_V1 = ControllerConfiguration(
    [27,  4,  2, 15, 23, 25,  7, 12, 20, 26, 13, 5],
    [17,  3, 14, 18, 24,  8,  1, 16, 21, 19,  6, 0],
    [22, 10],
    [11])

DESKTOP_V1 = ControllerConfiguration(
    [14, 15, 18, 23, 24],
    [ 8,  7,  1, 12, 16],
    [],
    [])
            

        

    
