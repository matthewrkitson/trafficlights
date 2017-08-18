from trafficlights import app, lights, teamcity_updater
from flask import render_template, request

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
