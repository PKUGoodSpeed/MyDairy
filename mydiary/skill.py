"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
from termcolor import colored
STAT_BAR = 60


def getColorViaLevel(level):
    assert level >= 0, "Level cannot be negative"
    if level < 4:
        return 'white'
    elif level < 8:
        return "green"
    elif level < 16:
        return "blue"
    elif level < 32:
        return "cyan"
    elif level < 64:
        return "yellow"
    else:
        return "red"


""" Show skill status """
def showSkill(skill_data):
    level = 0
    skill = str(skill_data["skill"])
    points = int(skill_data['points'])
    power = int(skill_data['power'])
    while level ** power <= points:
        level += 1
    current_level_points = points - (level - 1) ** power
    points_to_next_level = level ** power - (level - 1) ** power
    n_comp = int(STAT_BAR * current_level_points) / points_to_next_level
    color = getColorViaLevel(level-1)
    msg = colored("Skill: " + str(skill) + "      Power: " + str(power) + "\n", color)
    msg += colored("Level: {L}         Points: {P}".format(L=str(level-1), P=str(points)) + "\n", color)
    msg += colored("+" * int(n_comp), "green") + colored('-' * int(STAT_BAR - n_comp), 'white') + "Next Level\n"
    return msg


def showAllSkills(db):
    skills = db.execute(
        'SELECT * FROM mystatus').fetchall()
    msg = "=" * 80 + "\n"
    for i, skill_data in enumerate(skills):
        msg += showSkill(skill_data)
        if i < len(skills) - 1:
            msg += "-" * 60 + "\n"
    msg += "=" * 80 + "\n"
    return msg
        

def modifySkill(skill, db, pwr):
    """ Modify power value of a skill """
    skill_data = db.execute(
        'SELECT * FROM mystatus WHERE skill = ?', (str(skill), )).fetchone()
    if not skill_data:
        return colored("ERROR: Skill {S} is not in your skill set!".format(S=str(skill)), "red", "on_white")
    pwr = int(pwr)
    if pwr < 0:
        return colored("ERROR: Power value should alwasy be positive.", "red", "on_white")
    db.execute(
        'UPDATE mystatus SET power = ? WHERE skill = ?', (str(pwr), str(skill)))
    db.commit()
    return colored("{S}\' power is modified from {OLD} -> {NEW}".format(
        S=str(skill), OLD=str(skill_data['power']), NEW=str(pwr)), 'cyan')


def updateSkillPoints(skill, db, delta):
    """ Modify the total points of a skill """
    skill_data = db.execute(
        'SELECT * FROM mystatus WHERE skill = ?', (str(skill), )).fetchone()
    if not skill_data:
        return colored("ERROR: Skill {S} is not in your skill set!".format(S=str(skill)), "red", "on_white")
    new_points = max(0, skill_data['points'] + int(delta))
    db.execute(
        'UPDATE mystatus SET points = ? WHERE skill = ?', (str(new_points), str(skill)))
    db.commit()
    return colored("{S}\' power is updated from {OLD} -> {NEW}".format(
        S=str(skill), OLD=str(skill_data['points']), NEW=str(new_points)), 'cyan')


def addSkill(skill, db, **kwargs):
    """ Modify the total points of a skill """
    skill_data = db.execute(
        'SELECT * FROM mystatus WHERE skill = ?', (str(skill), )).fetchone()
    if skill_data:
        return colored("ERROR: Skill {S} is already in the skill set!".format(S=str(skill)), "red", "on_white")
    db.execute(
        'INSERT INTO mystatus (skill, power, points)'
        'VALUES (?, ?, ?)', (str(skill), str(kwargs['power']), "0"))
    db.commit()
    return colored("Add new skill: " + str(skill), 'cyan')


def dropSkill(skill, db):
    """ Modify the total points of a skill """
    skill_data = db.execute(
        'SELECT * FROM mystatus WHERE skill = ?', (str(skill), )).fetchone()
    if not skill_data:
        return colored("ERROR: Skill {S} is not in your skill set!".format(S=str(skill)), "red", "on_white")
    db.execute(
        'DELETE FROM mystatus WHERE skill = ?', (str(skill), ))
    db.commit()
    return colored("Drop skill: " + str(skill), 'cyan')
