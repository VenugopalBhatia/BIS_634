import numpy as np
import pandas as pd
import Path


class meshTerms:
    def __init__(self,fNameCancer,fNameAlzheimer):
        self.fNameCancer = Path(__file__).parent /"../Data" /fNameCancer
        self.fNameAlzheimer = Path(__file__).parent /"../Data" /fNameAlzheimer
        self.dfCancer = pd.read_json(self.fNameCancer,orient = "index")
        self.dfAlzheimer = pd.read_json(self.fNameAlzheimer,orient = "index")
    
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

    