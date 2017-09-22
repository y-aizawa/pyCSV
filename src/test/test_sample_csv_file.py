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

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_csvfl_csvToList(self):
        csvFullPath = r'C:\work\pyCSV\data\sample_data.CSV'
        countRows = 0
        countColumns = 0
        global newData
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        self.assertEqual((1, 124118, 7), (result, countRows, countColumns))

    def test_csvfl_listToCsv(self):
        global newData
        directory = r'C:\work\pyCSV\data\_'
        result, newName, countRows = csvfl_listToCsv (newData, True, directory, "newCsv")
        self.assertEqual((1, 124118), (result, countRows))
        print('### The following file is created. => ' + newName)
        
if __name__=='__main__':
    unittest.main()
