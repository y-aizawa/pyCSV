# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_column.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
from sample_csv_file import csvfl_csvToList
from sample_csv_column import csvcol_deleteCollumns
from sample_csv_column import csvcol_countEvery
from sample_csv_column import csvcol_countEvery_TowColumns

dataDir = r"C:\work\GitHub\pyCSV\data"
csvFullPath = dataDir + r'\sample_data.CSV'

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_csvcol_deleteCollumns(self):
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, newData, countRows, countColumns = csvcol_deleteCollumns(newData, [3,5,6])        
        self.assertEqual((1, 124118, 4), (result, countRows, countColumns))
        
    def test_csvcol_countEvery(self):
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, listCountEvery = csvcol_countEvery(newData, 2)
        self.assertEqual((1, 47), (result, len(listCountEvery)))
        
    def test_csvcol_countEvery_TowColumns(self):
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, listCountEvery = csvcol_countEvery_TowColumns(newData, 1, 2)
        self.assertEqual((1, 119964), (result, len(listCountEvery)))
        
if __name__=='__main__':
    unittest.main()
    
