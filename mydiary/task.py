"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import time
from datetime import datetime
from termcolor import colored


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


""" Proceed Actions """
def proceed(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
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
        return colored("ERROR: task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
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
    if passedDeadline(t):
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
    if passedDeadline(t):
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


""" Insert and remove tasks """
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
        return colored("ERROR: task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    db.execute('DELETE FROM mytasks WHERE id = ?', (str(task_id), ))
    db.commit()
    return colored("Drop Task {I} \'{NM}\'".format(
        I=str(task_id), NM=t['taskname']), "cyan")


def submitTask(task_id, db):
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(task_id), )).fetchone()
    if not t:
        return colored("ERROR: task #{I} does not exist!".format(I=str(task_id)), "red", "on_white")
    if not finished(t):
        return colored("ERROR: task #{I} is not completed!".format(I=str(task_id)), "red", "on_white")
    if submitted(t):
        return colored("ERROR: task #{I} has been submitted!".format(I=str(task_id)), "red", "on_white")
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
        db.execute('INSERT INTO mystatus (skill, level, points)'
        'VALUES (?, ?, ?)', (t['direction'], "0", str(r_points)))
        db.commit()
        msg += colored("Getting new skill {S}; points: {OLD}->{NEW}\n".format(
            S=t['direction'], OLD="0", NEW=str(r_points)), "cyan")
    else:
        new_pts = int(stat['points'] + r_points)
        db.execute('UPDATE mystatus SET points = ? WHERE skill = ?', (str(new_pts), t['direction']))
        db.commit()
        msg += colored("Skill {S} improved; points: {OLD}->{NEW}".format(
            S=t['direction'], OLD=str(stat['points']), NEW=str(new_pts)), "cyan")
    return msg
