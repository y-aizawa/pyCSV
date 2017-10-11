# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_row.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
import math
from sample_csv_file import csvfl_csvToList
from sample_csv_row import csvrec_matchRowNumbers
from sample_csv_row import csvrec_deleteRows
from sample_csv_row import csvrec_sampling

newData = []
dataDir = r"C:\work\GitHub\pyCSV\data"
csvFullPath = dataDir + '\sample_data.CSV'

class TestCsvRown(unittest.TestCase):
        
    def setUp(self):
        countRows = 0
        countColumns = 0
        global newData
        result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        self.assertEqual((1, 124118, 7), (result, countRows, countColumns))
    
    def tearDown(self):
        pass
    
    def test_csvrec_matchRowNumbers(self):
        result, rowNumbers = csvrec_matchRowNumbers(newData, 2, '山口県')     
        self.assertEqual((1, 1813), (result, len(rowNumbers)))
        
    def test_csvrec_deleteRows(self):
        global newData        
        # "山口県"の行番号を取得
        result, rowNumbers = csvrec_matchRowNumbers(newData, 2, '山口県')
        #" 山口県"の行を削除
        result, newData, countRows, countFields = csvrec_deleteRows(newData, rowNumbers)        
        self.assertEqual((1, 124118-1813, 7), (result, countRows, countFields))        

    def test_csvrec_sampling(self):
        global newData        
        result, newData, countRows, countFields = csvrec_sampling(newData, 0.01)
        self.assertEqual((1, math.ceil(124118*0.01)+1, 7), (result, countRows, countFields))  
         
if __name__=='__main__':
    unittest.main()
    
