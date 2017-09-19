# -*- coding: utf-8 -*-
"""
Modules manipulate a LIST which was converted from a CSV file.
The data will be manipulated in a LIST are equivalent to Field(Column) in CSV.
"""
import numpy as np

#---------------------------------------------------------
def csvfld_deleteCollumns(source, columnNumbers):
    # 削除対象列のcolNumbersを降順に並べる
    columnNumbers.sort()
    columnNumbers.reverse()
    
    # 列削除
    for colNum in columnNumbers:
        for row in source:
            #2列目を削除したい場合[2]が渡されるので、-1する。
            row.pop(colNum-1)

    return 1, source, np.array(source).shape[0], np.array(source).shape[1]

#============================ 
if __name__=='__main__':
    pass
