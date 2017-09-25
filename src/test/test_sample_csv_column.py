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

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_csvcol_deleteCollumns(self):
        csvFullPath = r'C:\work\pyCSV\data\sample_data.CSV'
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, newData, countRows, countColumns = csvcol_deleteCollumns(newData, [3,5,6])        
        self.assertEqual((1, 124118, 4), (result, countRows, countColumns))
        
    def test_csvcol_countEvery(self):
        csvFullPath = r'C:\work\pyCSV\data\sample_data.CSV'
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, listCountEvery = csvcol_countEvery(newData, 2)
        self.assertEqual((1, 47, '北海道', 8251), (result, len(listCountEvery), listCountEvery[0][0],listCountEvery[0][1]))
        
    def test_csvcol_countEvery_TowColumns(self):
        csvFullPath = r'C:\work\pyCSV\data\sample_data.CSV'
        countRows = 0
        countColumns = 0
        newData = []
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, listCountEvery = csvcol_countEvery_TowColumns(newData, 2, 2)
        self.assertEqual((1, 47, '北海道', '北海道', 8251), (result, len(listCountEvery), listCountEvery[0][0], listCountEvery[0][1], listCountEvery[0][2]))
        
if __name__=='__main__':
    unittest.main()
    
