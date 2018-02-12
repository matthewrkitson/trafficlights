#!/usr/bin/python3

import os

from flipflop import WSGIServer
# from werkzeug.contrib.fixers import CGIRootFix
from trafficlights import app

if __name__ == '__main__':
    # This may help fix routing bugs if we host at the root of the website. 
    # app.wsgi_app = CGIRootFix(app.wsgi_app)
    WSGIServer(app).run()

