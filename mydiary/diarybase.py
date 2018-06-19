"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
import os
from flask import render_template
from . import app
from . import auth
from .command import initApp
from .config import MyConfig

# Load config
app.config.from_object(MyConfig)

# Create instance path
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Create Cache folder
if not os.path.exists(app.config["DB_CACHE"]):
    os.makedirs(app.config["DB_CACHE"])


initApp()
'''
app.register_blueprint(auth.blueprint)
app.register_blueprint(question.blueprint)
app.register_blueprint(solution.blueprint)
# app.add_url_rule("/", endpoint='qustion.index')
'''

@app.route('/config')
def getConfig():
    return str(dict(app.config))