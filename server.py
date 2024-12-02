from flask import Flask, render_template, request
import psycopg2
from os import environ as env
from database import *
from algolia import *


app = Flask(__name__)

setup()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/basic', methods=['GET'])
def basic_search():
    query = request.args.get('query', '')
    workouts = []
    if query:
        workouts = search_workouts(search_query=query)
    else:
        workouts = get_workouts()
    
    return render_template('basic_search.html', workouts=workouts, query=query)


@app.route('/algolia')
def algolia():
    return render_template('algolia_search.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')