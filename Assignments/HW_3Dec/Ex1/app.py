from flask import Flask,request,render_template,jsonify
import pandas as pd
import requests
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../Files/data_cleaned.csv')

app = Flask(__name__)

data = pd.read_csv(filename)

@app.route('/')

def render_homepage():
    # render the homepage and form
    return render_template("homepage.html")

@app.route("/state/<string:name>")
def getStateData(name):
    dict_ = {}
    name = name.lower()
    try:
        dict_[name] = float(data[data['State'].str.lower() == name]['Age-Adjusted Incidence Rate([rate note]) - cases per 100,000'])
    except:
        dict_['message'] = "Check the name of the state" 
    return jsonify(dict_)
@app.route("/submit-form",methods = ["POST"])
# def sendRequest():
#     state_name = request.form['state']
#     params = {'state_name':state_name}
#     return requests.get("http://127.0.0.1:8000/info",params = params).text

@app.route("/info", methods=["GET"])
def get_info():
    state = request.args.get('state_name')
    print(request.args)
    dict_ = {}
    name = state.lower()
    try:
        dict_[name] = float(data[data['State'].str.lower() == name]['Age-Adjusted Incidence Rate([rate note]) - cases per 100,000'])
    except:
        dict_['message'] = "Check the name of the state" 
    return render_template("info.html",my_dict = dict_)

if __name__ == '__main__':
    app.debug = True
    app.run(port = 8000)
    app.run(debug = True)
   