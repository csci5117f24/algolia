from flask import Flask, render_template
import psycopg2
from os import environ as env
from database import *
from algolia import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/basic')
def basic():
    return render_template('basic_search.html')

@app.route('/algolia')
def algolia():
    return render_template('algolia_search.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')