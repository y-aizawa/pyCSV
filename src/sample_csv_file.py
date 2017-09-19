# -*- coding: utf-8 -*-
"""
Modules manipulate a csv file.
"""
import csv   #csvモジュールをインポートする
import datetime
import numpy as np

#---------------------------------------------------------
def csvfl_csvToList (csvFullPath):
    
    f = open(csvFullPath, 'r')
    dataReader = csv.reader(f)
    newData = []
    for row in dataReader:
        newData.append(row)

    return 1, newData, np.array(newData).shape[0], np.array(newData).shape[1]

#---------------------------------------------------------
def csvfl_listToCsv (source, ovwFlag, directory, csvName):

    now = datetime.datetime.now()
    newName = directory + csvName + "_{0:%Y%m%d-%H%M%S}.csv".format(now)
    # ファイルが無ければ作る、の'a'を指定
    # newLine=''が無いと、空の行が一行おきに出てしまう。
    f = open(newName, 'a', newline='') 
    
    # ファイルオープン  H27のデータは""はついていないが、""付で処理する。
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    i = 0
    for line in source:
        writer.writerow(line)
        i+=1

    countRows = i
    
    # ファイルクローズ
    f.close()
    return 1, newName, countRows

#============================ 
if __name__=='__main__':
    pass