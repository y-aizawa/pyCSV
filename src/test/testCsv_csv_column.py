# -*- coding: utf-8 -*-
"""
Unit test for sample_csv_column.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
from csv_file import csvfl_csvToList
from csv_column import csvcol_deleteColumns


dataDir = r"C:\work\GitHub\pyCSV\data"
csvFullPath = dataDir + r'\sample_data.CSV'

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        countRows = 0
        countColumns = 0
        global newData
        result, msg, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        self.assertEqual((1, 124118, 7), (result, countRows, countColumns))
    
    def tearDown(self):
        pass
    
    def test_csvcol_deleteCollumns(self):
        countRows = 0
        countColumns = 0
        newData = []
        result, msg, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
        
        result, msg, newData, countRows, countColumns = csvcol_deleteColumns(newData, [3,5,6])        
        self.assertEqual((1, 124118, 4), (result, countRows, countColumns))
        
    def test_csvcol_countEvery(self):
        pass
        
    def test_csvcol_countEvery_TowColumns(self):
        pass
        
if __name__=='__main__':
    unittest.main()
    
    #unittest.TextTestRunner(verbosity=1).run(suite())       
    
