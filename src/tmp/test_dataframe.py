# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 19:26:47 2017

@author: thuong-dp
"""

import pandas
import constants as const
import datetime

def csvfl_csvToList (csvFullPath):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    newData=[]
    countRows = 0
    countColumns = 0
    
    tp = pandas.read_csv(csvFullPath, sep=const.CSV_SEP, encoding=const.CSV_ENCODING, header=None,chunksize=10000, 
                         skipinitialspace=True, keep_default_na=False, low_memory=False, memory_map=False)
    
    df = pandas.concat(tp, ignore_index=True)

    
    #newData = df.values.tolist()
    newData = df
    
    
    countRows = df.shape[0]
    countColumns = df.shape[1]

    return result, msg, newData, countRows, countColumns

if __name__=='__main__':
    d = datetime.datetime.today()
    print("start ::: " +  d.strftime("%x %X"))
    
    # テストスイートを呼び出して実行します
    result, msg, newData, countRows, countColumns = csvfl_csvToList(r'C:\work\GitHub\pyCSV\data\_EL_公立のみ.csv')
    print(result)
    print(msg)
    print(newData)
    print(countRows)
    print(countColumns)
    
    
    d = datetime.datetime.today()
    print("finish ::: " +  d.strftime("%x %X"))
