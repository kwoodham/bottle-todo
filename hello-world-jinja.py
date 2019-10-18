# Example bottle application for test
# use: 'localhost:8080/hello/world'
from bottle import route, run
from jinja2 import Template
@route('/hello/<name>')
def index(name):
    template=Template('<b>Hello {{name}}</b>!')
    return template.render(name=name)

run(host='localhost', port=8080)
