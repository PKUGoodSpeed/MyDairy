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
    LEETCODE = {
        "DATABASE": app.instance_path + "/leetcode.database",
        "NUM_QUESTIONS": 851
    }
    USER = {
        "goodspeed": "1234567890"
    }
    DB_CACHE = app.instance_path + "/cache"