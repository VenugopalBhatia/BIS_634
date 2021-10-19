import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import json
import datetime


class getEntrezData:
    def __init__(self,url):
        self.url = url
    
    
    def queryAPI(self,_params,type = 'esearch.fcgi',req_type = "GET"):
        _url = self.url+type
        if(req_type == "POST"):
            data = requests.post(_url,data = _params)
        elif(req_type == "GET"):
            data = requests.get(_url,params = _params)

        print(data.status_code,data.url)
        return data
    
    def getFullRecords(self,_params,parse_records = False):
        raw_data = self.queryAPI(_params)
        data = BeautifulSoup(raw_data.text,'lxml')
        ids_ = [int(id_.text) for id_ in data.select('idlist>id')]
        id_len = len(ids_)
        id_str = str(ids_)
        id_str = re.sub('\[|\]','',id_str)
        req_data = {}  ## No real need for this, could simply pass params and still works however thought it should be better to keep post request data separate for this api call
        req_data['db'] = _params['db']
        req_data['id'] = id_str
        req_data['retmode'] = "xml"
        req_data['retmax'] = _params["retmax"]
        
        if(id_len>200):
            records_ = self.queryAPI(req_data,type = 'efetch.fcgi',req_type = "POST")
        else:
            records_ = self.queryAPI(req_data,type = 'efetch.fcgi')
        if(parse_records):
            self.parseRecords(records_,_params)
            pass
        else:
            return records_

    def parseRecords(self,records,_params,store = True):
        records_raw =  BeautifulSoup(records.text,'lxml')
        articleSet = records_raw.select("pubmedarticleset>*")
        records = {}
        for article in articleSet:
            #print(article)
            
            articlePmid = article.select("pmid")[0].text
            if(article.name == "pubmedbookarticle"):
                articleTitle = article.select("booktitle")[0].text 
            else:
                articleTitle = article.select("title")[0].text
            articleAbstract = [abstract.text for abstract in article.select("abstract>abstracttext")]
            articleMeshTerms = [meshTerm.text for meshTerm in article.select("meshheading")]
            records[articlePmid] = {
                "ArticleTitle": articleTitle,
                "AbstractText": articleAbstract,
                "query": _params['term'],
                "mesh_terms": articleMeshTerms
            }

        if(store):
            searchTerm = _params["term"].split(" AND ")[0]
            fileName = str(datetime.date.today()) + "_searched_term_" + searchTerm + ".json"
            path_ = Path(__file__).parent /"../Data" /fileName

            with open(path_,"w+") as jsonFile:
                json.dump(records,jsonFile)
            
            del records
        else:
            return records

    





    

        
        

