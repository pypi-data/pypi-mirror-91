# -*- coding: utf-8 -*-
from fdscraper import pd,np,os,pickle

def filter_columns(cols):
    years = [col.split(' ')[1] for col in cols]
    seen = set()
    uniq = [cols[idx] for idx,x in enumerate(years) if x not in seen and not seen.add(x)]
    return uniq

def combined_table(dfc):
    tbs = dfc['table_balance_sheet']
    tpnl = dfc['table_pnl']
    tcf = dfc['table_cashflow']
    tr = dfc['table_ratios']
#     print(latest_borrowings)
    df = pd.concat([tbs,tpnl,tcf,tr],axis='index')
    if('TTM' in df.columns):
        df.drop('TTM',inplace=True,axis='columns')
    cols = list(df.columns)
    cols = filter_columns(cols)
    df = df[cols]
    df.fillna('0',inplace=True)
    df.replace('','0',inplace=True)
    df = df.apply(lambda x:x.apply(lambda y:y.replace(',','')))
    df = df.apply(lambda x:x.apply(lambda y:y.replace('%','')))
    df = df.astype('float')    

    index = df.index
#     yoy_features_0 = ['Sales','Expenses','Operating Profit','Interest','Profit before tax',\
#                    'Net Profit', 'Borrowings', 'Reserves', 'Other Liabilities']
    yoy_features_0 = ['Sales/Revenue','Financing/Operating Profit','Net Profit']
#     yoy_features_1 = ['Revenue','Expenses','Financing Profit','Profit before tax',\
#                    'Net Profit', 'Borrowings', 'Reserves', 'Other Liabilities']
    yoy_features_1 = ['Revenue''Financing Profit''Net Profit']
#     print(cols)
    df=df.dropna(axis='columns')
    cols = df.columns.to_list()
    features_to_use = yoy_features_0
    status = 0
    for f in yoy_features_0:
        if f not in index:
            features_to_use = yoy_features_1
            status = 1
            break
    if(status):
        for f in yoy_features_1:
            if f not in index:
                return df,None
    epsilon = 1e-5
    for feature in features_to_use:
        df.loc[f'YOY_{feature}',:] = None
        if(len(cols)<=1):
            return df,None
        df.loc[f'YOY_{feature}',cols[1]:] = np.array(df.loc[feature,cols[1]:])/\
        (epsilon + np.array(df.loc[feature,cols[0]:cols[-2]])) - 1
        df.loc[f'YOY_{feature}',cols[0]] = None
    df.fillna(0,inplace = True)
    
#     df['pe'] = dfc['pe']
#     df['roe'] = dfc['roe']
#     df['de'] = latest_borrowings/(latest_sharecapital+latest_reserves)
    
    try:
        latest_borrowings = float(tbs.loc['Borrowings',:].iloc[-1].replace(',',''))
        latest_reserves = float(tbs.loc['Reserves',:].iloc[-1].replace(',',''))
        latest_sharecapital = float(tbs.loc['Share Capital',:].iloc[-1].replace(',',''))
        de = latest_borrowings/(latest_sharecapital+latest_reserves)
        return df,de
    except:
        return df,None
    


def get_table_features_recent(dft,num_past_years):
    cols = list(dft.columns)
    index = dft.index
    features = []
    for i in range(num_past_years):
        for p in index:
            features.append('Y'+str(i)+'_'+p)    

    df = pd.DataFrame(columns = features,dtype=float)
    num_rows = len(list(index))
    if(len(cols)<num_past_years):
        return df
    for j in range(num_past_years):
        newlist = list(dft[cols[len(cols)-num_past_years+j]])
        df.loc[0,features[num_rows*j:num_rows*(j+1)]] = newlist
    return df

def get_company_features(dfc,num_past_years):
    all_tables,de = combined_table(dfc)
    company_features = get_table_features_recent(all_tables,num_past_years)
    company_features['DE'] = de
    try:
        company_features['PE'] = float(dfc['pe'])
    except:
        company_features['PE'] = 40
    try:
        company_features['ROE'] = float(dfc['roe'])
    except:
        company_features['ROE'] = 0
    try:
        company_features['Market Cap'] = float(dfc['market_cap'].replace(',',''))
    except:
        company_features['Market Cap'] = 0

    return company_features

def get_sector_features(data_all,num_past_years):
    comp_names = list(data_all.keys())
    fdfs = pd.DataFrame()
    for company in comp_names:
#         print(company)
        cd = get_company_features(data_all[company],num_past_years)
        if(len(cd.index)==0):
#             print(company)
            continue
        cd.loc[:,'Company_name'] = company
        fdfs = fdfs.append(cd,ignore_index=True)
    return fdfs

def features_by_sector(base_path,sector_name,num_past_years):
    pickle_in = open(os.path.join(base_path,sector_name),'rb')
    data_all = pickle.load(pickle_in)
    fdfs = get_sector_features(data_all,num_past_years)
    return fdfs