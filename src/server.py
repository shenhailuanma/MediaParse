#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from datetime import datetime
import time

#from parser import Parser
import bottle




class Server:
    def __init__(self, ip='0.0.0.0', port=9090 ,log_level=logging.DEBUG):

        self.ip   = ip
        self.port = port

        # mark system start time
        self.system_initialized = datetime.now()


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

        self.logger.info('init over.')

        # for test
        self.longtest_cnt = 0

    
        #
        @bottle.route('/')
        @bottle.route('/index')
        def index():
            return "Hello, this is Media Paser."

        @bottle.route('/images/:filename')
        def send_image(filename=None):
            root_path = "%s/images" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)

        @bottle.route('/css/:filename')
        def send_css(filename=None):
            root_path = "%s/css" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)



        @bottle.error(404)
        def error404(error):
            #return "Nothing here, sorry."
            return bottle.static_file("404.html", "/root/MediaParse/html")



        ######################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())

        @bottle.route('/api/longtest')
        def longtest():
            cnt = self.longtest_cnt
            self.longtest_cnt += 1
            sleep_time = 0
            start = datetime.now()

            while True:
                self.logger.debug('Long test:%s, sleep_time:%s.' %(cnt, datetime.now() - start))
                time.sleep(1)
                sleep_time += 1
                if sleep_time > 10 :
                    break;


            return "%s" %(datetime.now())


        @bottle.route('/api/get_mediainfo/:url')
        def get_mediainfo(url=None):
            if url == None:
                return '{"result":"error","message":"url error."}'

            return '{"result":"success"}'

        ###   The task type, support: "parse", "transcode", "slice" ...
        ###   The API: create parse task
        @bottle.route('/api/create/task/parse', method="POST")
        def create_media_task():
            '''
                the post data format:
                {
                    "source": "xxx",  # the URL of the media, support FILE, HTTP, FTP
                    ""
                }

                response:
                {
                    "result" : "success",               # "success" or "error"
                    "message" : "create task ok.",      # string messages
                    "task_id" : 25                      # The task id
                }
            '''
            response = {}
            response['result'] = "success"
            response['message'] = "create task ok."
            response['task_id'] = -1

            # get the post data
            post_data = bottle.request.body.getvalue()
            self.logger.debug('create_media_task,handle the request post data: %s' %(post_data))

            post_data_json = json.loads(post_data)

            # check the params
            if not post_data_json.has_key('source'):
                response['result'] = "error"
                response['message'] = "params 'source' error."
                return json.dumps(response)

            # create the task
            create_task_params = {}
            create_task_params = post_data_json['source']
            

            return "create_media_task"



    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)



if __name__ == "__main__":
    server = Server('0.0.0.0', 9090, logging.DEBUG)
    server.run()
    run(host='0.0.0.0', port=9090, debug=True)
else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 9090, logging.DEBUG)
    server.run()
    application = bottle.default_app()