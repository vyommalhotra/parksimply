import os
from flask import Flask
from flask import send_file

app = Flask(__name__)

@app.route('/test')
def display_title():
    return {'title': 'Park Simply'}

@app.route('/get_car_ids')
def get_car_ids():
    f = open("buffer.txt", "r")
    return {'data': f.read()}

@app.route('/get_display')
def get_display():
    filename = "display.jpg"
    return send_file(filename, mimetype="image/jpg")
