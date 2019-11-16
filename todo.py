import sqlite3
import datetime
from bottle import Bottle, route, run, debug, template, request, static_file, error
import os
import json

def get_projects():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT name FROM projects ORDER BY name DESC")
    projects = c.fetchall()
    conn.commit()
    c.close()
    return projects

def get_states():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT name, color FROM states ORDER BY name ASC")
    states = c.fetchall()
    conn.commit()
    c.close()
    return states


def display_item(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todo WHERE todo.id==?", (no,))
    cur_data = c.fetchall()

    if cur_data[0][2] == 1:
        cur_status = 'open'
    else:
        cur_status = 'closed'

    sql = """SELECT id, task_id, entry_date, ledger FROM history WHERE task_id==?
        UNION
        SELECT id, task_id, entry_date, ledger FROM notes WHERE task_id==?
        ORDER BY entry_date DESC;"""

    c.execute(sql,(no,no,))
    ledger_data = c.fetchall()

    sql = """SELECT id, task_id, entry_date, filename, 
        description, filesize, filetype FROM attach WHERE task_id==?
        ORDER BY entry_date DESC;"""

    c.execute(sql,(no,))
    attach_data = c.fetchall()

    conn.commit()
    c.close()       

    if cur_status=='open':

        return template('edit_task', old=cur_data, 
            old_status=cur_status, no=no, projects=get_projects(), 
            states=get_states(), notes=ledger_data, attachments=attach_data)

    else:

        return template('view_task', old=cur_data, 
            old_status=cur_status, no=no, projects=get_projects(), 
            states=get_states(), notes=ledger_data, attachments=attach_data)


app = Bottle()


@app.get('/closed')
def closed_all():
        return closed_list(proj='all', tag='all', state='all')


@app.get('/closed/<proj>/<tag>/<state>')
def closed_list(proj, tag, state):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    sql = """SELECT id, task, project, tag, state, date_due 
          FROM todo WHERE todo.status LIKE '0'"""

    # see https://www.tutorialspoint.com/python/python_tuples.htm 
    arg = ()
    if proj != "all":
        sql = sql + " AND project LIKE ?"
        arg = arg + (proj,)
    if tag != "all":
        sql = sql + " AND tag LIKE ?"
        arg = arg + (tag,)
    if state != "all":
        sql = sql + " AND state LIKE ?"
        arg = arg + (state,)

    c.execute(sql, arg)      
    result = c.fetchall()

    sql = """SELECT task_id, entry_date 
          FROM history WHERE task_id==? AND ledger LIKE 'CLOSED%'"""

    i = 0
    for row in result:
        arg = (row[0],)
        c.execute(sql,arg)
        a = c.fetchone()
        result[i] = result[i] + (a[1],)
        i = i+1

    conn.commit()
    c.close()

    # I can't use ORDERBY in sql because I don't have the right field to index
    # until the closed dates are appended to each list item, and that doesn 't
    # happen until the second sql where I match things up using the task id.

    # Get a list of the "closed" dates in the order they appear in result list
    a = [result[i][6] for i in range(len(result))]

    # Get the sorted index that the result list needs to be reindexed to 
    # https://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list
    sort_index = sorted(range(len(a)), key=lambda k: a[k], reverse=True)

    # Apply the sort index to the result table
    # https://stackoverflow.com/questions/2177590/how-can-i-reorder-a-list
    result = [result[i] for i in sort_index]

    return template('make_table_closed', rows=result)


@app.get('/todo')
def todo_all():
        return todo_list(proj='all', tag='all', state='all')


@app.post('/filter')
def todo_filter():
    project = request.forms.get('project').strip()
    tag = request.forms.get('tag').strip()
    state = request.forms.get('state').strip()
    if project == '': 
        project = 'all'
    if tag == '': 
        tag = 'all'
    if state == '': 
        state = 'all'

    return todo_list(proj=project, tag=tag, state=state)


@app.get('/todo/<proj>/<tag>/<state>')
def todo_list(proj, tag, state):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    sql = """SELECT id, task, project, tag, state, date_due FROM todo WHERE todo.status LIKE '1'"""

    # see https://www.tutorialspoint.com/python/python_tuples.htm 
    arg = ()
    if proj != "all":
        sql = sql + " AND project LIKE ?"
        arg = arg + (proj,)
    if tag != "all":
        sql = sql + " AND tag LIKE ?"
        arg = arg + (tag,)
    if state != "all":
        sql = sql + " AND state LIKE ?"
        arg = arg + (state,)

    c.execute(sql, arg)      
    result = c.fetchall()

    sql = """SELECT task_id, entry_date FROM history WHERE task_id==? and ledger LIKE 'OPENED%'"""

    i = 0
    for row in result:
        arg = (row[0],)
        c.execute(sql,arg)
        a = c.fetchone()
        result[i] = result[i] + (a[1],)
        i = i+1

    c.close()

    return template('make_table', rows=result, states=get_states())


@app.post('/new')
def new_item():
    if request.forms.get('cancel'):
        return todo_list(proj='all', tag='all', state='all')

    elif request.forms.get('save'):
        task = request.forms.get('task').strip()
        project = request.forms.get('project').strip()
        tag = request.forms.get('tag').strip()
        state = request.forms.get('state').strip()
        date_in = datetime.datetime.now().isoformat()
        date_due = request.forms.get('date_due').strip()
        if date_due == '':
            date_due = '2000-01-01'

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        sql = """INSERT INTO 'todo' 
               ('task', 'status', 'project', 'tag','state', 'date_due') 
               VALUES (?,1,?,?,?,?);"""
        arg = (task, project, tag, state, date_due)
        c.execute(sql, arg)
        new_id = c.lastrowid

        # Update the history table
        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger')
                VALUES (?, ?, ?)"""
        arg = (new_id, date_in, "OPENED - " + state)
        c.execute(sql, arg)

        conn.commit()
        c.close()

        return todo_list(proj='all', tag='all', state='all')

    else:
        return template('new_task.tpl', projects=get_projects(), states=get_states())


@app.get('/del/<no:int>')
def del_item(no):
    if request.GET.confirm_cancel:
        return todo_list(proj='all', tag='all', state='all')

    elif request.GET.confirm_delete:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET status = ?, state = ? WHERE id LIKE ?;", (0, "DELETED", no,))

        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, "CLOSED - DELETED")"""
        arg = (no, datetime.datetime.now().isoformat())
        c.execute(sql, arg)

        conn.commit()
        c.close()

        return todo_list(proj='all', tag='all', state='all')

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (no,))
        task_text = c.fetchone()
        c.close()

        return template('del_task.tpl', task=task_text, no=no)

# Support synonyms for edit: view, modify...
@app.get('/view/<no:int>')
def view_item(no):
    return display_item(no=no)

@app.get('/modify/<no:int>')
def modify_item(no):
    return display_item(no=no)

@app.get('/edit/<no:int>')
def edit_item_get_url(no):
    return display_item(no=no)

@app.get('/edit')
def edit_item_get_form():
    no = request.GET.number.strip()
    return display_item(no=no)

@app.post('/edit/<no:int>')
def edit_item(no):   
    if request.forms.get('cancel'):
        return todo_list(proj='all', tag='all', state='all')

    if request.forms.get('top'):
        return todo_list(proj='all', tag='all', state='all')

    elif request.forms.get('new_note'):
        return new_note(no=int(request.forms.get('task_number')))

    elif request.forms.get('new_file'):
        return new_file(no=int(request.forms.get('task_number')))

    elif request.forms.get('edit_note'):
        return edit_note(no=int(request.forms.get('note_number')))

    elif request.forms.get('save'):
        task = request.forms.get('task')
        status = request.forms.get('status')
        project = request.forms.get('project')
        tag = request.forms.get('tag')
        state = request.forms.get('state')
        date_due = request.forms.get('date_due')
        if date_due == '':
            date_due = '2000-01-01'

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        sql = """UPDATE todo 
            SET task = ?, status = ?, project = ?, tag = ?, state = ?, date_due = ?
            WHERE id LIKE ?"""
        c.execute(sql, (task, status, project, tag, state, date_due, no))

        if status == 0:
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
            arg = (no, datetime.datetime.now().isoformat(), "CLOSED - " + state)

        else:
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
            arg = (no, datetime.datetime.now().isoformat(), "EDITED - " + state)

        c.execute(sql, arg)
        conn.commit()
        c.close()

        return display_item(no=no)

    elif request.forms.get('delete'):
        return del_item(no=int(request.forms.get('task_number')))

    else:
        return display_item(no=no)

@app.post('/new_note/<no:int>')
def new_note(no):
    if request.forms.get('cancel'):
        return display_item(no=no)

    elif request.forms.get('save'):  
        note = request.forms.get('note').strip()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        sql = """INSERT INTO 'notes' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
        arg = (no, datetime.datetime.now().isoformat(), note)
        c.execute(sql, arg)
        conn.commit()
        c.close()

        return display_item(no=no)

    else:
        return template('new_note', no=no)



@app.get('/edit_note')
def edit_from_table():
    if request.GET.edit_note:
        number = int(request.GET.note_number.strip())
        return edit_note(number)


@app.post('/edit_note/<no:int>')
def edit_note(no):
    if request.forms.get('cancel'):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task_id FROM notes WHERE id==?", (no,))
        result = c.fetchone()
        c.close()

        return display_item(no=int(result[0]))

    elif request.forms.get('save'):
        note = request.forms.get('note').strip()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("UPDATE notes SET ledger = ? WHERE id==?", (note, no,))
        c.execute("SELECT task_id FROM notes WHERE id==?", (no,))
        task_id = c.fetchone()

        if note == "":
            c.execute("DELETE FROM notes WHERE id==?;", (no,))
            
        conn.commit()
        c.close()

        return display_item(no=task_id[0])

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("SELECT ledger FROM notes WHERE id==?", (no,))
        note = c.fetchone()

        conn.commit()
        c.close()
        return template('edit_note', no=no, note=note)


@app.post('/new_file/<no:int>')
def new_file(no):

    if request.forms.get('cancel'):
        return display_item(no=no)

    elif request.forms.get('submit'):  
        upload = request.files.get('upload')
        save_path = filedir = os.getcwd() + '/files'
        entry_date = datetime.datetime.now().isoformat()
        isoname = entry_date.replace(':','-')
        file_path = "{path}/{file}".format(path=save_path, file=isoname)
        upload.save(file_path, overwrite=True)

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        description = request.forms.get('description')
        filesize = upload.file.seek(0, 2)
        upload.file.seek(0, 0)

        sql = """INSERT INTO 'attach' ('task_id', 'entry_date', 'filename', 
                 'description', 'filesize', 'filetype', 'isoname') VALUES (?, ?, ?, ?, ?, ?,?)"""
        arg = (no, entry_date, upload.filename, description, filesize, upload.content_type, isoname)
        c.execute(sql, arg)
        conn.commit()
        c.close()

        return display_item(no=no)

    else:
        return template('new_file', no=no)


@app.post('/edit_file')
def edit_file():
    no = int(request.forms.get('number'))
    filedir = os.getcwd() + '/files'

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT id, isoname, filename, filetype FROM attach WHERE id==?"""
    c.execute(sql, (no,))
    a = c.fetchone()

    if request.forms.get('download'):
        return static_file(a[1], root=filedir, download=a[2], mimetype=a[3])

    # Need a confirmation in here...
    elif request.forms.get('delete'):
        c.execute("DELETE FROM attach WHERE id==?;", (no,))
        file_path = "{path}/{file}".format(path=filedir, file=a[1])
        os.remove(file_path)

    conn.commit()
    c.close()

    task_id = int(request.forms.get('task_id'))
    return display_item(no=task_id)


# From baseline example - need to extend to pull in notes and status table
@app.get('/item/<item:re:[0-9]+>')
def show_item(item):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchone()
    c.close()

    if not result:
        return 'This item number does not exist!'
    else:
        return 'Task: %s' % result[0]


@app.get('/help')
def help():
    static_file('help.html', root='.')


#  Comes from page that showed how to reference css
@app.get('/static<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static')


# https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
# https://stackoverflow.com/questions/23110383/how-to-dynamically-build-a-json-object-with-python
@app.get('/json/<item:re:[0-9]+>')
def show_json(item):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchone()
    names = [description[0] for description in c.description]
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        out = {}
        for i in range(len(names)):
            out[names[i]] = result[i]
        
        # Change 1/0 status to open/closed
        if out['status'] == 1:
            out['status'] = 'open'
        else:
            out['status'] = 'closed'

        json_out = json.dumps(out)
        return json_out # returning dumps() directly causes an error



@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

# app.run(host='localhost', port=8081, reloader=True, debug=True)
app.run(host='localhost', port=8080)
