"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
from flask import Flask
app = Flask(__name__, instance_relative_config=True)
from . import diarybase