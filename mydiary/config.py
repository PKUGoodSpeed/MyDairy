"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
from . import app

class MyConfig:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "auto_blog"
    DATABASE = app.instance_path + '/tasks.database'
    LC_DATABASE = app.instance_path + "/leetcode.database"
    LC_TOTAL = 851
    DB_CACHE = app.instance_path + "/cache"