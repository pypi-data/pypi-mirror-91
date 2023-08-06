# -*- coding: utf-8 -*-

from . import webdriver,get_all_tables
from fdscraper import time,os,pickle


class Companies:
    def __init__(self,companies=[],driver_path='chromedriver.exe'):
        #Initializing the webdriver
        options = webdriver.ChromeOptions()
        
        #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
        options.add_argument('headless')
        options.add_argument("window-size=1920,1080")
        options.add_argument("start-maximized")
        
        #Change the path to where chromedriver is in your home folder.
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        # driver.set_window_size(1120, 1000)
        # driver.implicitly_wait(5) # seconds
        
        self.companies = companies
        
    def get_financials(self,file_path=None,out_path=None,verbose=0):
        all_company_data = {}
        if(file_path!=None):
            with open(file_path,'r') as f:
                data = f.read()
                f.close()
            companies = data.split(',')
            companies = [idd.strip() for idd in companies]
            self.companies = companies
        if(verbose>0): print(self.companies)  
        for idd in self.companies[1:]:
            url = f"https://www.screener.in/company/{idd}"
            tic = time.time()
            driver = self.driver
            driver.get(url)
            company_name = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/h1").text
            if(verbose>0): print(company_name,end='-->')
            # Try to get the consolidated figures if they exist
            try:
                consolidated_link = driver.find_element_by_xpath("/html/body/main/section[4]/div[1]/div[1]/p/a")
                if(consolidated_link.text=="View Consolidated"):
                    driver.get(f"https://www.screener.in/company/{idd}/consolidated")
            except:
                pass
            # Get all the data
            company_data = get_all_tables(driver)
            all_company_data[idd] = company_data
            toc = time.time()
            if(verbose>0): print(f"Time taken: {toc-tic} seconds")
        
        if(out_path!=None):
            pickle_out = open(os.path.join(out_path,self.companies[0]+'.pickle'),'wb')
            pickle.dump(all_company_data,pickle_out)
            pickle_out.close()
        driver.quit()
        
        return all_company_data
        

def from_file(file_path,driver_path,out_path):
    """Scrape all the financial data from screener of the specified companies
    in the input file"""
    with open(file_path,'r') as f:
        data = f.read()
        f.close()
        
    ids = data.split(',')
    ids = [idd.strip() for idd in ids]
    print(ids)
    all_company_data = {}
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    options.add_argument('headless')
    options.add_argument("window-size=1920,1080")
    options.add_argument("start-maximized")
#     options.addArguments("--headless");
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_window_size(1120, 1000)
    # driver.implicitly_wait(5) # seconds
    
    for idd in ids[1:]:
        url = f"https://www.screener.in/company/{idd}"
        tic = time.time()
        driver.get(url)
        company_name = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/h1").text
        print(company_name,end='-->')
        # Try to get the consolidated figures if they exist
        try:
            consolidated_link = driver.find_element_by_xpath("/html/body/main/section[4]/div[1]/div[1]/p/a")
            if(consolidated_link.text=="View Consolidated"):
                driver.get(f"https://www.screener.in/company/{idd}/consolidated")
        except:
            pass
        # Get all the data
        company_data = get_all_tables(driver)
        all_company_data[idd] = company_data
        toc = time.time()
        print(f"Time taken: {toc-tic} seconds")
    pickle_out = open(os.path.join(out_path,ids[0]+'.pickle'),'wb')
    pickle.dump(all_company_data,pickle_out)
    pickle_out.close()
    driver.quit()
    
    return all_company_data


def from_list(ids,driver_path,out_path):
    """Scrape all the financial data from screener of the specified companies
    in the input list"""

    all_company_data = {}
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    options.add_argument('headless')
    options.add_argument("window-size=1920,1080")
    options.add_argument("start-maximized")
#     options.addArguments("--headless");
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_window_size(1120, 1000)
    # driver.implicitly_wait(5) # seconds
    
    for idd in ids[1:]:
        url = f"https://www.screener.in/company/{idd}"
        tic = time.time()
        driver.get(url)
        company_name = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/h1").text
        print(company_name,end='-->')
        # Try to get the consolidated figures if they exist
        try:
            consolidated_link = driver.find_element_by_xpath("/html/body/main/section[4]/div[1]/div[1]/p/a")
            if(consolidated_link.text=="View Consolidated"):
                driver.get(f"https://www.screener.in/company/{idd}/consolidated")
        except:
            pass
        # Get all the data
        company_data = get_all_tables(driver)
        all_company_data[idd] = company_data
        toc = time.time()
        print(f"Time taken: {toc-tic} seconds")
    pickle_out = open(os.path.join(out_path,ids[0]+'.pickle'),'wb')
    pickle.dump(all_company_data,pickle_out)
    pickle_out.close()
    driver.quit()
    
    return all_company_data