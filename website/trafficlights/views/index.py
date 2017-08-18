from trafficlights import app, lights
from flask import render_template, request
import trafficlights.controller as controller

@app.route('/')
def index():
    errors = []
    
    for i in range(lights.num_indicators):
        arg = 'pair' + str(i)
        if arg in request.args:
            value = request.args[arg]
            if value == 'red':
                lights.set_indicator(i, controller.Controller.RED)
            elif value == 'green':
                lights.set_indicator(i, controller.Controller.GREEN)
            elif value == 'off':    
                lights.set_indicator(i, controller.Controller.OFF)
            elif value == 'both':
                lights.set_indicator(i, controller.Controller.BOTH)
            else:
                errors.append('Unrecognised value specified for ' + arg + ': ' + value)
                
    for i in range(lights.num_buzzers):
        arg = 'buzzer' + str(i)
        if arg in request.args:
            value = request.args[arg]

            try:
                duration = int(value)
            except Exception as ex:
                errors.append('Unable to convert ' + value + ' to ms duration for ' + arg + ': ' + str(ex))

            lights.buzz(i, duration)

    return render_template('index.html', lights=lights, errors=errors)
