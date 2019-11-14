from bottle import Bottle, route, request, template, static_file, run
from datetime import datetime
import os

app = Bottle()

@app.get('/upload')
def up_home():
    return template('upload.tpl')

@app.post('/upload')
def do_upload():
    upload = request.files.get('upload')
    save_path = "./files"
    blobname = datetime.now().isoformat() + ".blob"
    # blobname = "fred"
    file_path = "{path}/{file}".format(path=save_path, file=blobname)
    print(file_path)
    upload.save(file_path, overwrite=True)
    return "File successfully saved to '{0}'.".format(save_path)

@app.get('/download')
def down_home():
    return template('download_static.tpl')

@app.post('/download')
def do_download():
    isoname = request.forms.get('isofile')
    filedir = os.getcwd() + '/files'
    return static_file(isoname, root=filedir, download='201910-oct-monthly-kpwoodham.pdf')

app.run(host='localhost', port=8082, debug=True, reload=True)