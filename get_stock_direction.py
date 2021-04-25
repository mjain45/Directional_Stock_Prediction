# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:42:55 2021

@author: apro
"""

import pickle
import numpy as np
from statistics import mode
from datetime import datetime
import json
#%%
# ticker_gms = [('AMZN',2),('AAPL', 1)]
# orig_dt = datetime.strptime('2019-01-04T21:27:00', '%Y-%m-%dT%H:%M:%S') #Input date time
# result = {}
def get_nearest(d, orig_dt):
    # print("orig dt ............", type(orig_dt))
    diff = datetime.strptime(d, '%Y-%m-%d %H:%M:%S') - orig_dt
    # print(type(diff.total_seconds()))
    if float(diff.total_seconds()) < 0:
        return np.Inf
    else:
        # print("diff in secs: ....", diff.total_seconds)
        return diff.total_seconds()
    

#%%
def get_direc(ticker_gms, orig_dt):
    # global result
    result = {}
    for ticker, n_gms in ticker_gms:
        result.setdefault(ticker, {})
        
        # with open('meta_files/'+ ticker +'_all_grams' + str(n_gms) +'(column_names).pickle', 'rb') as handle:
        #     all_grams = pickle.load(handle)
            
        with open('meta_files/'+ ticker +'_news_2019_' + str(n_gms) +'(row_index).pickle', 'rb') as handle:
            news = pickle.load(handle)
            
        with open('meta_files/'+ ticker +'_all_occurance_2019_' + str(n_gms) +'(features).pickle', 'rb') as handle:
            all_occurance = pickle.load(handle)
            
        with open('meta_files/gui_models/logistic_reg_'+ ticker +'240.pkl', 'rb') as handle:
            clf = pickle.load(handle)
            
        with open('meta_files/240minall_trading_news_fixed.pickle', 'rb') as handle: # change file according to hour threshold
            trading_news = pickle.load(handle)
            
        with open('meta_files/gui_models/features_mask_'+ ticker +'240_1000.pkl', 'rb') as handle:
            mask = pickle.load(handle)
    
        
        key_found = (min(list(trading_news.keys()), key=lambda d: get_nearest(d, orig_dt)))
        print("key_found is ", key_found)
        result[ticker].setdefault('trade_time',key_found)
        features_array = []
        for item in trading_news[key_found]:
            if item in news:
                idx = news.index(item)
                arr = all_occurance[idx].todense()
                raveled = np.asarray(arr).ravel()
                features_array.append(raveled)
             
        features_array = np.array(features_array)
        print("features_array shape is ", features_array.shape)
        new_features = features_array[:, mask]
    
        preds = []
        for news_art in new_features:
            preds.append(clf.predict([news_art])[0])
            
        result[ticker].setdefault('direction',int(mode(preds)))
    return result
#%%
# =============================================================================
# comment below if needed
# =============================================================================
# result = get_direc(ticker_gms, orig_dt)
# print(result)
# with open("direction_result.json", "w",encoding='utf8') as outfile:
#     json.dump(result, outfile, indent=4,ensure_ascii=False)