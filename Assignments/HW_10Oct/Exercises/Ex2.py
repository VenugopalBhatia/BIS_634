import numpy as np
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns

class meshTerms:
    def __init__(self,fNameCancer,fNameAlzheimer):
        self.fNameCancer = Path(__file__).parent /"../Data" /fNameCancer
        self.fNameAlzheimer = Path(__file__).parent /"../Data" /fNameAlzheimer
        self.dfCancer = pd.read_json(self.fNameCancer,orient = "index",convert_axes=False)
        self.dfAlzheimer = pd.read_json(self.fNameAlzheimer,orient = "index",convert_axes=False)
    
    def getData(self):
        return self.dfCancer,self.dfAlzheimer

    def getMeshTerms(self,df):
        mesh_terms_arr = np.array(df['mesh_terms'].values)
        mesh_terms_arr = np.concatenate(mesh_terms_arr).ravel()
        return mesh_terms_arr

    def getMeshTermCounts(self,df,nlargest = 10):
        mesh_terms_arr = self.getMeshTerms(df)
        df1 = pd.DataFrame({"mesh_terms":np.unique(mesh_terms_arr,return_counts = True)[0],"counts":np.unique(mesh_terms_arr,return_counts = True)[1]})
        mesh_terms_frequency = df1.nlargest(nlargest,'counts')
        return mesh_terms_frequency
    
    def createSummaryTable(self,df_alzheimer_nl,df_cancer_nl):
        df_summaryTable = pd.DataFrame(0,index = df_alzheimer_nl['mesh_terms'],columns = df_cancer_nl['mesh_terms'])
        index = df_summaryTable.index
        def getTermSum(x):
            _index = x.name
            try:
                df_summaryTable[_index][_index] = df_cancer_nl[df_cancer_nl['mesh_terms'] == _index]['counts'].values[0] + df_alzheimer_nl[df_alzheimer_nl['mesh_terms'] == _index]['counts'].values[0]
            except:
                pass
        df_summaryTable.apply(getTermSum,axis = 1)
        return df_summaryTable

    

    def plotMeshTermCounts(self,mesh_terms_frequency):
        sns.set(rc={'figure.figsize':(25.7,12.27)})
        sns.barplot(x = mesh_terms_frequency['mesh_terms'],y = mesh_terms_frequency['counts'])
    
    def genSummary(self,nLargest = 10):
        df_cancer_nl = self.getMeshTermCounts(self.dfCancer,nlargest = nLargest)
        df_alzheimer_nl = self.getMeshTermCounts(self.dfAlzheimer,nlargest = nLargest)
        summary_table = self.createSummaryTable(df_alzheimer_nl,df_cancer_nl)
        return summary_table,df_alzheimer_nl,df_cancer_nl

    