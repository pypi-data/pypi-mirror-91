# -*- coding: utf-8 -*-
from . import features_by_sector,get_sector_features
from fdscraper import tqdm,os,pd

def get_similar_sectors(base_path,num_past_years):
    sector_list = []
    sector_dict = {'sector_names':[],'columns':[]}
    out_list = []
    for sector_name in tqdm(os.listdir(base_path)):
        sname = sector_name.split('.')[0]
        if sname.split('_')[0] == 'all':
            continue
        print(sname)
        dft = features_by_sector(base_path,sector_name,num_past_years)
        found = False
        if(len(sector_list)!=0):
            for i,(sector,dfs) in enumerate(zip(sector_list,out_list)):
                if(set(sector['columns'])==set(list(dft.columns))):
                    sector['sector_names'].append(sector_name.split('.')[0])
                    dft['sector'] = sname
                    dfs = dfs.append(dft,ignore_index=True)
                    out_list[i] = dfs
                    found = True
                    break
            if(not found):
                sector_dict = {'sector_names':[],'columns':[]}
                sector_dict['sector_names'].append(sector_name.split('.')[0])
                sector_dict['columns'] = list(dft.columns)
                sector_list.append(sector_dict)
                dft['sector'] = sname
                out_list.append(dft)
        else:
            sector_dict['sector_names'].append(sector_name.split('.')[0])
            sector_dict['columns'] = list(dft.columns)
            sector_list.append(sector_dict)
            dft['sector'] = sname
            out_list.append(dft)
#         break
    return sector_list,out_list

def preprocess_financials(data=None,num_past_years=5,base_path=None,\
                          sname='Preprocessed data',verbose=0):
    if(base_path!=None):
        sectors = os.listdir(base_path)
        out_df = pd.DataFrame()
        for sector_name in tqdm(sectors):
            sname = sector_name.split('.')[0]
            if sname.split('_')[0] == 'all':
                continue
            if(verbose>0): print(sname)
            dft = features_by_sector(base_path,sector_name,num_past_years)
            dft['sector'] = sname
            out_df = out_df.append(dft,ignore_index=True)
        return dft
    else:
        dft = get_sector_features(data,num_past_years)
        return dft
            
        