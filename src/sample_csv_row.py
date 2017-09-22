# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Record in CSV.
"""
import random
import math
import copy

#---------------------------------------------------------
def csvrec_deleteRows(source, rowNumbers):   
    # 削除対象行のrecordNumbers降順に並べる
    rowNumbers.sort()
    rowNumbers.reverse()
    
    # 各要素に1を引く。recordIndexesはrecord 1,2,3を削除したい場合[1,2,3]となっているため。
    rowIndexes = [x - 1 for x in rowNumbers]

    # 行削除
    for idx in rowIndexes:
        del source[idx]
        
    #　行数、列数計算
    r = 0
    c = 0
    for row in source:
        r += 1
        if c < len(row):
            c = len(row)
            
    # sourceが大きいとMemoryErrorが出てしまうため、処理を変更。
    # return 1, source, np.array(source).shape[0], np.array(source).shape[1]
    
    return 1, source, r, c

#---------------------------------------------------------
def csvrec_matchRowNumbers(source, targetColumnNumber, key):
    # index
    indexes = []
    for i, x in enumerate(source):
        if x[targetColumnNumber -1] == key:
            indexes.append(i)
    rowNumbers = [x + 1 for x in indexes]

    return 1, rowNumbers

#---------------------------------------------------------
def csvrec_sampling(source, samplingRatio):
    # headerを確保
    header = copy.deepcopy(source[0])
    # sourceからheadderを削除
    result, sourceWOHeader, countRows, countFields = csvrec_deleteRows(source, [1])
    # サンプリング数の計算
    numberOfSamples = math.ceil(countRows * samplingRatio)    
    # サンプリング対象Indexを取得
    tgtIndex = random.sample(range(countRows), numberOfSamples)
    # サンプリング
    samples = [sourceWOHeader[i] for i in tgtIndex]
    # ヘッダを挿入
    samples.insert(0, header)
    
    return 1, samples, numberOfSamples + 1, len(header)

#============================ 
if __name__=='__main__':
    pass


    