# -*- coding: utf-8 -*-
"""
Modules manipulate a csv file.
"""
import csv   #csvモジュールをインポートする
import datetime
import numpy as np

def csvfl_csvToList (csvFullPath ):
    
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

    
if __name__=='__main__':
    
    csvFullPath = r'C:\work\GitHub\pyCSV\data\sample_data.CSV'
    newData = []
    countRows = 0
    countColumns = 0
    print('>>> start : csvfl_csvToList')
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print('The number of rows in original csv is ...' + str(countRows))
    print('The number of columns in original csv is ...' + str(countColumns))
    print('<<< finish : csvfl_csvToList')
    
    directory = r'C:\work\GitHub\pyCSV\data\_'
    newName = ""
    print('')
    print('>>> start : csvfl_listToCsv')
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "newCsv")
    print('The new file name is ...' + newName)
    print('The number of rows in the new csv is ...' + str(countRows))
    print('>>> finish : csvfl_listToCsv')
    