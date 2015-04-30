
import logging

from parser import Parser
from bottle import route, run, template, error, static_file





class Server:
    def __init__(self, ip='localhost', port=9090 ,log_level=logging.DEBUG):
        # 

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
        @route('/api/get_mediainfo/:url')
        def get_mediainfo(url=None):
            if url == None:
                return '{"result":"error","message":"url error."}'

            return '{"result":"success"}'

        @route('/api/parse/:url')
        def parse_file(url=None):
            return "parse file: %s" %(url)



        # the 'host' need be modified to local ip address. 
        run(host='10.33.2.201', port=9090, debug=True)


if __name__ == "__main__":
    server = Server('10.33.2.201', 9090, logging.DEBUG)