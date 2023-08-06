# -*- coding: utf-8 -*-

points_de = [0.1,0.2,0.5,0.8,1,1.5,2,2.5,3,4]
points_roe = [0,1,2,4,7,10,13,17,21,27]
points_pe = [8,12,20,30,40,50,60,70,80,100]
points_rev = [0,1,2.5,5,7.5,10,12.5,15,20,30]
points_pat = points_rev

def score(points,value,minM = True):
    i = 0
    while(value>points[i]):
        i += 1
        if(i==10):
            break
    if(i!=10):
        factor = (value-points[i-1])/(points[i]-points[i-1])
    else:
        factor = 1
    if(minM):
        i=10-i
        if(i==10):
            return i
        return i-factor
    else:
        if(i==0):
            return i
        return i+factor-1
    
def get_score(values):
    de  = score(points_de,values['de'],minM = True)
    pe  = score(points_pe,values['pe'],minM = True)
    roe = score(points_roe,values['roe'],minM = False)
    rev = score(points_rev,values['rev'],minM = False)
    pat = score(points_pat,values['pat'],minM = False)
    
    ratio_score = 5*roe+3*de+2*pe
    ratio_score /= 10
    
    sc = rev*0.3+pat*0.5+ratio_score*0.2
#     print(ratio_score,rev,pat)
    return sc

def get_imp(dfc):
    weights = [0,2,3,4,4]
    sales = [f'Y{i}_YOY_Sales/Revenue' for i in range(5)]
    pats = [f'Y{i}_YOY_Net Profit' for i in range(5)]
#     rev = sum([weights[i]*sales[i] for i in range(5)])/sum(weights)
#     pat = sum([weights[i]*pat[i] for i in range(5)])/sum(weights)
    rev = dfc[sales]*weights*100
    dfc['Revenue Growth'] = rev.sum(axis=1)/sum(weights)

    pat = dfc[pats]*weights*100
    dfc['PAT Growth'] = pat.sum(axis=1)/sum(weights)
    
    return dfc

def get_top_companies(dfc):
    ndf = get_imp(dfc)
#     print(ndf.head())
    for i in ndf.index:
        if(ndf.loc[i,'DE']==None):
            ndf.loc[i,'DE'] = 1
        values = {
        'de':ndf.loc[i,'DE'],
        'pe':ndf.loc[i,'DE'],
        'roe':ndf.loc[i,'ROE'],
        'rev':ndf.loc[i,'Revenue Growth'],
        'pat':ndf.loc[i,'PAT Growth']
        }
        ndf.loc[i,'Score(10)'] = get_score(values)
    ndf.sort_values('Score(10)',ascending=False,inplace=True)
    return ndf
