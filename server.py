#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import uuid
from datetime import datetime

from config import Config
from common.Log import Logger 

import flask


# prepare
os.system("mkdir -p " + Config.logDir)

# set the logger
logger = Logger(Config.logDir + '/server.log', Config.logLevel, 'server')

app = flask.Flask(__name__, static_folder = "./dist/static", template_folder = "./dist")

# web
@app.route('/')
@app.route('/index')
def index():
    try:
        logger.info("request index")
        return flask.render_template("index.html")

    except Exception,ex:
        logger.error("index error:%s" %(ex))
        return "Hello, this is Media Paser."


if __name__ == "__main__":
    app.run('0.0.0.0', Config.servicePort, debug = True,  threaded = True)