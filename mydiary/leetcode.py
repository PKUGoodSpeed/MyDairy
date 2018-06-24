"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
from termcolor import colored


def getColorViaStatus(status):
    if status == 'solved':
        return "on_green"
    elif status == "stuck":
        return "on_yellow"
    elif status == "marked":
        return "on_red"
    else:
        return "on_white"


def showLc(db):
    from numpy import random
    lc_data = db.execute("SELECT * FROM questions")
    msg = ""
    for i, q in enumerate(lc_data):
        q_id = int(q['id'])
        bc = getColorViaStatus(str(q['status']))
        msg += colored("[%03d]" % q_id, "magenta", bc)
        if (i+1) % 20 == 0:
            msg += "\n"
    msg += "\n" * 3
    msg += "=" * 40 + "\n"
    for stat in ["solved", "unsolved", "stuck", "marked"]:
        msg += colored("[###]", "magenta", getColorViaStatus(stat))
        msg += " " + stat + " " * 20
    msg += "\n"
    return msg


def updateQuestion(q_id, db, status):
    if status not in ["solved", "unsolved", "stuck", "marked"]:
        return colored("ERROR: Status {S} is not a valid status!".format(S=str(status)), "red", "on_white")
    q_data = db.execute(
        'SELECT * FROM questions WHERE id = ?', (str(q_id), )).fetchone()
    if not q_data:
        return colored("ERROR: Question #{I} does not exist!".format(I=str(q_id)), "red", "on_white")
    db.execute('UPDATE questions SET status = ? WHERE id = ?', (str(status), str(q_id)))
    db.commit()
    return colored("Status of question #{I} -> {NEW}".format(
        I=str(q_id), NEW=str(status)), "cyan")


def getLcQuestionNumbers(lc_db, n_question=10):
    import numpy as np
    lc_data = lc_db.execute('SELECT * FROM questions').fetchall()
    rest_questions = [q['id'] for q in lc_data if q['status'] in ['unsolved', 'stuck']]
    return np.random.choice(rest_questions, n_question)


def registerLcTask(db, lc_db, n_question=10):
    from .task import registerTask
    todo = getLcQuestionNumbers(lc_db, n_question)
    t_data = {
        "duration": 24,
        "category": "stdy",
        "direction": "algo",
        "taskname": "leetcode",
        "rewards": "10",
        "num_steps": "10"
    }
    t_data['description'] = """
### Solve the following leetcode questions and post on LCAutoBlogs
    """
    t_data['description'] += "\n"
    for td in todo:
        t_data['description'] += "- " + str(td) + "\n"
    registerTask(db, **t_data)
    return todo
