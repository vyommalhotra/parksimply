import os
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def display_title():
    return {'title': 'Park Simply'}

@app.route('/get_car_ids')
def get_car_ids():
    f = open("buffer.txt", "r")
    return {'data': f.read()}
