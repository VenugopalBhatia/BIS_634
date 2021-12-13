from flask import Flask,request,render_template,jsonify
import pandas as pd
import requests
import os
from controllers import homepage

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './data/Corona_Tweet_Data_processed.csv')

app = Flask(__name__)





@app.route('/')

def render_homepage():
    data_countries = homepage.getDropDownList(20)
    # render the homepage and form
    return render_template("homepage.html",dropdown = data_countries)

@app.route("/getRegionData",methods = ['POST'])
def getRegionData():
    regions_dict = request.form.to_dict(flat = False)
    #print(request.form)
    try:
        regions = regions_dict['Region_Dropdown']
        #print(list(regions))
        data_regions = homepage.returnRegionData(regions)
    except:
        data_regions = homepage.returnRegionData()
    #print(data_regions)

    return jsonify(data_regions)

@app.route("/getWordCloud",methods = ['POST'])
def getWordCloud():
    
    regions_dict = request.form.to_dict(flat = False)
    print("********regions dict", regions_dict)
    #print("Function called")
    
    try:
        regions = regions_dict['Region_Dropdown']
        print(list(regions))
    except:
        regions = None
        print("Exception")
       
    try:
        sentiment = int(regions_dict['Sentiment'][0])
    except:
        sentiment = 0
    
    print("Sentiment",sentiment)
    
    wc_filename = homepage.getWordCloud(regions,sentiment)
    
    _url = './static/images/' + wc_filename

    data_dict = {'_link':_url}
    return jsonify(data_dict)

@app.route("/getWordFrequencies",methods = ['POST'])

def getWordFrequencies():
    
    regions_dict = request.form.to_dict(flat = False)
    print("********regions dict", regions_dict)
    #print("Function called")
    
    try:
        regions = regions_dict['Region_Dropdown']
        print(list(regions))
    except:
        regions = None
        print("Exception")
       
    try:
        sentiment = int(regions_dict['Sentiment'][0])
    except:
        sentiment = 0
    
    try:
        numWords = int(regions_dict['numWords'][0])
    except:
        numWords = 10
    
    print("numWords",numWords)

    topNTerms_dict = homepage.getTopNTerms(regions,sentiment,numWords)
    

    return jsonify(topNTerms_dict)


@app.route("/getTopMentions",methods = ['POST'])

def getTopMentions():
    
    regions_dict = request.form.to_dict(flat = False)
    print("********regions dict", regions_dict)
    #print("Function called")
    
    try:
        regions = regions_dict['Region_Dropdown']
        print(list(regions))
    except:
        regions = None
        print("Exception")

    try:
        mentions = int(regions_dict['Mentions_count'][0])
    except:
        mentions = 100
    
    print("numMentions",mentions)

    topNTerms_dict = homepage.getTopMentions(regions,mentions)
    

    return jsonify(topNTerms_dict)
    
    


@app.route("/getHistograms",methods = ['POST'])

def getHistograms():
    
    regions_dict = request.form.to_dict(flat = False)
    print("********regions dict", regions_dict)
    #print("Function called")
    
    try:
        regions = regions_dict['Region_Dropdown']
        print(list(regions))
    except:
        regions = None
        print("Exception")
    
    try:
        sentiment = int(regions_dict['Sentiment'][0])
    except:
        sentiment = 0




    tweet_lengths = homepage.getHistogram(regions,sentiment)

    tweet_lengths = tweet_lengths.tolist()

    tweet_lengths_dict = {'tweet_lengths': tweet_lengths}
    

    return jsonify(tweet_lengths_dict)

    
    



if __name__ == '__main__':
    app.debug = True
    app.run(port = 8000)
    app.run(debug = True)
   