import sqlite3
import datetime
from bottle import route, run, debug, template, request, static_file, error
import datetime

# URLs of form todo/project/tag/state
@route('/todo/<proj>/<tag>/<state>')
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

    sql = """SELECT task_id, entry_date FROM history WHERE task_id==? and ledger LIKE 'OPENED'"""

    i = 0
    for row in result:
        arg = (row[0],)
        c.execute(sql,arg)
        a = c.fetchone()
        result[i] = result[i] + (a[1],)
        i = i+1

    c.close()

    return template('make_table', rows=result)

# URLs /todo - return all
@route('/todo',  method='GET')
def todo_all():
        return todo_list(proj='all', tag='all', state='all')

# URLs of form /new, returns to /project/tag/state list
@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        project = request.GET.project.strip()
        tag = request.GET.tag.strip()
        state = request.GET.state.strip()
        date_in = datetime.datetime.now().isoformat()
        date_due = request.GET.date_due.strip()


        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        sql = """INSERT INTO 'todo' 
               ('task', 'status', 'project', 'tag','state', 'date_due') 
               VALUES (?,1,?,?,?,?);"""
        arg = (new, project, tag, state, date_due)
        c.execute(sql, arg)
        new_id = c.lastrowid

        # Update the history table
        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger')
                VALUES (?, ?,"OPENED")"""
        arg = (new_id, date_in)
        c.execute(sql, arg)

        conn.commit()
        c.close()

        return todo_list(proj='all', tag='all', state='all')

    else:
        return template('new_task.tpl')

# URLs /del/number, returns to /project/tag/state list
@route('/del/<no:int>', method='GET')
def del_item(no):

    if request.GET.delete:

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("DELETE FROM todo WHERE id LIKE ?;", (no,))

        sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, "DELETED")"""
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

# URLs /del - gets number from form, returns to /del/number
@route('/del',  method='GET')
def del_item_from_table():
    if request.GET.delete:
        number = request.GET.number.strip()
        return del_item(number)

# URLs /edit/number, returns to /project/tags/state
@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        task = request.GET.task.strip()
        status = request.GET.status.strip()
        project = request.GET.project.strip()
        tag = request.GET.tag.strip()
        state = request.GET.state.strip()
        date_due = request.GET.date_due.strip()

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
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, "CLOSED")"""
            arg = (no, datetime.datetime.now().isoformat())

        else:
            sql = """INSERT INTO 'history' ('task_id', 'entry_date', 'ledger') VALUES (?, ?, "EDITED")"""
            arg = (no, datetime.datetime.now().isoformat())

        c.execute(sql, arg)
        conn.commit()
        c.close()

        return todo_list(proj='all', tag='all', state='all')

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchall()

        if cur_data[0][2] == 1:
            cur_status = 'open'
        else:
            cur_status = 'closed'

        return template('edit_task', old=cur_data, old_status=cur_status, no=no)

# URL /edit, gets number from form and executes /edit/number
@route('/edit', method='GET')
def edit_item_from_table():

    if request.GET.edit:
        number = request.GET.number.strip()
        return edit_item(number)

# From baseline example - need to extend to pull in notes and status table
@route('/item<item:re:[0-9]+>')
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


@route('/help')
def help():
    static_file('help.html', root='.')

#  Comes from page that showed how to reference css
@route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static')

@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {{'task': result[0]}, {'status': result[1]}, {'project': result[2]}, {'tag': result[3]}, {'state': result[4]}}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment
