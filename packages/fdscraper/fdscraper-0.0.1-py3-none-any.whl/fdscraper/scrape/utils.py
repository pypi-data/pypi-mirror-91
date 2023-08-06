# -*- coding: utf-8 -*-

from fdscraper import pd
import json
from . import NoSuchElementException

def get_date_and_price(price_data):
    date = []
    price = []
    for date_data in price_data:
        date.append(date_data[0])
        price.append(float(date_data[1]))
    return date,price

def get_price(driver,num_days=500):
    ele = driver.find_element_by_xpath('//*[@id="company-info"]')
    comp_id = ele.get_attribute('data-company-id')

    chart_data_url = 'https://www.screener.in/api/company/'+comp_id+ \
    f'/chart/?q=Price&days={num_days}&consolidated=true'
    
    driver.get(chart_data_url)
    try:
        data = json.loads(driver.find_element_by_xpath('/html/body/pre').text)
    except NoSuchElementException:
        return None
    price_data = data['datasets'][0]['values']
    date,price=get_date_and_price(price_data)
    driver.back()
    return pd.Series(price,index=date)

def get_all_tables(driver):
    """Getting all the fndamental data from the page of the respective stock"""
    # print("Getting basic data...")
    # tic = time.time()
    try:
        current_price = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[2]/span[2]/span').text
    except NoSuchElementException:
        current_price = None
    try:
        market_cap = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[1]/span[2]/span').text
    except NoSuchElementException:
        market_cap = None
    try:
        book_value = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[5]/span[2]/span').text
    except NoSuchElementException:
        book_value = None
    try:
        pe = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[4]/span[2]/span').text
    except NoSuchElementException:
        pe = None
    try:
        dividend = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[6]/span[2]/span').text
    except NoSuchElementException:
        dividend = None
    try:
        roce = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[7]/span[2]/span').text
    except NoSuchElementException:
        roce = None
    try:
        roe = driver.find_element_by_xpath('//*[@id="top-ratios"]/li[8]/span[2]/span').text
    except NoSuchElementException:
        roe = None
    try:
        sales3yr = driver.find_element_by_xpath('//*[@id="content-area"]/section[1]/ul/li[9]/b').text
    except NoSuchElementException:
        sales3yr = None
#     table_peers = driver.find_element_by_xpath('//*[@id="peers-table-placeholder"]/div[2]/table')
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting shareholders data...")
    # tic = time.time()
    xpath_shareholding = '//*[@id="shareholding"]/div[@class="responsive-holder fill-card-width"]/table'
    data_shareholding = get_all_data(xpath_shareholding,driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting quarters data...")
    # tic = time.time()
    xpath_quarters = '//*[@id="quarters"]/div[@class="responsive-holder fill-card-width"]/table'
    data_quarters = get_all_data(xpath_quarters,driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting PnL data...")
    # tic = time.time()
    xpath_pnl = '//*[@id="profit-loss"]/div[@class="responsive-holder fill-card-width"]/table'
    data_pnl = get_all_data(xpath_pnl,driver)
    ind_org = data_pnl.index.to_list()
    ind = ['Sales/Revenue' if x=='Sales' or x=='Revenue' else x for x in ind_org]
    ind = ['Financing/Operating Profit' if x=='Financing Profit' or x=='Operating Profit' else x for x in ind]
    ind = ['OPM/FPM %' if x=='Financing Margin %' or x=='OPM %' else x for x in ind]
    mapping = {x:y for x,y in zip(ind_org,ind)}
    data_pnl.rename(index=mapping,inplace=True)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting Balance sheet data...")
    # tic = time.time()
    xpath_balance_sheet = '//*[@id="balance-sheet"]/div[@class="responsive-holder fill-card-width"]/table'
    data_balance_sheet = get_all_data(xpath_balance_sheet,driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting Cashflow data...")
    # tic = time.time()
    xpath_cashflow = '//*[@id="cash-flow"]/div[@class="responsive-holder fill-card-width"]/table'
    data_cashflow = get_all_data(xpath_cashflow,driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting ratios data...")
    # tic = time.time()
    xpath_ratios = '//*[@id="ratios"]/div[@class="responsive-holder fill-card-width"]/table'
    data_ratios = get_all_data(xpath_ratios,driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    # print("Getting price data...")
    # tic = time.time()
    price = get_price(driver)
    # toc = time.time()
    # print(f"Done in {toc-tic} seconds")
    
    flist = {
        'price':price,
        'current_price':current_price,
        'market_cap':market_cap,
        'book_value':book_value,
        'pe':pe,
        'dividend':dividend,
        'roce':roce,
        'roe':roe,
        'sales3yr':sales3yr,
        'table_quarters':data_quarters,
        'table_pnl':data_pnl,
        'table_balance_sheet':data_balance_sheet,
        'table_cashflow':data_cashflow,
        'table_ratios':data_ratios,
        'table_shareholding':data_shareholding}
    return flist

def get_all_data(xpath_table,driver):
    try:
        table = driver.find_element_by_xpath(xpath_table)
    except NoSuchElementException:
        return None
    rows = table.find_elements_by_tag_name("tr")
    datas = table.find_elements_by_tag_name("td")
    ro1 = rows[0]
    datas = ro1.find_elements_by_tag_name("th")
    columns = [datas[i].text for i in range(1,len(datas))]
    df = pd.DataFrame(columns=columns)
    for row in rows[1:]:
        datas = row.find_elements_by_tag_name("td")
        if(datas[0].text==''):
            continue
        ro = [datas[j].text for j in range(len(datas))]
        sr = pd.Series(ro[1:],name=ro[0].split('+')[0].strip(),index=columns)
        df = df.append(sr)
    return df