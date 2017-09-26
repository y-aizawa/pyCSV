# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_file.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
from sample_csv_file import csvfl_csvToList
from sample_csv_file import csvfl_listToCsv

newData = []
dataDir = r"C:\work\GitHub\pyCSV\data"
csvFullPath = dataDir + r'\sample_data.CSV'

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_csvfl_csvToList(self):
        countRows = 0
        countColumns = 0
        global newData
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        self.assertEqual((1, 124118, 7), (result, countRows, countColumns))

    def test_csvfl_listToCsv(self):
        global newData
        directory = dataDir + "\\"
        result, newName, countRows = csvfl_listToCsv (newData, True, directory, "newCsv")
        self.assertEqual((1, 124118), (result, countRows))
        print('### The following file is created. => ' + newName)
        
if __name__=='__main__':
    unittest.main()
