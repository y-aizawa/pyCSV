# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 14:42:40 2017

@author: fjn
"""

import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import time

from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv

if __name__=='__main__':
    print("read data...")
    start = time.time()
    csvFullPath = r"C:\Users\10007434\Desktop\folder\matome.csv"   # input path of large data file
    existHeaderFlag = 1
    result, msg, newData, countRows, countColumns = csvfl_csvToDataFrame (csvFullPath, existHeaderFlag)
    end = time.time()
    print("finish: " + str((end - start)/60) + " minutes")
    
    print("================================")
    print("write data...")
    start = time.time()
    source = newData
    ovwFlag = True
    directory = r"C:\Users\10007434\Desktop\folder"
    csvName = "test_large_data"
    result, msg, newName = csvfl_dataFrameToCsv (source, existHeaderFlag, ovwFlag, directory, csvName)
    end = time.time()
    print("finish: " + str((end - start)/60) + " minutes")
