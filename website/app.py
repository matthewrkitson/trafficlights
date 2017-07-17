from flask import Flask, render_template, request
import controller
import os

app = Flask(__name__)
app.debug = True
app.use_debugger = True
app.use_reloader = True

lights = controller.Controller(controller.FULLSIZE_V1)

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
                lights.buzz(i, duration)
            except:
                errors.append('Unable to convert ' + value + ' to ms duration for ' + arg)

    return render_template('index.html', lights=lights, errors=errors)

@app.route('/admin')
def admin():
    if 'poweroff' in request.args:
      os.system('sudo poweroff')

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

