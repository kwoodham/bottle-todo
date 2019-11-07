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

#   From: https://docs.python.org/3/library/io.html
#   seek puts the stream position 0 bytes from the EOF (2)
#   tell reports the current stream position
#   print(upload.file.seek(0, 2))
#   print(upload.file.tell())

    # Put the stream position at the EOF to get the size, 
    # then reset to BOF for write into BLOB
    filesize = upload.file.seek(0, 2)
    upload.file.seek(0, 0)

    conn = sqlite3.connect('blob.db')
    c = conn.cursor()

    sql = """INSERT INTO 'blob' ('name', 'type', 'size', 'file') VALUES (?,?,?,?);"""
    arg = (upload.filename, upload.content_type, filesize, upload.file.read(),)
    c.execute(sql, arg)

    conn.commit()
    c.close()

    return template('upload_stats', name=upload.filename, filetype=upload.content_type, size=filesize)

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
