from trafficlights import app
from trafficlights import controller
from flask import render_template, request

@app.route('/<int:indicator>/teamcitywebhook', methods=['GET', 'POST'])
def teamcitywebhook(indicator):
    try:
        json = request.get_json()

        if json is None:
            return 'The body of the request must be a JSON object with a build.buildResults property that has a value of "running", "success", or "failure"'

        build = json['build']
        build_result = build['buildResult']

        if build_result == 'running':
            lights.set_indicator(indicator, controller.Controller.BOTH)
        elif build_result == 'success':
            lights.set_indicator(indicator, controller.Controller.GREEN)
        elif build_result == 'failure':
            lights.set_indicator(indicator, controller.Controller.RED)

        return build_result
    except Exception as ex:
        return str(ex), 500

