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
    db = getDatabase()
    tasks = db.execute(
        'SELECT * FROM mytasks').fetchall()
    tasks.reverse()
    # Only show 100 tasks
    tasks = tasks[: 100]
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'base.html', NAVS=navs)


@app.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        print("x")
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'base.html', NAVS=navs)


@app.route("/view", methods=('GET', 'POST'))
def view():
    q_title = request.args.get("q_title", type=str)
    if request.method == 'POST':
        print("x")
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'base.html', NAVS=navs)


@app.route("/edit", methods=('GET', 'POST'))
def edit():
    q_title = request.args.get("q_title", type=str)
    if request.method == 'POST':
        print("x")
    navs = []
    navs.append({"link": url_for('index'), "msg": "Index"})
    navs.append({"link": url_for('skill'), "msg": "Skills"})
    navs.append({"link": url_for('leetcode'), "msg": "LeetCode"})
    return render_template(
        'base.html', NAVS=navs)