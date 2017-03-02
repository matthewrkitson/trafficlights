from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import os
 
try: 
   reds = [8, 7, 1, 12, 16]
   greens = [14, 15, 18, 23, 24]
   lights = greens + reds

   GPIO.setmode(GPIO.BCM)
   for light in lights:
     GPIO.setup(light, GPIO.OUT)
     GPIO.output(light, 0)
except:
    pass

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    for i in range(5):
        arg = 'pair' + str(i)
        if arg in request.args:
            value = request.args[arg]
            if value == 'red':
                GPIO.output(reds[i], 1)
                GPIO.output(greens[i], 0)
            if value == 'green':
                GPIO.output(reds[i], 0)
                GPIO.output(greens[i], 1)
            if value == 'off':
                GPIO.output(reds[i], 0)
                GPIO.output(greens[i], 0)

        if 'poweroff' in request.args:
            os.system('sudo poweroff')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

