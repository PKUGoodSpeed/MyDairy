"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import os
import click
import sqlite3
from shutil import copyfile
from datetime import datetime
from termcolor import colored
from flask import g, render_template
from . import app


def getDatabase():
    if "database" not in g:
        g.database = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row
    return g.database


def closeDatabase(e=None):
    db = g.pop('database', None)
    if db is not None:
        db.close()


def getLcDatabase():
    if "lc_database" not in g:
        g.lc_database = sqlite3.connect(
            app.config["LC_DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.lc_database.row_factory = sqlite3.Row
    return g.lc_database


def closeLcDatabase(e=None):
    db = g.pop('lc_database', None)
    if db is not None:
        db.close()


def dupDatebase(name="tasks"):
    # Make replica of database
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    if not os.path.exists(app.config["DB_CACHE"]):
        os.path.exists(app.config["DB_CACHE"])
    src = app.instance_path + "/" + name + ".database"
    tar = app.config["DB_CACHE"] + "/" + name + "_"
    tar += str(datetime.now()).replace(" ", "_")
    tar += ".database"
    copyfile(src, tar)
    click.echo(name + " database is saved in " + tar)


def showLc():
    from numpy import random
    msg = ""
    for i in range(851):
        u = random.random()
        if u > 0.5:
            msg += colored("[%03d]" %(i+1), "green")
        else:
            msg += colored("[%03d]" %(i+1), "white")
        if (i+1) % 20 == 0:
            msg += "\n"
    click.echo(msg)
