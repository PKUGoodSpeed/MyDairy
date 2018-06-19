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


@click.command('show-lc', short_help=colored("Show Leetcode completion status.", "blue"))
@with_appcontext
def showLcCmd():
    database.showLc()


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
    click.echo(colored("Initialize My LeetCode Database Succeed!", "cyan"))


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
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def dropTaskCmd(tid):
    db = database.getDatabase()
    msg = task.dropTask(tid, db)
    click.echo(msg)


@click.command('subm-t', short_help=colored('Submit a completed task.', "blue"))
@click.option('--tid', help=colored('Task id.', "yellow"), default=1)
@with_appcontext
def submitTaskCmd(tid):
    db = database.getDatabase()
    msg = task.submitTask(tid, db)
    click.echo(msg)


def initApp():
    app.teardown_appcontext(database.closeDatabase)
    app.teardown_appcontext(database.closeLcDatabase)
    app.cli.add_command(initDatabaseCmd)
    app.cli.add_command(showLcCmd)
    app.cli.add_command(initLcCmd)
    app.cli.add_command(showTaskDetailCmd)
    app.cli.add_command(showTaskSummaryCmd)
    app.cli.add_command(registerTaskCmd)
    app.cli.add_command(proceedTaskCmd)
    app.cli.add_command(undoTaskCmd)
    app.cli.add_command(dropTaskCmd)
    app.cli.add_command(submitTaskCmd)
