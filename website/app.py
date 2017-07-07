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
    for i in range(5):
        arg = 'pair' + str(i)
        if arg in request.args:
            value = request.args[arg]
            if value == 'red':
                lights.set_indicator(i, controller.RED)
            if value == 'green':
                lights.set_indicator(i, controller.GREEN)
            if value == 'off':    
                lights.set_indicator(i, controller.OFF)
            if value == 'both':
                lights.set_indicator(i, controller.BOTH)

    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'poweroff' in request.args:
      os.system('sudo poweroff')

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

