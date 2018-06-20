"""
Diary system
@author: pkugoodspeed
@date: 06/18/2018
"""
from . import app
from markdown2 import markdown
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .database import getDataBase, getLcDatabase


