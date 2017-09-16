# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Field(Column) in CSV.
"""
from sample_csv_file import csvfl_csvToList
from sample_csv_file import csvfl_listToCsv
import numpy as np

def csvfld_deleteFields(source, fieldIndexes):
    # 削除対象列のindexを降順に並べる
    fieldIndexes.sort()
    fieldIndexes.reverse()
    
    # 列削除
    for idx in fieldIndexes:
        for row in source:
            #2列目を削除したい場合[2]が渡されるので、-1にする。
            row.pop(idx-1)

    return 1, source, np.array(source).shape[0], np.array(source).shape[1]


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
    
    print('')
    print('>>> start : csvfld_deleteFields')
    result, newData, countRows, countColumns = csvfld_deleteFields(newData, [3,5,6])
    print('The number of rows in original csv is ...' + str(countRows))
    print('The number of columns in original csv is ...' + str(countColumns))
    print('<<< finish : csvfld_deleteFields')
  
    directory = r'C:\work\GitHub\pyCSV\data\_'
    newName = ""
    print('')
    print('>>> start : csvfl_listToCsv')
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "newCsv")
    print('The new file name is ...' + newName)
    print('The number of rows in the new csv is ...' + str(countRows))
    print('>>> finish : csvfl_listToCsv')