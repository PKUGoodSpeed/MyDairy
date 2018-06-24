"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import time
from datetime import datetime
from termcolor import colored
from markdown2 import markdown
from . import skill as skl


MUTABLES = ['num_steps', 'rewards', 'deadline']


def finished(t):
    return t['fin_steps'] == t['num_steps']


def notStart(t):
    return int(t['fin_steps']) == 0


def submitted(t):
    return bool(t['t_complete'])


def passedDeadline(t):
    ddl = int(time.mktime(time.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")))
    now = int(time.time())
    return now > ddl


""" Get Task status for web usage """
def getTaskStatus(t):
    task_data = dict(t)
    task_data['color'] = 'yellow'
    if submitted(t):
        task_data['color'] = 'orange'
    elif passedDeadline(t):
        task_data['color'] = 'red'
    elif finished(t):
        task_data['color'] = 'green'
    task_data['ratio'] = str(100. * t['fin_steps'] / t['num_steps'])
    task_data['description'] = markdown(t['description'])
    return task_data


""" Proceed Actions """
def proceed(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: Task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: Task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
    if finished(t):
        return colored("COMPLETED: task #{I} is completed!".format(I=str(task_id)), "green")
    new_fin_steps = int(t['fin_steps']) + 1
    db.execute(
        'UPDATE mytasks SET fin_steps = ? WHERE id = ?', (str(new_fin_steps), str(task_id)))
    db.commit()
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    color = "yellow"
    if finished(t):
        color = "green"
    msg = colored("STATUS: {F}/{N} is finished!".format(F=str(t['fin_steps']), N=str(t['num_steps'])), color)
    if finished(t):
        msg += "\n" + colored("COMPLETED: task #{I} is completed!".format(I=str(task_id)), "green")
    return msg


def undoProceed(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: Task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: Task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
    new_fin_steps = max(0, int(t['fin_steps']) - 1)
    db.execute(
        'UPDATE mytasks SET fin_steps = ? WHERE id = ?', (str(new_fin_steps), str(task_id)))
    db.commit()
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    color = "red"
    if new_fin_steps:
        color = "yellow"
    msg = colored("STATUS: {F}/{N} is finished!".format(F=str(t['fin_steps']), N=str(t['num_steps'])), color)
    return msg


""" Command line display msgs """
def showTaskDetail(t):
    """ Show a task info """
    msg = "=" * 50 + "\n"
    msg += "TASK #{I}\n".format(I=str(t['id']))
    msg += "{C} {D} \'{N}\'\n".format(C=t['category'], D=t['direction'], N=t['taskname'])
    msg += t['description'] + "\n"
    msg += "Register time:   " + t['t_register'] + '\n'
    msg += "Complete time:        " + t['t_complete'] + '\n'
    msg += "Deadline:        " + t['deadline'] + '\n'
    stat = "Rewards {R} point; Status {F}/{N};\n".format(
        R=str(t['rewards']), F=str(t['fin_steps']), N=str(t['num_steps']))
    color = "yellow"
    if submitted(t):
        color= "cyan"
    elif passedDeadline(t):
        color = 'magenta'
    elif notStart(t):
        color = "red"
    elif finished(t):
        color = "green"
    msg += colored(stat, color)
    msg += "Current time:    " + str(datetime.now()).split(".")[0] + "\n"
    msg += "=" * 50 + "\n"
    return msg


def showTaskSummary(t):
    """ Show task summary """
    color = "yellow"
    if submitted(t):
        color = "cyan"
    elif passedDeadline(t):
        color = 'magenta'
    elif notStart(t):
        color = "red"
    elif finished(t):
        color = "green"
    msg = "{I} \'{NM}\' {F}/{N}".format(
        I=str(t['id']), NM=t['taskname'], F=str(t['fin_steps']), N=str(t['num_steps']))
    return colored(msg, color)


def showTasks(tasks):
    msg = "=" * 80 + "\n"
    for i, t in enumerate(tasks):
        msg += showTaskSummary(t) + "\n"
        if i < len(tasks) - 1:
            msg += "-" * 40 + "\n"
    msg += "=" * 80 + "\n"
    return msg


""" Insert, remove, and update tasks """
def registerTask(db, duration, **options):
    t_regi = int(time.time())
    deadline = t_regi + int(int(duration) * 3600)
    options["t_register"] = str(datetime.fromtimestamp(t_regi))
    options['taskname'] += " " + str(datetime.fromtimestamp(t_regi))
    options["deadline"] = str(datetime.fromtimestamp(deadline))
    options['t_complete'] = ""
    options["fin_steps"] = "0"
    db.execute(
        'INSERT INTO mytasks (category, direction, taskname, t_register, t_complete, deadline, description, num_steps, fin_steps, rewards)'
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            options["category"], options['direction'], options['taskname'], options['t_register'], options['t_complete'],
            options["deadline"], options["description"], options["num_steps"], options["fin_steps"], options["rewards"]))
    db.commit()
    t = db.execute('SELECT * FROM mytasks WHERE t_register = ?', (options['t_register'], )).fetchone()
    return t['id']


def dropTask(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: Task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: Task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
    db.execute('DELETE FROM mytasks WHERE id = ?', (str(task_id), ))
    db.commit()
    return colored("Drop Task {I} \'{NM}\'".format(
        I=str(task_id), NM=t['taskname']), "cyan")


def updateTask(task_id, db, entry, value):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: Task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: Task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
    if entry not in MUTABLES:
        return colored("ERROR: Entry {E} is not in the mutable columns!".format(E=str(entry)), "red", "on_white")
    if entry == 'deadline':
        deadline = int(time.time() + float(value) * 3600)
        deadline = str(datetime.fromtimestamp(deadline))
        db.execute(
            'UPDATE mytasks SET deadline = ? WHERE id = ?', (deadline, str(task_id)))
        db.commit()
    else:
        db.execute(
            'UPDATE mytasks SET {ENTRY} = ? WHERE id = ?'.format(ENTRY=str(entry)), (str(value), str(task_id)))
        db.commit()
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    return showTaskDetail(t)
    
    
""" Submit task """
def submitTask(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: Task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: Task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
    if not finished(t):
        return colored("ERROR: Task #{I} is not completed!".format(I=str(task_id)), "red", "on_white")
    t_comp = int(time.time())
    t_comp = str(datetime.fromtimestamp(t_comp))
    r_points = int(t['rewards'])
    db.execute('UPDATE mytasks SET t_complete = ? WHERE id = ?', (t_comp, str(task_id)))
    db.commit()
    msg = colored("Successfully summitted task {I} \'{NM}\' at {TC}, get {R} reward points!\n".format(
        I=str(task_id), NM=t['taskname'], TC=t_comp, R=str(r_points)), "cyan")
    # For study we need to update the total points
    if t['category'] == 'stdy':
        stat = db.execute('SELECT * FROM mystatus WHERE skill = ?', (t['direction'], )).fetchone()
        if not stat:
            msg += skl.addSkill(t['direction'], db, power=2) + "\n"
        msg += skl.updateSkillPoints(t['direction'], db, delta=r_points) +'\n'
    return msg
