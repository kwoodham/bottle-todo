import sqlite3
import datetime
from bottle import route, run, debug, template, request, static_file, error

@route('/todo/<proj>/<tag>/<state>')
def todo_list(proj, tag, state):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    sql = "SELECT id, task, project, tag, state, date_in FROM todo WHERE status LIKE '1'"
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
    c.close()

    output = template('make_table', rows=result)
    return output


@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        project = request.GET.project.strip()
        tag = request.GET.tag.strip()
        state = request.GET.state.strip()
        date_in = datetime.date.today()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        sql = """INSERT INTO 'todo' 
               ('task', 'status', 'project', 'tag','state', 'date_in') 
               VALUES (?,1,?,?,?,?);"""
        arg = (new, project, tag, state, date_in)
        c.execute(sql, arg)
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        task = request.GET.task.strip()
        status = request.GET.status.strip()
        project = request.GET.project.strip()
        tag = request.GET.tag.strip()
        state = request.GET.state.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ?, project = ?, tag = ?, state = ? WHERE id LIKE ?", (task, status, project, tag, state, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchall()

        if cur_data[0][2] == 1:
            old_status = 'open'
        else:
            old_status = 'closed'

        return template('edit_task', old=cur_data, old_status=old_status, no=no)


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
