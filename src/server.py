


from bottle import route, run, template

@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)



run(host='localhost', port=9090)
