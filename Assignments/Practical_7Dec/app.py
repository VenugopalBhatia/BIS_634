from flask import Flask,request,render_template,jsonify
import pandas as pd
import requests
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './Files/us_states_Dec7.csv')

app = Flask(__name__)

data = pd.read_csv(filename)

@app.route('/plot',method = ['GET'])
def getDate():
    date = requests.args.get(date)
    data_date = data[data.date == date]
    

