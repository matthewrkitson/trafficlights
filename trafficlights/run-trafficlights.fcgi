#!/usr/bin/python3

import os

from flipflop import WSGIServer
from app import app

#def myapp(env, start_response):
#    start_response('200 OK', [('Content-Type', 'text/plain')])
#    return ['python-fcgi: test\n']

if __name__ == '__main__':
    WSGIServer(app).run()

