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

import redis
import bottle
import flask


# set the logger
logger = Logger('/var/log/MediaParse_server.log', 'debug', 'server')



class Server:
    def __init__(self):
        self.task_queue = Rqueue(name='parse_task')
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_tasks_info_all(self):
        try:
            tasks_info_all = []
            tasks = self.redis.keys("parse_task:*")
            for task_one in tasks:
                task_info_one = None
                task_info_one = self.redis.hgetall(task_one)
                if task_info_one != None:
                    tasks_info_all.append(task_info_one)

            logger.debug("get_tasks_info_all len:%s" %(len(tasks_info_all)))
            return tasks_info_all
        except Exception,ex:
            logger.error("get_tasks_info_all error:%s" %(ex))
            return []

    def delete_task(self, task_id):
        try:
            tasks_info_all = []

        except Exception,ex:
            logger.error("delete_task error:%s" %(ex))




# get the server
server = Server()
app = flask.Flask(__name__)

@app.route('/api/gettime')
def gettime():
    return "%s" %(datetime.now())

@app.route('/')
@app.route('/index')
def index():
    #return "Hello, this is Media Paser."
    tasks_info_all = []
    tasks_info_all = server.get_tasks_info_all()
    return flask.render_template('index.html', task_all = tasks_info_all)



if __name__ == "__main__":
    app.run('0.0.0.0', 9090, debug = True,  threaded = True)



class Server_old:
    def __init__(self, ip='0.0.0.0', port=9090 ,log_level=logging.DEBUG):

        self.ip   = ip
        self.port = port

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'Server.log'

        self.logger = logging.getLogger('Server')
        self.logger.setLevel(self.log_level)

        # create a handler for write the log to file.
        fh = logging.FileHandler(self.log_path)
        fh.setLevel(self.log_level)

        # create a handler for print the log info on console.
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        # set the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


        self.file_path = os.path.realpath(__file__)
        self.dir_path  = os.path.dirname(self.file_path)

        # task queue
        self.task_queue = Rqueue(name='parse_task')
        self.redis = redis.Redis(host='localhost', port=6379, db=0)


        self.logger.info('init over.')

        # for test
        self.longtest_cnt = 0

    
        #
        @bottle.route('/')
        @bottle.route('/index')
        def index():
            return "Hello, this is Media Paser."

        ######################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())


        ###   The task type, support: "parse", "transcode", "slice" ...
        ###   The API: create parse task
        @bottle.route('/api/mediaparse/create', method="POST")
        def create_media_task():
            '''
                the post data format:
                {
                    "url": "xxx",  # the URL of the media, support FILE, HTTP, FTP
                    "name" : "media name"
                }

                response:
                {
                    "result" : "success",               # "success" or "error"
                    "message" : "create task ok.",      # string messages
                    "task_id" : 25                      # The task id
                }
            '''

            try:
                response = {}
                response['result'] = "success"
                response['message'] = "create task ok."
                response['task_id'] = -1

                # get the post data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('create_media_task,handle the request post data: %s' %(post_data))

                post_data_json = json.loads(post_data)

                # check the params
                if not post_data_json.has_key('url'):
                    response['result'] = "error"
                    response['message'] = "params 'url' error."
                    return json.dumps(response)

                if  post_data_json.has_key('name'):
                    post_data_json['name'] = post_data_json['name'].encode('utf-8')
                else:
                    post_data_json['name'] = 'default name'

                # generate id
                task_id = uuid.uuid1()
                self.logger.debug('generate task_id: %s' %(task_id))


                post_data_json['id'] = str(task_id)
                post_data_json['status'] = 'created'
                post_data_json['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                # push to task queue
                self.task_queue.push(task_id)
                self.redis.hmset("parse_task:%s" %(task_id), post_data_json)
                
                # test
                data = self.redis.hgetall("parse_task:%s" %(task_id))
                self.logger.debug('task data : %s' %(json.dumps(data)))

                response['task_id'] = str(task_id)
                return "%s" %(json.dumps(response))

            except Exception,ex:
                self.logger.error("create_media_task error:%s" %(ex))
                response['result'] = "error"
                response['message'] = str(ex)
                return json.dumps(response)


        @bottle.route('/api/mediaparse/status/:task_id')
        def get_mediaparse_task_status(task_id=None):
            try:
                response = {}
                response['result'] = "success"

                self.logger.debug('task_id: %s' %(task_id))
                data = self.redis.hgetall("parse_task:%s" %(task_id))
                self.logger.debug('task data : %s' %(json.dumps(data)))

                response['task'] = data

                return json.dumps(response)
            except Exception,ex:
                self.logger.error("get_mediaparse_task_status error:%s" %(ex))
                response['result'] = "error"
                response['message'] = str(ex)
                return json.dumps(response)

        @bottle.route('/api/mediaparse/delete/:task_id')
        def delete_mediaparse_task(task_id=None):
            try:
                response = {}
                response['result'] = "success"

                self.logger.debug('task_id: %s' %(task_id))
                data = self.redis.delete("parse_task:%s" %(task_id))

                return json.dumps(response)
            except Exception,ex:
                self.logger.error("delete_mediaparse_task error:%s" %(ex))
                response['result'] = "error"
                response['message'] = str(ex)
                return json.dumps(response)


    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)




