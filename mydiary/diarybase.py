"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import os
from markdown2 import markdown
from flask import Blueprint, flash, redirect, render_template, request, url_for
from . import app
from .command import initApp
from .config import MyConfig
from .database import getDatabase, getLcDatabase

# Load config
app.config.from_object(MyConfig)

# Create instance path
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Create Cache folder
if not os.path.exists(app.config["DB_CACHE"]):
    os.makedirs(app.config["DB_CACHE"])


initApp()


@app.route('/config')
def getConfig():
    return str(dict(app.config))


""" Task pages """
def getSingleTask(task_id):
    return getDataBase().execute(
        "SELECT * FROM mytasks WHERE id = ?", (str(task_id), )
    ).fetchone()


def getNavs():
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return navs


@app.route("/skill")
def skill():
    from . import skill as skl
    db = getDatabase()
    skills = [skl.getSkillStatus(s) for s in db.execute('SELECT * FROM mystatus').fetchall()]
    return render_template(
        'skill.html', SKLS=skills, NAVS=getNavs())


@app.route("/leetcode")
def leetcode():
    from .utils import getBlock, getLeetCodeStatus
    from . import leetcode as lc
    db = getLcDatabase()
    questions = db.execute('SELECT * FROM questions').fetchall()
    assert questions
    return render_template(
        'leetcode.html', PAGEBODY=getLeetCodeStatus(questions), NAVS=getNavs())


@app.route("/", methods=('GET', 'POST'))
def index():
    from .task import getTaskStatus
    db = getDatabase()
    tasks = db.execute(
        'SELECT * FROM mytasks').fetchall()
    tasks.reverse()
    # Only show 100 tasks
    tasks = tasks[: 100]
    TS = []
    for t in tasks:
        TS.append(getTaskStatus(t))
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'tasks.html', NAVS=navs, TASKS=TS)


@app.route("/create", methods=('GET', 'POST'))
def create():
    from .task import registerTask
    db = getDatabase()
    if request.method == 'POST':
        kwargs = dict([(key, val[0]) for key, val in dict(request.form).items()])
        registerTask(db, **kwargs)
        return redirect(url_for('index'))
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'create.html', NAVS=navs)


@app.route("/view", methods=('GET', 'POST'))
def view():
    from .task import getTaskStatus
    task_id = request.args.get("task_id", type=str)
    if request.method == 'POST':
        print("x")
    t = getDatabase().execute('SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    t_data = getTaskStatus(t)
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'task.html', NAVS=navs, T=t_data)


@app.route("/edit", methods=('GET', 'POST'))
def edit():
    from .task import getTaskStatus
    task_id = request.args.get("task_id", type=str)
    db = getDatabase()
    t = db.execute('SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    t_data = getTaskStatus(t)
    if request.method == 'POST':
        db.execute('UPDATE mytasks SET description = ? WHERE id = ?', (request.form["description"], str(task_id)))
        db.commit()
        return redirect(url_for('view', task_id=task_id))
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    t_data['description'] = t['description']
    return render_template(
        'edit.html', NAVS=navs, T=t_data)