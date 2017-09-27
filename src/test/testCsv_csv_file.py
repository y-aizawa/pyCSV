# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_file.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
from csv_file import csvfl_csvToList
from csv_file import csvfl_listToCsv

newData = []
dataDir = r"C:\work\GitHub\pyCSV\data"
dataDirErr = r"C:\work\GitHub\pyCSV\datadata"

csvFullPath = dataDir + r'\sample_data.CSV'
csvFullPathNotExist = dataDir + r'\sample_dataError.CSV'
csvFullPathEmpty = dataDir + r'\empty_data.CSV'
csvFullPathErr = dataDir + r'\err:::.CSV'

import datetime
now = datetime.datetime.now()
newCsvName = "newCsv_{0:%Y%m%d-%H%M%S}.csv".format(now)

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testCsv_csvfl_csvToList_1(self):
        countRows = 0
        countColumns = 0
        global newData
        result, msg, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        self.assertEqual((1, "Complete.", 124118, 7), (result, msg, countRows, countColumns))
        
    def testCsv_csvfl_csvToList_2(self):
        result, msg, newData, countRows, countColumns = csvfl_csvToList ("")
        self.assertEqual((0, "Error : Cannot find the CSV file specified. []",0, 0), (result, msg, countRows, countColumns))        
        
    def testCsv_csvfl_csvToList_3(self):
        result, msg, newData, countRows, countColumns = csvfl_csvToList (csvFullPathNotExist)
        self.assertEqual((0, "Error : Cannot find the CSV file specified. [C:\work\GitHub\pyCSV\data\sample_dataError.CSV]", 0, 0), (result, msg, countRows, countColumns))           
        
    def testCsv_csvfl_csvToList_4(self):
        result, msg, newData, countRows, countColumns = csvfl_csvToList (csvFullPathEmpty)
        self.assertEqual((0, "Error : The file specified was empty.", 0, 0), (result, msg, countRows, countColumns)) 
        
    def testCsv_csvfl_listToCsv_1(self):
        global newData
        directory = dataDir + "\\"
        result, msg, newName = csvfl_listToCsv (newData, True, directory, newCsvName)
        print('listToCsv_1 : created file name is : => ' + newName)        
        self.assertEqual((1, "Complete."), (result, msg))
        
  
    def testCsv_csvfl_listToCsv_1_2(self):
        global newData
        directory = dataDir + "\\"
        result, msg, newName = csvfl_listToCsv (newData, True, directory, "sample_data.CSV")
        print('listToCsv_1_2 : created file name is : => ' + newName)        
        self.assertEqual((1, "Complete.",  "sample_data(1).CSV"), (result, msg, newName))
        
    def testCsv_csvfl_listToCsv_2(self):
        directory = dataDir + "\\"
        result, msg, newName = csvfl_listToCsv ([], True, directory, newCsvName)
        self.assertEqual((0, "Error : The source was empty.", ""), (result, msg, newName))

    def testCsv_csvfl_listToCsv_3(self):
        global newData
        directory = dataDir + "\\"
        result, msg, newName = csvfl_listToCsv (newData, True, directory, csvFullPathErr)
        self.assertEqual((0, "Error : Invalid CSV file name. [C:\work\GitHub\pyCSV\data\err:::.CSV]", ""), (result, msg, newName))
        
    def testCsv_csvfl_listToCsv_4(self):
        global newData
        directory = dataDirErr + "\\"
        result, msg, newName = csvfl_listToCsv (newData, True, directory, newCsvName)
        self.assertEqual((0, "Error : Cannot find the directory specified. [C:\work\GitHub\pyCSV\datadata\]", ""), (result, msg, newName))        
                
if __name__=='__main__':
    unittest.main()
