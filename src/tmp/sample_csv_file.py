# -*- coding: utf-8 -*-
"""
Modules manipulate a csv file.
"""
import csv   #csvモジュールをインポートする
import datetime

#---------------------------------------------------------
def csvfl_csvToList (csvFullPath):
    
    f = open(csvFullPath, 'r')
    dataReader = csv.reader(f)
    newData = []
    r=0
    c=0
    for row in dataReader:
        newData.append(row)
        r+=1
        if c < len(row):
            c = len(row)

    # sourceが大きいとMemoryErrorが出てしまうため、処理を変更。
    # return 1, newData, np.array(newData).shape[0], np.array(newData).shape[1]
    return 1, newData, r, c

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
    d = datetime.datetime.today()
    print("start ::: " +  d.strftime("%x %X"))
    
    # テストスイートを呼び出して実行します
    result, newData, countRows, countColumns = csvfl_csvToList(r'C:\work\GitHub\pyCSV\data\_EL_公立のみ.csv')
    print(result)
    print(newData)
    print(countRows)
    print(countColumns)
    
    
    d = datetime.datetime.today()
    print("finish ::: " +  d.strftime("%x %X"))