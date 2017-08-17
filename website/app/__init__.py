from flask import Flask, render_template, request
import controller
import poller
from teamcity_updater import TeamCityUpdater
from flash_updater import FlashUpdater
import os
import pwd
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

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

@app.route('/admin')
def admin():
    if 'poweroff' in request.args:
      poweroff()

    return render_template('admin.html')

@app.route('/logs')
def logs_get():
    log_file = log_file_path()
    with open(log_file, 'r') as content_file:
        content = content_file.read()
    return render_template('logs.html', content=content, logging=logging, logger=app.logger)
    
@app.route('/logs', methods=['POST'])
def logs_post():
    if 'clear' in request.form:
        file_handler.doRollover()
        
    if 'refresh' in request.form:
        # Do nothing, but we'll fall through to the standard render
        pass
        
    return logs_get()

@app.route('/teamcity', methods=['GET'])
def teamcity_get():
    return render_template('teamcity.html', config=teamcity_updater.get_config())

@app.route('/teamcity', methods=['POST'])
def teamcity_post(): 
    config = dict()
    config['baseurl'] = request.form['baseurl']
    config['username'] = request.form['username']
    config['password'] = request.form['password']

    build_types = [''] * lights.num_indicators
    for index in range(lights.num_indicators):
        build_types[index] = request.form['build_type_' + str(index)]
    config['build_types'] = build_types

    teamcity_updater.set_config(config)

    return teamcity_get()

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return exception, 500
    
def poweroff():
    for i in range(lights.num_indicators):
        lights.set_indicator(i, controller.Controller.BOTH)

    os.system('sudo poweroff')
    
def username():
    return pwd.getpwuid(os.geteuid()).pw_name

def log_file_path():
    return '/var/tmp/' + username() + 'trafficlights.log'
    

log_file = log_file_path()
file_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
    
app.logger.setLevel(logging.DEBUG)
app.logger.info('Starting traffiglights website')
app.logger.info('Running as user ' + username())

try:    
    lights = controller.Controller(controller.FULLSIZE_V1, app.logger)
    lights.add_input_response(0, poweroff)

    app.logger.info('Creating updaters')
    teamcity_updater = TeamCityUpdater(lights, app.logger)
    flash_updater = FlashUpdater(lights, app.logger, enable_lights=False)

    app.logger.debug('Starting poller')
    poller = poller.Poller(lights, [teamcity_updater, flash_updater], app.logger)
    poller.start()

except Exception as ex:
    app.logger.exception(ex)
    raise

