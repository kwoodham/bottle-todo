import sqlite3
import datetime
from bottle import Bottle, route, run, debug, template, request, static_file, error

app = Bottle()

@app.post('/upload')
def do_upload():

    upload = request.files.get('upload')
#   print(upload.filename)
#   print(upload.content_type)
#   print(upload.content_length)
#   upload.save(upload.filename, overwrite='True')

    conn = sqlite3.connect('blob.db')
    c = conn.cursor()

    sql = """INSERT INTO 'blob' ('name', 'type', 'file') VALUES (?,?,?);"""
    arg = (upload.filename, upload.content_type, upload.file.read(),)
    c.execute(sql, arg)

    conn.commit()
    c.close()

@app.get('/upload')
def home():
    return template('upload.tpl')

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


app.run(host='localhost', port=8080, debug=True)
