#!/usr/bin/python3

import os

from flipflop import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()

