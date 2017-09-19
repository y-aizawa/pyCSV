# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_column.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
from sample_csv_file import csvfl_csvToList
from sample_csv_column import csvfld_deleteCollumns

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_csvfld_deleteCollumns(self):
        csvFullPath = r'C:\work\GitHub\pyCSV\data\sample_data.CSV'
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, newData, countRows, countColumns = csvfld_deleteCollumns(newData, [3,5,6])        
        self.assertEqual((1, 124118, 4), (result, countRows, countColumns))
        
if __name__=='__main__':
    unittest.main()
    
