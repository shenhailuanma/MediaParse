
import logging
import os

from datetime import datetime
import time

#from parser import Parser
from bottle import route, run, template, error, static_file, default_app





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

        self.logger.info('init over.')

        # for test
        self.longtest_cnt = 0

    def run(self):
        #
        @route('/')
        @route('/index')
        def index():
            return "Hello, this is Media Paser."

        @route('/hello/<name>')
        def hello(name):
            return template('<b>Hello {{name}}</b>!', name=name)

        @route('/images/:filename')
        def send_image(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            return static_file(filename, root='/root/MediaParse/html/images')

        @route('/css/:filename')
        def send_css(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            return static_file(filename, root='/root/MediaParse/html/css')



        @error(404)
        def error404(error):
            #return "Nothing here, sorry."
            return static_file("404.html", "/root/MediaParse/html")



        ######################
        #API
        #################
        @route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())

        @route('/api/longtest')
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


        @route('/api/get_mediainfo/:url')
        def get_mediainfo(url=None):
            if url == None:
                return '{"result":"error","message":"url error."}'

            return '{"result":"success"}'

        ###   The task type, support: "parse", "transcode", "slice" ...
        ###   The API: create parse task
        @route('/api/create/task/parse', method="POST")
        def create_media_task():
            '''
                the post data format:
                {
                    "source": "xxx",  # the URL of the media, support FILE, HTTP, FTP
                    ""
                }
            '''
            return "create_media_task"



        # the 'host' need be modified to local ip address. 
        #run(host=self.ip, port=self.port, debug=True)



if __name__ == "__main__":
    server = Server('0.0.0.0', 9090, logging.DEBUG)
    server.run()
    run(host='0.0.0.0', port=9090, debug=True)
else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 9090, logging.DEBUG)
    server.run()
    application = default_app()