


from bottle import route, run, template

@route('/')
@route('/index')
def index():
    return "Hello, this is Media Paser."

@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/get_mediainfo/:url')
def get_mediainfo(url=None):
    if url == None:
        return '{"result":"error","message":"url error."}'

    return '{"result":"success"}'

@route('/parse/:url')
def parse_file(url=None)
    return "parse file: %s" %(url)

# the 'host' need be modified to local ip address. 
run(host='localhost', port=9090)
