# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Field(Column) in CSV.
"""
import datetime
#---------------------------------------------------------
def csvcol_deleteCollumns(source, columnNumbers):
    # 削除対象列のcolNumbersを降順に並べる
    columnNumbers.sort()
    columnNumbers.reverse()
    
    # 列削除
    for colNum in columnNumbers:
        for row in source:
            #2列目を削除したい場合[2]が渡されるので、-1する。
            row.pop(colNum-1)
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
##### 指定した列を上からすべて検索し、要素ごとに出現する回数をカウントしたリストを作成する。 ####
def csvcol_countEvery(source, columnNumber):
    idx = columnNumber - 1
    d = {}
    isFirst = True
    for row in source:
        if isFirst == True:
            isFirst = False
            continue
        
        item = row[idx]
        if item in d:
            d[item] = d[item] + 1
        else:
            d[item] = 1
    # 辞書オブジェクトをリストのリストに変換
    l = [list(x)  for x in d.items()]
    return 1, l

#---------------------------------------------------------
##### 指定した２列を上からすべて検索し、2列の要素をペアとして、出現する回数をカウントしたリストを作成する。 ####
def csvcol_countEvery_TowColumns(source, columnNumber1, columnNumber2):
    idx1 = columnNumber1 - 1
    idx2 = columnNumber2 - 1
    d = {}
    isFirst = True
    
    #　separator文字列を作成
    now = datetime.datetime.now()
    separator = "_{0:%Y%m%d-%H%M%S}_".format(now)
    
    for row in source:
        if isFirst == True:
            isFirst = False
            continue
        
        item1 = row[idx1]
        item2 = row[idx2]
        item = str(item1) + separator + str(item2)
        
        # 列１、列２の値をseparatorで連結してkeyとして辞書オブジェクトに登録。
        if item in d:
            d[item] = d[item] + 1
        else:
            d[item] = 1
            
    # 辞書オブジェクトをリストのリストに変換。keyをseparatorで分割する。
    l = [[row[0].split(separator)[0], row[0].split(separator)[1], row[1]] for row in d.items()]

    return 1, l

#============================ 
if __name__=='__main__':
    pass
        