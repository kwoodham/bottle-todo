import sqlite3
import datetime
from bottle import Bottle, route, run, debug, template, request, static_file, error
import os
import json

# Some front end functions

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


def filter_list():
    task_string = request.forms.get('task_string').strip()
    project = request.forms.get('project').strip()
    tag = request.forms.get('tag').strip()
    state = request.forms.get('state').strip()
    if project == '': 
        project = 'all'
    if tag == '': 
        tag = 'all'
    if state == '': 
        state = 'all'

    return todo_list(tstr=task_string, proj=project, tag=tag, state=state)


def display_raw(no):
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

    return template('view_raw', old=cur_data, 
        old_status=cur_status, no=no, projects=get_projects(), 
        states=get_states(), notes=ledger_data, attachments=attach_data)


def display_item_edit(no):
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

    return template('edit_task', old=cur_data, 
        old_status=cur_status, no=no, projects=get_projects(), 
        states=get_states(), notes=ledger_data, attachments=attach_data)


# This is the same view as edit with all edit buttons removed
# It also provides access to open and closed item lists
def display_item_view(no):
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

    return template('view_task', old=cur_data, 
        old_status=cur_status, no=no, projects=get_projects(), 
        states=get_states(), notes=ledger_data, attachments=attach_data)


# Processes selections from edit_task template through display_item_edit() 
def edit_item(no): 
    if request.forms.get('cancel'):
        return todo_list(tstr='', proj='all', tag='all', state='all')

    elif request.forms.get('new_note'):
        return new_note(no=int(request.forms.get('task_number')))

    elif request.forms.get('new_file'):
        return new_file(no=int(request.forms.get('task_number')))

    elif request.forms.get('edit_note'):
        return edit_note(no=int(request.forms.get('note_number')))

    elif request.forms.get('save'):
        return save_task(no=int(request.forms.get('task_number')))

    elif request.forms.get('delete'):
        return delete_task(no=int(request.forms.get('task_number')))

    else:
        return display_item_edit(no=no)


# Processes confirmation from "del_task" template
def delete_task(no):
    if request.forms.get('confirm_cancel'):
        return display_item_edit(no=no)

    elif request.forms.get('confirm_delete'):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET status = ?, state = ? WHERE id LIKE ?;", (0, "DELETED", no,))

        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, "CLOSED - DELETED")"""
        arg = (no, datetime.datetime.now().isoformat())
        c.execute(sql, arg)

        conn.commit()
        c.close()

        return todo_list(tstr='', proj='all', tag='all', state='all')

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (no,))
        task_text = c.fetchone()
        c.close()

        return template('del_task.tpl', task=task_text, no=no)


def save_task(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # get previous information about the task so that I can record what's changed in the ledger
    c.execute( """SELECT * FROM TODO WHERE id LIKE ?""",(no,) )
    a = c.fetchone()
    old_task = a[1].strip() 
    old_status = a[2]
    old_project = a[3].strip()
    old_tag = a[4].strip()
    old_state = a[5].strip()
    old_date_due = a[6].strip()

    # get the new information from the form:
    task = request.forms.get('task').strip()
    status = request.forms.get('status')
    project = request.forms.get('project').strip()
    tag = request.forms.get('tag').strip()
    state = request.forms.get('state').strip()
    date_due = request.forms.get('date_due').strip()
    if date_due == '':
        date_due = '2000-01-01'

    if status == 'open':
        status = 1
    else:
        status = 0

    # Update the todo table
    sql = """UPDATE todo 
        SET task = ?, status = ?, project = ?, tag = ?, state = ?, date_due = ?
        WHERE id LIKE ?"""
    c.execute(sql, (task, status, project, tag, state, date_due, no))

    # Set up the ledger text to append to the history entry (don't use elif in order
    # to catch changes in more than one field at a time)
    ledger_text = " | "
    if old_task != task:
        ledger_text += "task:" + old_task + "-->" + task + "; "
    if old_status != status:
        ledger_text += "status:" + str(old_status) + "-->" + str(status) + "; "
    if old_project != project:
        ledger_text += "project:" + old_project + "-->" + project + "; "
    if old_tag != tag:
        ledger_text += "tag:" + old_tag + "-->" + tag + "; "
    if old_state != state:
        ledger_text += "state:" + old_state + "-->" + state + "; "
    if old_date_due != date_due:
        ledger_text += "date_due:" + old_date_due + "-->" + date_due + "; "

    # 12/27/2019 - Only record save if something has changed
    if ledger_text != " | ":

        # Write out the ledger for closed or edited (but not closed) tasks
        if status == 0:
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
            arg = (no, datetime.datetime.now().isoformat(), "CLOSED - " + state + ledger_text)
        else:
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
            arg = (no, datetime.datetime.now().isoformat(), "EDITED - " + state + ledger_text)
        c.execute(sql, arg)
        
    conn.commit()
    c.close()

    return display_item_edit(no=no)


# Handles attaching a new file through new_file template
# supports display_item_edit()
def new_file(no):
    if request.forms.get('cancel'):
        return display_item_edit(no=no)

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

        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
        arg = (no, datetime.datetime.now().isoformat(), "EDITED - attach file: " + upload.filename)
        c.execute(sql, arg)

        conn.commit()
        c.close()

        return display_item_edit(no=no)

    else:
        return template('new_file.tpl', no=no)


# Processes file download directly and passes delete confirmation through 
# to del_file template and del_file() routine (below)
# Supports display_item_edit()
def edit_file():
    no = int(request.forms.get('number'))
    filedir = os.getcwd() + '/files'

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT id, task_id, isoname, filename, filetype FROM attach WHERE id==?"""
    c.execute(sql, (no,))
    a = c.fetchone()
    file_id  = a[0]
    task_id  = a[1]
    isoname  = a[2]
    filename = a[3]
    filetype = a[4]

    if request.forms.get('download'):
        return static_file(isoname, root=filedir, download=filename, mimetype=filetype)

    elif request.forms.get('delete'):
       return template('del_file.tpl', 
        file_id=file_id, task_id=task_id, 
        filename=filename, isoname=isoname, filetype=filetype)

    else:
        return display_item_edit(no=task_id)

# Processes delete file confirmation: cancel and delete through del_file template
# Supports edit_file()
def del_file():
    task_id  = request.forms.get('task_id')
    file_id  = request.forms.get('file_id')
    filename = request.forms.get('filename')
    isoname  = request.forms.get('isoname')
    filetype = request.forms.get('filetype')

    if request.forms.get('confirm_cancel'):
        return display_item_edit(no=task_id)

    elif request.forms.get('confirm_delete'):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        filedir = os.getcwd() + '/files'
        c.execute("DELETE FROM attach WHERE id==?;", (file_id,))
        file_path = "{path}/{file}".format(path=filedir, file=isoname)
        os.remove(file_path)

        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
        arg = (task_id, datetime.datetime.now().isoformat(), "EDITED - remove file: " + filename)
        c.execute(sql, arg)
        conn.commit()
        c.close()
        return display_item_edit(no=task_id)
    
    else:
        return template('del_file.tpl', file_id=file_id, task_id=task_id, filename=filename, filetype=filetype)


def closed_list(tstr, proj, tag, state):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    sql = """SELECT id, task, project, tag, state, date_due 
          FROM todo WHERE todo.status LIKE '0'"""

    # see https://www.tutorialspoint.com/python/python_tuples.htm 
    arg = ()
    if (tstr != "all") and (tstr != ""):
        sql += " AND task LIKE ?"
        arg += ("%" + tstr + "%",)
    if proj != "all":
        sql += " AND project LIKE ?"
        arg += (proj,)
    if tag != "all":
        sql += " AND tag LIKE ?"
        arg += (tag,)
    if state != "all":
        sql += " AND state LIKE ?"
        arg += (state,)

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


def todo_list(tstr, proj, tag, state):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    sql = """SELECT id, task, project, tag, state, date_due FROM todo WHERE todo.status LIKE '1'"""

    # see https://www.tutorialspoint.com/python/python_tuples.htm 
    arg = ()
    if (tstr != "all") and (tstr != "") and (tstr != "search text"):
        sql += " AND task LIKE ?"
        arg += ("%" + tstr + "%",) # This adds a wildcard before and after the string
    if proj != "all":
        sql += " AND project LIKE ?"
        arg += (proj,)
    if tag != "all":
        sql += " AND tag LIKE ?"
        arg += (tag,)
    if state == "!dormant":
        sql += " AND state NOT LIKE ?"
        arg += ('dormant', )
    elif state != "all":
        sql += " AND state LIKE ?"
        arg += (state,)

    sql += " ORDER BY date_due ASC;"

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

    return template('make_table', rows=result, states=get_states(), projects=get_projects())

def json_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT id FROM todo WHERE todo.status LIKE '1' ORDER BY todo.date_due ASC;"""
    c.execute(sql)      
    result = c.fetchall()

    out_table = []

    for row in result:
        c.execute("SELECT * FROM todo WHERE id LIKE ?", (row[0],))
        result = c.fetchone()
        names = [description[0] for description in c.description]

        out = {}
        for i in range(len(names)):
            out[names[i]] = result[i]
        out_table.append(json.dumps(out))
    c.close()

    return template('make_json_table.tpl', rows=out_table)

# https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
# https://stackoverflow.com/questions/23110383/how-to-dynamically-build-a-json-object-with-python
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


def new_item():
    if request.forms.get('cancel'):
        return todo_list(tstr='', proj='all', tag='all', state='all')

    elif request.forms.get('save'):
        task = request.forms.get('task').strip()
        if task == '':
            task = "blank"
        project = request.forms.get('project').strip()
        if project == '':
            project = "unassigned"
        tag = request.forms.get('tag').strip()
        state = request.forms.get('state').strip()
        if state == '':
            state = 'dormant'
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

        return todo_list(tstr='', proj='all', tag='all', state='all')

    else:
        return template('new_task.tpl', projects=get_projects(), states=get_states())


def new_note(no):
    if request.forms.get('cancel'):
        return display_item_edit(no=no)

    elif request.forms.get('save'):  
        note = request.forms.get('note').strip()
        if note != '': # 2/7/2020: Don't save an empty note
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()

            sql = """INSERT INTO 'notes' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, ?)"""
            arg = (no, datetime.datetime.now().isoformat(), note)
            c.execute(sql, arg)
            conn.commit()
            c.close()

        return display_item_edit(no=no)

    else:
        return template('new_note.tpl', no=no)


def edit_note(no):
    if request.forms.get('cancel'):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task_id FROM notes WHERE id==?", (no,))
        result = c.fetchone()
        c.close()

        return display_item_edit(no=int(result[0]))

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

        return display_item_edit(no=task_id[0])

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("SELECT ledger FROM notes WHERE id==?", (no,))
        note = c.fetchone()

        conn.commit()
        c.close()

        return template('edit_note.tpl', no=no, note=note)


def history_all():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT todo.id, todo.project, todo.task, history.entry_date AS entry_date, history.ledger 
            FROM todo INNER JOIN history WHERE todo.id LIKE history.task_id
            UNION
            SELECT todo.id, todo.project, todo.task, notes.entry_date AS entry_date, notes.ledger
            FROM todo INNER JOIN notes WHERE todo.id LIKE notes.task_id 
            ORDER by entry_date DESC;"""

    c.execute(sql)      
    results = c.fetchall()
    c.close()
    return template('history_table', results=results)


def history_after(start):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT todo.id, todo.project, todo.task, history.entry_date AS entry_date, history.ledger 
            FROM todo INNER JOIN history 
            WHERE ( todo.id LIKE history.task_id ) AND ( entry_date >= ? )
            UNION
            SELECT todo.id, todo.project, todo.task, notes.entry_date AS entry_date, notes.ledger
            FROM todo INNER JOIN notes 
            WHERE ( todo.id LIKE notes.task_id ) AND ( entry_date >= ? )
            ORDER by entry_date DESC;"""
    
    arg = (start, start,)

    c.execute(sql, arg)      
    results = c.fetchall()
    c.close()
    return template('history_table', results=results)


def history_between(start,end):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    sql = """SELECT todo.id, todo.project, todo.task, history.entry_date AS entry_date, history.ledger 
            FROM todo INNER JOIN history 
            WHERE ( todo.id LIKE history.task_id ) AND ( entry_date BETWEEN ? AND ? )
            UNION
            SELECT todo.id, todo.project, todo.task, notes.entry_date AS entry_date, notes.ledger
            FROM todo INNER JOIN notes 
            WHERE ( todo.id LIKE notes.task_id ) AND ( entry_date BETWEEN ? AND ? )
            ORDER by entry_date DESC;"""
    
    arg = (start, end, start, end,)

    c.execute(sql, arg)      
    results = c.fetchall()
    c.close()
    return template('history_table', results=results)


## ===========================================
## DEFINE THE APP AND SUPPORTED URL CONSTRUCTS
## ===========================================

app = Bottle()


# Supports URL 
@app.get('/new')
def new_get():
    return new_item()


@app.get('/todo')
def todo_all():
    return todo_list(tstr='', proj='all', tag='all', state='all')


# Filtering active tasis via URL in task-string, project, tag, and state elements
@app.get('/todo/<tstr>')
def todo_tstr(tstr):
    return todo_list(tstr=tstr, proj='all', tag='all', state='all')


@app.get('/todo/<tstr>/<proj>')
def todo_proj(tstr, proj):
    return todo_list(tstr=tstr, proj=proj, tag='all', state='all')


@app.get('/todo/<tstr>/<proj>/<tag>')
def todo_proj_tag(tstr, proj, tag):
    return todo_list(tstr=tstr, proj=proj, tag=tag, state='all')


@app.get('/todo/<tstr>/<proj>/<tag>/<state>')
def todo_proj_tag_state(tstr, proj, tag, state):
    return todo_list(tstr=tstr, proj=proj, tag=tag, state=state)


# Filtering using callbacks from make_table template
@app.post('/filter')
def filter_list_post():
    return filter_list()


# Filtering closed tasks via URL in task-string, project, tag, and state elements
@app.get('/closed')
def closed_all():
    return closed_list(tstr='all', proj='all', tag='all', state='all')


@app.get('/closed/<tstr>')
def closed_tstr(tstr):
    return closed_list(tstr=tstr, proj='all', tag='all', state='all')


@app.get('/closed/<tstr>/<proj>')
def closed_proj(tstr, proj):
    return closed_list(tstr=tstr, proj=proj, tag='all', state='all')


@app.get('/closed/<tstr>/<proj>/<tag>')
def closed_proj_tag(tstr, proj, tag):
    return closed_list(tstr=tstr, proj=proj, tag=tag, state='all')


@app.get('/closed/<tstr>/<proj>/<tag>/<state>')
def closed_proj_tag_state():
    return closed_list(tstr=tstr, proj=proj, tag=tag, state=state)


# Entire list of open tasks in JSON tables
@app.get('/json')
def json_get():
    return json_list()


# Single JSON line for specific task
@app.get('/json/<item:re:[0-9]+>')
def show_json_get(item):
    return show_json(item=item)


# Supports viewing an item without editing controls
@app.get('/view/<no:int>')
def view_item_get(no):
    return display_item_view(no=no)


# raw text for pasting into markdown pages
@app.get('/raw/<no:int>')
def raw_item_get(no):
    return display_raw(no=no)


# Supports per-task "edit" buttons in make_table template
@app.get('/edit/<no:int>')
def edit_item_get(no):
    return display_item_edit(no=no)

## TASK AND NOTE CALLBACKS

# Callback to create a task from make_table template
@app.post('/new')
def new_post():
    return new_item()

# Callback to edit a task from edit_task template
@app.post('/edit/<no:int>')
def edit_item_post(no):
    return edit_item(no=no)

# Callback to delete task
@app.post('/del/<no:int>')
def del_item_post(no):
    return delete_task(no=no)

# Callback for new note
@app.post('/new_note/<no:int>')
def new_note_post(no):
    return new_note(no=no)

# Callback for editing a note (erasing text will delete)
@app.post('/edit_note/<no:int>')
def edit_note_post(no):
    return edit_note(no=no)


## FILE CALLBACKS

# Callback to create a new file
@app.post('/new_file/<no:int>')
def new_file_post(no):
    return new_file(no=no)

# Callback for file download and delete 
@app.post('/edit_file')
def edit_file_post():
    return edit_file()

# Callback to confirm file delete
@app.post('/del_file')
def del_file_post():
    return del_file()


# All history
@app.get('/history')
def history_all_get():
    return history_all()


# History after a given start date (inclusive)
@app.get('/history/<start>')
def history_after_get(start):
    return history_after(start=start)

# History between a start and end date (inclusive)
@app.get('/history/<start>/<end>')
def history_between_get(start,end):
    return history_between(start=start, end=end)


@app.get('/help')
def help():
    static_file('help.html', root='.')


#  Comes from page that showed how to reference css
@app.get('/static<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static')


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


## =========================================
# START THE WEBSERVER AND CROSS YOUR FINGERS
## =========================================


# app.run(host='localhost', port=8081, reloader=True, debug=True)
app.run(host='localhost', port=8080)
