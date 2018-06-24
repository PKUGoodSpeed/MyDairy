"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import click
from termcolor import colored
from flask.cli import with_appcontext
from . import app
from . import task
from . import skill as skl
from . import leetcode as lc
from . import database


@click.command('init-db', short_help=colored("Initialize tasks database.", "blue"))
@with_appcontext
def initDatabaseCmd():
    try:
        database.dupDatebase("tasks")
    except:
        click.echo(colored("WARNING: Duplicating database failed!", "yellow", "on_white"))
    db = database.getDatabase()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    click.echo(colored("Initialize My Tasks Database Succeed!", "cyan"))


@click.command('init-lc', short_help=colored("Initialize Leetcode database.", "blue"))
@with_appcontext
def initLcCmd():
    try:
        database.dupDatebase("leetcode")
    except:
        click.echo(colored("WARNING: Duplicating database failed!", "yellow", "on_white"))
    lc_db = database.getLcDatabase()
    with app.open_resource('lc_schema.sql') as f:
        lc_db.executescript(f.read().decode('utf8'))
    for i in range(app.config['LEETCODE']['NUM_QUESTIONS']):
        lc_db.execute("INSERT INTO questions (status) VALUES (\'unsolved\')")
    lc_db.commit()
    click.echo(colored("Initialize My LeetCode Database Succeed!", "cyan"))


@click.command('show-lc', short_help=colored("Show Leetcode completion status.", "blue"))
@with_appcontext
def showLcCmd():
    db = database.getLcDatabase()
    click.echo(lc.showLc(db))


@click.command('updt-lc', short_help=colored('Update lc questions\' status.', "blue"))
@click.option('--qid', help=colored('Question ids.', "yellow"), default='0')
@click.option('--status', help=colored('Status.', "yellow"), default='marked')
@with_appcontext
def updateLcCmd(qid, status):
    db = database.getLcDatabase()
    for q_id in qid.split(","):
        click.echo(lc.updateQuestion(q_id, db, status))


@click.command('rollout-lc', short_help=colored("Roll out unsolved leetcode question numbers.", "blue"))
@click.option('--nq', help=colored('Number of questions to be rolled out.', "yellow"), default=10)
@with_appcontext
def rolloutLcCmd(nq):
    from .leetcode import getLcQuestionNumbers
    lc_db = database.getLcDatabase()
    todo = getLcQuestionNumbers(lc_db, n_question=int(nq))
    msg = "Get unsolved questions " + ",".join([str(m) for m in todo])
    click.echo(colored(msg, "cyan"))


@click.command('regi-lc', short_help=colored("Register Leetcode question task.", "blue"))
@click.option('--nq', help=colored('Number of questions to be rolled out.', "yellow"), default=10)
@with_appcontext
def registerLcTaskCmd(nq):
    from .leetcode import registerLcTask
    lc_db = database.getLcDatabase()
    db = database.getDatabase()
    try:
        todo = registerLcTask(db, lc_db, n_question=int(nq))
        msg = "Get unsolved questions " + ",".join([str(m) for m in todo])
        click.echo(colored(msg, "cyan"))
        click.echo(colored("Registered leetcode task!", "cyan"))
    except:
        click.echo(colored("ERROR: Registering leetcode task failed!", "red", "on_white"))


""" Task commands """
@click.command('show-td', short_help=colored("Show task detail.", "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def showTaskDetailCmd(tid):
    db = database.getDatabase()
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(tid), )).fetchone()
    if not t:
        click.echo(colored("ERROR: Task #{I} does not exist!".format(I=str(tid)), "red", "on_white"))
        return
    msg = task.showTaskDetail(t)
    click.echo(msg)


@click.command('show-ts', short_help=colored("Show task summary.", "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def showTaskSummaryCmd(tid):
    db = database.getDatabase()
    t = db.execute(
        'SELECT * FROM mytasks WHERE id = ?', (str(tid), )).fetchone()
    if not t:
        click.echo(colored("ERROR: Task #{I} does not exist!".format(I=str(tid)), "red", "on_white"))
        return
    msg = task.showTaskSummary(t)
    click.echo(msg)


@click.command('regi-t', short_help=colored("Register a new task.", "blue"))
@click.option('--category', help=colored('Task category, e.g. stdy.', "yellow"), default='stdy')
@click.option('--direction', help=colored('Task direction, e.g. algo.', "yellow"), default='algo')
@click.option('--taskname', help=colored('Task name, e.g. leetcode.', "yellow"), default='leetcode')
@click.option('--description', help=colored('Description of the task, e.g. This task is about ...', "yellow"), default="Undefined")
@click.option('--num_steps', help=colored('Number of steps needed to complete the task, e.g. 10 (questions).', "yellow"), default=10)
@click.option('--rewards', help=colored('Rewards obtained upon completion of the task, e.g. 10 (points).', "yellow"), default=10)
@click.option('--duration', help=colored('Duration estimation of doing the task, e.g. 12 (hours).', "yellow"), default=12)
@with_appcontext
def registerTaskCmd(category, direction, taskname, description, num_steps, rewards, duration):
    db = database.getDatabase()
    tid = task.registerTask(
        db, duration, category=category, direction=direction, taskname=taskname,
        description=description, num_steps=str(num_steps), rewards=str(rewards))
    msg = colored("Successfully registered new task with id=" + str(tid), "magenta")
    click.echo(msg)


@click.command('proc-t', short_help=colored('Proceed a task.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def proceedTaskCmd(tid):
    db = database.getDatabase()
    msg = task.proceed(tid, db)
    click.echo(msg)


@click.command('undo-t', short_help=colored('Undo a proceed.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def undoTaskCmd(tid):
    db = database.getDatabase()
    msg = task.undoProceed(tid, db)
    click.echo(msg)


@click.command('drop-t', short_help=colored('Drop an existing task.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=0)
@with_appcontext
def dropTaskCmd(tid):
    db = database.getDatabase()
    msg = task.dropTask(tid, db)
    click.echo(msg)


@click.command('updt-t', short_help=colored('Update an existing task.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@click.option('--entry', help=colored('Entry name of the update.', "yellow"), default='rewards')
@click.option('--value', help=colored('Value to modified to for the above entry.', "yellow"), default=1)
@with_appcontext
def updateTaskCmd(tid, entry, value):
    db = database.getDatabase()
    msg = task.updateTask(tid, db, entry, value)
    click.echo(msg)


@click.command('subm-t', short_help=colored('Submit a completed task.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def submitTaskCmd(tid):
    db = database.getDatabase()
    msg = task.submitTask(tid, db)
    click.echo(msg)

""" Skill commands """
@click.command('show-as', short_help=colored('Show all skills\' status.', "blue"))
@with_appcontext
def showAllSkillsCmd():
    db = database.getDatabase()
    click.echo(skl.showAllSkills(db))


@click.command('show-sk', short_help=colored('Show a skill status.', "blue"))
@click.option('--skill', help=colored('Skill name.', "yellow"), default='algo')
@with_appcontext
def showSkillCmd(skill):
    db = database.getDatabase()
    skill_data = db.execute(
        'SELECT * FROM mystatus WHERE skill = ?', (str(skill), )).fetchone()
    if not skill_data:
        click.echo(colored("ERROR: Skill {S} is not in your skill set!".format(S=str(skill)), "red", "on_white"))
        return
    click.echo(skl.showSkill(skill_data))


@click.command('add-sk', short_help=colored('Add a new skill.', "blue"))
@click.option('--skill', help=colored('Skill name.', "yellow"), default='algo')
@click.option('--power', help=colored('Skill power.', "yellow"), default=2)
@with_appcontext
def addSkillCmd(skill, power):
    db = database.getDatabase()
    click.echo(skl.addSkill(skill, db, power=power))


@click.command('drop-sk', short_help=colored('Drop an existing skill.', "blue"))
@click.option('--skill', help=colored('Skill name.', "yellow"), default='')
@with_appcontext
def dropSkillCmd(skill):
    db = database.getDatabase()
    click.echo(skl.dropSkill(skill, db))


@click.command('modi-sk', short_help=colored('Modify the power of an existing skill.', "blue"))
@click.option('--skill', help=colored('Skill name.', "yellow"), default='algo')
@click.option('--power', help=colored('Skill power.', "yellow"), default=2)
@with_appcontext
def modifySkillCmd(skill, power):
    db = database.getDatabase()
    click.echo(skl.modifySkill(skill, db, power))


@click.command('updt-sk', short_help=colored('Updating a skill points.', "blue"))
@click.option('--skill', help=colored('Skill name.', "yellow"), default='algo')
@click.option('--delta', help=colored('Delta point values.', "yellow"), default='0')
@with_appcontext
def updateSkillCmd(skill, delta):
    db = database.getDatabase()
    click.echo(skl.updateSkillPoints(skill, db, int(delta)))


def initApp():
    app.teardown_appcontext(database.closeDatabase)
    app.teardown_appcontext(database.closeLcDatabase)
    app.cli.add_command(initDatabaseCmd)
    app.cli.add_command(initLcCmd)
    app.cli.add_command(showLcCmd)
    app.cli.add_command(updateLcCmd)
    app.cli.add_command(rolloutLcCmd)
    app.cli.add_command(registerLcTaskCmd)
    app.cli.add_command(showTaskDetailCmd)
    app.cli.add_command(showTaskSummaryCmd)
    app.cli.add_command(registerTaskCmd)
    app.cli.add_command(proceedTaskCmd)
    app.cli.add_command(undoTaskCmd)
    app.cli.add_command(dropTaskCmd)
    app.cli.add_command(submitTaskCmd)
    app.cli.add_command(updateTaskCmd)
    app.cli.add_command(showAllSkillsCmd)
    app.cli.add_command(showSkillCmd)
    app.cli.add_command(addSkillCmd)
    app.cli.add_command(dropSkillCmd)
    app.cli.add_command(modifySkillCmd)
    app.cli.add_command(updateSkillCmd)
