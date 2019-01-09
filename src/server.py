#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import json
import time
import uuid
from datetime import datetime

from common.Rqueue import Rqueue
from config import config
from common.Log import Logger

import flask

# set the logger
logger = Logger('/tmp/MediaParse_server.log', 'debug', 'server')


app = flask.Flask(__name__)

# web
@app.route('/')
@app.route('/index')
def index():
    try:
        #return "Hello, this is Media Paser."
        tasks_info_all = []
        # tasks_info_all = server.get_tasks_info_all()
        return flask.render_template('index.html', task_all = tasks_info_all)

    except Exception,ex:
        logger.error("index error:%s" %(ex))
        return "Hello, this is Media Paser."



if __name__ == "__main__":
    app.run('0.0.0.0', 9090, debug = True,  threaded = True)
