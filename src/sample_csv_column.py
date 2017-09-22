# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Field(Column) in CSV.
"""
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
##### 指定した列に含まれる要素の種類を抽出し数をカウント。辞書オブジェクトにする。 ####
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

#============================ 
if __name__=='__main__':
    pass
