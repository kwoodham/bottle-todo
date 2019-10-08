# Example bottle application for test
# use: 'localhost:8080/hello/world'
from bottle import route, run, template
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)