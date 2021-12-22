import numpy as np
import os
import pandas as pd
import utils
import importlib
importlib.reload(utils)
import random
import glob


dirname = os.path.dirname(__file__)
df_filename = os.path.join(dirname, '../data/Corona_Tweet_Data_processed.csv')
wordcloud_filename = os.path.join(dirname, '../static/images/wordcloud.jpg')

data = pd.read_csv(df_filename,parse_dates=['TweetAt'],index_col = 0,dtype={'UserName': 'str', 'ScreenName': 'str','Location':'str'},converters={"message_tokens_lemmatized": lambda x: x.strip("[]").replace("'","").split(", "),"message_tokenized": lambda x: x.strip("[]").replace("'","").split(", "),"mentions":lambda x: x.strip("[]").replace("'","").split(", ")})
data['TweetAt'] = pd.to_datetime(data['TweetAt'],errors = 'coerce')


def getDropDownList(n):
    filename = os.path.join(dirname, '../data/locations.npy')
    locations = np.load(filename,allow_pickle=True)
    valid_locations = locations[0][locations[1]>n]
    return list(valid_locations)


def returnRegionData(regions = None):
    data_lst = []
    sentiments = [-2,-1,0,1,2]
    sentiment_mapping = {-2:'Extremely Negative',-1:'Negative',0:'Neutral',1:'Positive',2:'Extremely Positive'}
    # print('**************',regions,type(regions))
    # print(regions)
    if(regions!= None):
        subset_data = data[data['Location'].str.contains("\\b(" + "|".join(regions) + ")\\b",na = False,case = False)]
    else:
        subset_data = data

    for i in sentiments:
        s_data = subset_data[subset_data['Sentiment_numerical'] == i].groupby('TweetAt').count()
        s_data.sort_index(inplace=True)
        counts = s_data['OriginalTweet'].values
        counts = counts.tolist()
        dates = s_data.index.astype(str)
        s_data_dict = {'x': list(dates),'y':counts,'name':sentiment_mapping[i]}
        data_lst.append(s_data_dict)

    return data_lst


def getWordCloud(regions = None,sentiment = 0):
    print("in get word cloud")
    print(regions)
    print(sentiment)

    for filename in glob.glob(os.path.join(dirname, '../static/images/wordcloud*')):
        try:
            os.remove(filename)
        except:
            pass
    
    if(regions!= None):
        subset_data = data[data['Location'].str.contains("\\b(" + "|".join(regions) + ")\\b",na = False,case = False)].copy()
    else:
        print("Yesss")
        subset_data = data

    wc_filename = "wordcloud" +str(random.randint(0,100000)) + ".jpg"
    wordcloud_filename = os.path.join(dirname, '../static/images/'+wc_filename)
    print("subset data",len(subset_data))
    utils.create_wordcloud(subset_data.loc[subset_data['Sentiment_numerical'] == sentiment,"lemmatized_message"].values,wordcloud_filename)
    return wc_filename

def getTopNTerms(regions = None,sentiment = 0,n = 10):
    print("in get word cloud")
    print(regions)
    print(sentiment)

    
    
    if(regions!= None):
        subset_data = data[data['Location'].str.contains("\\b(" + "|".join(regions) + ")\\b",na = False,case = False)].copy()
    else:
        subset_data = data

    
    df_nterms = subset_data.loc[subset_data['Sentiment_numerical'] == sentiment].copy()
    frequent_terms = utils.getMostCommon(df_nterms,n,"message_tokens_lemmatized")
    frequent_terms = list(map(list, zip(*frequent_terms)))
    frequent_terms_dict = {'x': frequent_terms[0],'y':frequent_terms[1]}

    return frequent_terms_dict

def getTopMentions(region = None,n = 100):
    all_words = []
    if(region!= None):
        subset_data = data[data['Location'].str.contains("\\b(" + "|".join(region) + ")\\b",na = False,case = False)].copy()
    else:
        print("Yesss")
        subset_data = data

    
    subset_data['mentions'].apply(lambda x: utils.add_words(all_words,x))
    all_words = np.array(all_words)
    all_words = all_words[all_words!='']
    freq_cnt = np.unique(all_words,return_counts= True)
    sorted_indexes = np.argsort(freq_cnt[1])[::-1]
    mentions = freq_cnt[0][sorted_indexes]
    counts = freq_cnt[1][sorted_indexes]
    mentions_t = mentions[counts>n].tolist()
    counts_t = counts[counts>n].tolist()
    frequent_mentions_dict = {'x': counts_t,'y':mentions_t}

    return frequent_mentions_dict

def getHistogram(regions = None,sentiment = 0):
    print("in get word cloud")
    print(regions)
    print(sentiment)

    
    
    if(regions!= None):
        subset_data = data[data['Location'].str.contains("\\b(" + "|".join(regions) + ")\\b",na = False,case = False)].copy()
    else:
        subset_data = data

    
    tweet_lengths = subset_data.loc[subset_data['Sentiment_numerical'] == sentiment,'Tweet_Length'].values

    return tweet_lengths
    


