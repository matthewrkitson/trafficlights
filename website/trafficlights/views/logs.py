from trafficlights import app, log_file_path, file_handler
from flask import render_template, request
import logging

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
