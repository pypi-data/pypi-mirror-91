# -*- coding: utf-8 -*-
from . import download,gtc,prf


class Score:
    def __init__(self,data=None,companies=[],file_path=None,driver_path\
                 = 'chromedriver.exe'):        
        if(file_path!=None):
            comps = download.Companies(driver_path=driver_path)
            if(companies==None):
                self.data = comps.get_financials(file_path=file_path)
        elif(companies!=None):
            comps = download.Companies(driver_path=driver_path)
            comps.companies = companies
            self.data = comps.get_financials()
        else:
            self.data = data
        
    def fundamental_score(self):
        proc_data = prf.preprocess_financials(self.data)
        cols = ['Company_name','DE','PE','ROE','Market Cap','Revenue Growth','PAT Growth','Score(10)']
    
        results = gtc(proc_data)[cols]
        
        return results
        
            
            