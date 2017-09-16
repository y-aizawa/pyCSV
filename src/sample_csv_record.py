# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Record in CSV.
"""
from sample_csv_file import csvfl_csvToList
from sample_csv_file import csvfl_listToCsv
import numpy as np
import random
import math
import copy

#---------------------------------------------------------
def csvrec_deleteRecords(source, recNumbers):   
    # 削除対象行のrecordNumbers降順に並べる
    recNumbers.sort()
    recNumbers.reverse()
    # 各要素に1を引く。recordIndexesはrecord 1,2,3を削除したい場合[1,2,3]となっているため。
    recIndexes = [x - 1 for x in recNumbers]
    # 行削除
    for idx in recIndexes:
        del source[idx]

    return 1, source, np.array(source).shape[0], np.array(source).shape[1]

#---------------------------------------------------------
def csvrec_matchRecordIndexes(source, targetFieldNumber, key):
    # index
    indexes = []
    for i, x in enumerate(source):
        if x[targetFieldNumber -1] == key:
            indexes.append(i)
    recNumbers = [x + 1 for x in indexes]

    return 1, recNumbers

#---------------------------------------------------------
def csvrec_sampling(source, samplingRatio):
    # headerを確保
    header = copy.deepcopy(source[0])
    # sourceからheadderを削除
    result, sourceWOHeader, countRows, countFields = csvrec_deleteRecords(source, [1])
    # サンプリング数の計算
    numberOfSamples = math.ceil(countRows * samplingRatio)    
    # サンプリング対象Indexを取得
    tgtIndex = random.sample(range(countRows), numberOfSamples)
    # サンプリング
    samples = [sourceWOHeader[i] for i in tgtIndex]
    # ヘッダを挿入
    samples.insert(0, header)
    
    return 1, samples, numberOfSamples + 1, np.array(samples).shape[1]

#============================ 
if __name__=='__main__':
    
    csvFullPath = r'C:\work\GitHub\pyCSV\data\sample_data.CSV'
    newData = []
    countRows = 0
    countFields = 0
    print('>>> start : csvfl_csvToList')
    result, newData, countRows, countFields = csvfl_csvToList (csvFullPath)
    print('The number of rows in original csv is ...' + str(countRows))
    print('The number of Fields in original csv is ...' + str(countFields))
    print('<<< finish : csvfl_csvToList')
    
#    print('')
#    print('>>> start : csvrec_deleteRecords')
#    result, newData, countRows, countFields = csvrec_sampling(newData, 0.01)
#    print('The number of rows in original csv is ...' + str(countRows))
#    print('The number of Fields in original csv is ...' + str(countFields))
#    print('<<< finish : csvrec_deleteRecords')

    print('')
    print('>>> start : csvrec_matchRecordIndexes')
    result, indexes = csvrec_matchRecordIndexes(newData, 2, '山口県')
    print('The number of rows in original csv is ...' + str(indexes))
    print('<<< finish : csvrec_matchRecordIndexes')
  
    print('')
    print('>>> start : csvrec_deleteRecords')
    result, newData, countRows, countFields = csvrec_deleteRecords(newData, indexes)
    print('The number of rows in original csv is ...' + str(countRows))
    print('The number of Fields in original csv is ...' + str(countFields))
    print('<<< finish : csvrec_deleteRecords')

    directory = r'C:\work\GitHub\pyCSV\data\_'
    newName = ""
    print('')
    print('>>> start : csvfl_listToCsv')
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "newCsv")
    print('The new file name is ...' + newName)
    print('The number of rows in the new csv is ...' + str(countRows))
    print('>>> finish : csvfl_listToCsv')
    