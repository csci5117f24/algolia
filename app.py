from flask import Flask, render_template
import psycopg2
from os import environ as env
from database import *
from algolia import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')