# -*- coding: utf-8 -*-
"""
Unit test for csv_column.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
import pandas
import time

# import function
from csv_column import csvcol_getHeaderColumnNumber
from csv_column import csvcol_getHeaderName
from csv_column import csvcol_deleteColumn
from csv_column import csvcol_deleteColumns
from csv_column import csvcol_duplicateColumn
from csv_column import csvcol_countEvery
from csv_column import csvcol_fillRandomNumber
from csv_column import csvcol_fillSequentialNumber
from pandas.util.testing import assert_frame_equal
from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv

dataPath = r".\data\sample_large_data.csv"
dataDir =  r".\data"

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    #  csv_fileとの連携テスト
    def testCsv_csvcol_combined_test(self):
        result, msg, source, countRows, countColumns = csvfl_csvToDataFrame (dataPath, 1)
        
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "町村")
        self.assertEqual((1, "Complete.", 4), (result, msg, headerColumnNumber))

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, [2,5])
        self.assertEqual((1, "Complete.", 48, 3), (result, msg, countRows, countColumns)) 

        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_1.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_1.csv"), (result, msg, newName))        
        
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, [6,4,2])
        self.assertEqual((1, "Complete.", countRows, 4), (result, msg, countRows, countColumns))
        
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 1, 0, "Duplicated")
        self.assertEqual((1, "Complete.", countRows, 5), (result, msg, countRows, countColumns))
        
        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_2.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_2.csv"), (result, msg, newName))
        
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, [1,3,5], 8, True, True)
        self.assertEqual((1, "Complete.", countRows, countColumns), (result, msg, countRows, countColumns))
        
        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_3.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_3.csv"), (result, msg, newName))
        
        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(source, [1,3,5], 8, True, True)
        self.assertEqual((1, "Complete.", countRows, countColumns), (result, msg, countRows, countColumns))
        
        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_4.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_4.csv"), (result, msg, newName))

        
# PG_21
    # sourceのformatが不正
    def testCsv_csvcol_getHeaderColumnNumber1(self):
        source = []
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "Test")
        self.assertEqual((0, "Error : The source was invalid format.", 0), (result, msg, headerColumnNumber))

    # sourceがNULL
    def testCsv_csvcol_getHeaderColumnNumber2(self):
        sourceNull = pandas.DataFrame()
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(sourceNull, "Test")
        self.assertEqual((0, "Error : The source was empty.", 0), (result, msg, headerColumnNumber))

    # [headerName]が[string]のデータ型以外の場合
    def testCsv_csvcol_getHeaderColumnNumber3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, 12345)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: headerName input 1 byte
    def testCsv_csvcol_getHeaderColumnNumber4(self):
        source = pandas.DataFrame([["集計日","教科","ヤマグチケン","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","A","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "ﾔﾏｸﾞﾁｹﾝ")
        self.assertEqual((0, "Error : Cannot find the header specified.[ﾔﾏｸﾞﾁｹﾝ]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: headerName input 2 byte
    def testCsv_csvcol_getHeaderColumnNumber5(self):
        source = pandas.DataFrame([["集計日","教科","ﾔﾏｸﾞﾁｹﾝ","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","A","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "ヤマグチケン")
        self.assertEqual((0, "Error : Cannot find the header specified.[ヤマグチケン]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    def testCsv_csvcol_getHeaderColumnNumber6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "33")
        self.assertEqual((0, "Error : Cannot find the header specified.[33]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: upper and lower values
    def testCsv_csvcol_getHeaderColumnNumber7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","abc"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "ABC")
        self.assertEqual((0, "Error : Cannot find the header specified.[ABC]", 0), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber8(self):
        source = pandas.DataFrame([["集計日","教科","ﾔﾏｸﾞﾁｹﾝ","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "ﾔﾏｸﾞﾁｹﾝ")
        self.assertEqual((1, "Complete.", 3), (result, msg, headerColumnNumber)) 

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber9(self):
        source = pandas.DataFrame([["集計日","Test","ヤマグチケン","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "ヤマグチケン")
        self.assertEqual((1, "Complete.", 3), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber10(self):
        source = pandas.DataFrame([["集計日","Test","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "集計日")
        self.assertEqual((1, "Complete.", 1), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber11(self):
        source = pandas.DataFrame([["集計日","Test","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "採点完了件数")
        self.assertEqual((1, "Complete.", 9), (result, msg, headerColumnNumber))

# PG_22
    # sourceのformatが不正
    def testCsv_csvcol_getHeaderName1(self):
        source = []
        result, msg, headerName = csvcol_getHeaderName(source, 2)
        self.assertEqual((0, "Error : The source was invalid format.", ""), (result, msg, headerName))

    # sourceがNULL
    def testCsv_csvcol_getHeaderName2(self):
        source = pandas.DataFrame()
        result, msg, headerName = csvcol_getHeaderName(source, 2)
        self.assertEqual((0, "Error : The source was empty.", ""), (result, msg, headerName))

    # [headerColumnNumber]が[int]のデータ型以外の場合
    def testCsv_csvcol_getHeaderName3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerName = csvcol_getHeaderName(source, "2")
        self.assertEqual((-1, "Error : An unexpected error occurred.", ""), (result, msg, headerName))

    # headerが見つからない
    def testCsv_csvcol_getHeaderName4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        result, msg, headerName = csvcol_getHeaderName(source, 0)
        self.assertEqual((0,"Error : The specified headerColumnNumber was out of range. [0]",""), (result, msg, headerName))

    # headerが見つからない
    def testCsv_csvcol_getHeaderName5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        result, msg, headerName = csvcol_getHeaderName(source, 10)
        self.assertEqual((0,"Error : The specified headerColumnNumber was out of range. [10]",""), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerName = csvcol_getHeaderName(source, 5)
        self.assertEqual((1,"Complete.","マーク値"), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerName = csvcol_getHeaderName(source, 1)
        self.assertEqual((1,"Complete.","集計日"), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, headerName = csvcol_getHeaderName(source, 9)
        self.assertEqual((1,"Complete.","採点完了件数"), (result, msg, headerName))


# PG_23
    # sourceのformatが不正
    def testCsv_csvcol_deleteColumn1(self):
        source = []
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 2)
        data_expected = pandas.DataFrame()
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvcol_deleteColumn2(self):
        source = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 2)
        data_expected = pandas.DataFrame()
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # [columnNumber]が[int]のデータ型以外の場合
    def testCsv_csvcol_deleteColumn3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, "2")
        data_expected = pandas.DataFrame()
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumn4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 0)
        data_expected = pandas.DataFrame()
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [0]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumn5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 10)
        data_expected = pandas.DataFrame()
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","国","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 3)
        self.assertEqual((1, "Complete.", 3, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["国","2","M","","12893","0","0","12893"],
                                          ["国","3","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 1)
        self.assertEqual((1, "Complete.", 3, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数"],
                                          ["2017-06-25","国","2","M","","12893","0","0"],
                                          ["2017-06-25","国","3","短","","12893","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 9)
        self.assertEqual((1, "Complete.", 3, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn9(self):
        source = pandas.DataFrame([["集計日"],
                                    ["2017-06-25"],
                                    ["2017-06-25"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(source, 1)
        self.assertEqual((1, "Complete.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

# PG_24
    # sourceのformatが不正
    def testCsv_csvcol_deleteColumns1(self):
        source= []
        columnNumbers = [1,6]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_deleteColumns2(self):
        source = pandas.DataFrame()
        columnNumbers = [1,6]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]が[list]のデータ型以外の場合
    def testCsv_csvcol_deleteColumns3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = 1
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumbersがNULL
    def testCsv_csvcol_deleteColumns4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvcol_deleteColumns5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [1,"6"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumns6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [0,7]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[0, 7]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumns7(self):
        source = pandas.DataFrame([
            ["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
            ["2017-06-25","国","2","M","","12893","0","0","12893"],
            ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [1,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[1, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [1,9]
        data_expected = pandas.DataFrame([["教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数"],
                                          ["国","2","M","","12893","0","0"],
                                          ["国","3","短","","12893","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((1, "Complete.", 3, 7), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [2]
        data_expected = pandas.DataFrame([["集計日","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","3","短","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((1, "Complete.", 3, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [1,2,3,4,5,6,7,8,9]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((1, "Complete.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # Compelete delete many column
    def testCsv_csvcol_deleteColumns11(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbers = [4,5,6]
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","国","2","0","0","12893"],
                                          ["2017-06-25","国","3","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(source, columnNumbers)
        self.assertEqual((1, "Complete.", 3, 6), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

# PG_25
    # sourceのformatが不正
    def testCsv_csvcol_duplicateColumn1(self):
        source = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 10, "教科")
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_duplicateColumn2(self):
        source = pandas.DataFrame()
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 10, "教科")
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumber_From]が[int]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, "2", 10, "教科")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Fromがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 0, 5, "教科")
        self.assertEqual((0, "Error : The specified columnNumber_From was out of range. [0]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Fromがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 10, 5, "教科")
        self.assertEqual((0, "Error : The specified columnNumber_From was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumber_To]が[int]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, "5", "教科")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Toがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, -1, "教科")
        self.assertEqual((0, "Error : The specified columnNumber_To was out of range. [-1]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Toがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 10, "教科")
        self.assertEqual((0, "Error : The specified columnNumber_To was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [headerName_To]が[string]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 10, 123)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # headerName_Toで指定されたヘッダ名が既に存在していた場合
    def testCsv_csvcol_duplicateColumn10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 3, "集計日")
        self.assertEqual((0, "Error : The specified headerName_To is duplicated. [集計日]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_duplicateColumn11(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","教科2","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","国","2","M","国","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","国","","12893","0","0","0"]])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 5, "教科2")
        self.assertEqual((1, "Complete.", 3, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_duplicateColumn12(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数","教科2"],
                                          ["2017-06-25","国","2","M","","12893","0","0","12893","国"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","国"]])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 2, 0, "教科2")
        self.assertEqual((1, "Complete.", 3, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（colulmnNumber_From　＝　colulmnNumber_To）
    def testCsv_csvcol_duplicateColumn13(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日2","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","2017-06-25","国","3","短","","12893","0","0","0"]])
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 1, 1, "集計日2")
        self.assertEqual((1, "Complete.", 3, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（colulmnNumber_From　＞　colulmnNumber_To）
    def testCsv_csvcol_duplicateColumn18(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        data_expected = pandas.DataFrame([["集計日","教科2","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","","国","3","短","","12893","0","0","0"]])
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(source, 5, 2, "教科2")
        self.assertEqual((1, "Complete.", 3, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

#PG_42
    # sourceのformatが不正
    def testCsv_csvcol_countEvery1(self):
        sourceNotList = []
        keyColumnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(sourceNotList, keyColumnNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_countEvery2(self):
        sourceNull = pandas.DataFrame()
        keyColumnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(sourceNull, keyColumnNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbers]が[list]のデータ型以外の場合
    def testCsv_csvcol_countEvery3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersNotList = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbersNotList)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがNULL
    def testCsv_csvcol_countEvery4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersNull = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbersNull)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbersがNULL] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvcol_countEvery5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersNNotNumber = [1,"5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbersNNotNumber)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

     # keyUniqueがsourceの範囲を超えていた
    def testCsv_csvcol_countEvery6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersOutRangeMin = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbersOutRangeMin)
        self.assertEqual((0, "Error : The specified keyColumnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

     # keyUniqueがsourceの範囲を超えていた
    def testCsv_csvcol_countEvery7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersOutRangeMax = [2,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbersOutRangeMax)
        self.assertEqual((0, "Error : The specified keyColumnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_csvcol_countEvery8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        keyColumnNumbers = [1]
        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 3, 2), (result, msg, countRows, countColumns))
        data_expected = pandas.DataFrame([["集計日","count"],
                                          ["2017-06-25","3"],
                                          ["2017-06-26","3"]])
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate column)
    def testCsv_csvcol_countEvery9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        keyColumnNumbers = [1,1,1]
        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 3, 2), (result, msg, countRows, countColumns))
        data_expected = pandas.DataFrame([["集計日","count"],
                                          ["2017-06-25","3"],
                                          ["2017-06-26","3"]])
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_countEvery10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        keyColumnNumbers = [1,2]
        data_expected = pandas.DataFrame([["集計日","教科","count"],
                                          ["2017-06-25","国","3"],
                                          ["2017-06-26","国","2"],
                                          ["2017-06-26","数","1"]])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 4, 3), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_csvcol_countEvery11(self):
        source = pandas.DataFrame([
            ["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
            ["2017-06-25","国","2","M","","12893","0","0","12893"],
            ["2017-06-25","国","3","短","","12893","0","0","0"],
            ["2017-06-25","国","4","記述	","","12893","0","0","0"],
            ["2017-06-26","国","2","M","","12323","0","0","1000"],
            ["2017-06-26","国","3","短","","12323","0","0","1000"],
            ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        keyColumnNumbers = [1,2,3,4,5,6,7,8,9]
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数","count"],
                                          ["2017-06-25","国","2","M","","12893","0","0","12893","1"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","1"],
                                          ["2017-06-25","国","4","記述	","","12893","0","0","0","1"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000","1"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000","1"],
                                          ["2017-06-26","数","8","記述	","","12323","0","0","1000","1"]])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

#Test for svcol_fillRandomNumber
    # sourceのformatが不正
    def testCsv_svcol_fillRandomNumber1(self):
        sourceNotList = []
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(sourceNotList, columnNumbers, 8, True, True)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_svcol_fillRandomNumber2(self):
        sourceNull = pandas.DataFrame()
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(sourceNull, columnNumbers, 8, True, True)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbers]が[list]のデータ型以外の場合
    def testCsv_svcol_fillRandomNumber3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbersNotList = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbersNotList, 8, True, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがNULL
    def testCsv_svcol_fillRandomNumber4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbersNull = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbersNull, 8, True, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbersがNULL] 内の要素が[int]のデータ型以外の場合
    def testCsv_svcol_fillRandomNumber5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbersNNotNumber = [1,"5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbersNNotNumber, 8, True, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

     # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillRandomNumber6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        columnNumbersOutRangeMin = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbersOutRangeMin, 8, True, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

     # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillRandomNumber7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"]])
        keyColumnNumbersOutRangeMax = [2,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, keyColumnNumbersOutRangeMax, 8, True, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_svcol_fillRandomNumber8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        columnNumbers = [1]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbers, 8, True, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))


    # 処理が問題なく完了した(duplicate column)
    def testCsv_svcol_fillRandomNumber9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        columnNumbers = [1,1,1]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbers, 8, True, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))


    # 処理が問題なく完了した（many column）
    def testCsv_svcol_fillRandomNumber10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                   ["2017-06-25","国","3","短","","12893","0","0","0"],
                                   ["2017-06-25","国","4","記述	","","12893","0","0","0"],
                                   ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                   ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                   ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        columnNumbers = [1,2]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbers, 8, True, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))

        
    # 処理が問題なく完了した（all column）
    def testCsv_svcol_fillRandomNumber11(self):
        source = pandas.DataFrame([
            ["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
            ["2017-06-25","国","2","M","","12893","0","0","12893"],
            ["2017-06-25","国","3","短","","12893","0","0","0"],
            ["2017-06-25","国","4","記述	","","12893","0","0","0"],
            ["2017-06-26","国","2","M","","12323","0","0","1000"],
            ["2017-06-26","国","3","短","","12323","0","0","1000"],
            ["2017-06-26","数","8","記述	","","12323","0","0","1000"]])
        columnNumbers = [1,2,3,4,5,6,7,8,9]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, columnNumbers, 8, True, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        
    # Case: input correct values
    # source's large size (110万行 x 700列)
    def testPerformance(self):
        result_csv, msg_csv, source, countRows_csv, countColumns_csv = csvfl_csvToDataFrame(dataPath, 1)

        # function csvcol_getHeaderColumnNumber
        start = time.time()
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(source, "headername")
        end = time.time()
        print("Time test function csvcol_getHeaderColumnNumber: " + str(end - start))

        # function csvcol_getHeaderName
        start = time.time()
        result, msg, headerName = csvcol_getHeaderName(source, 200)
        end = time.time()
        print("Time test function csvcol_getHeaderName: " + str(end - start))

        # function csvcol_deleteColumn
        start = time.time()
        result, msg, newData, countRows, countColumns = csvcol_deleteColumn(source, 2)
        end = time.time()
        print("Time test function csvcol_deleteColumn: " + str(end - start))

        # function csvcol_deleteColumns
        start = time.time()
        result, msg, newData, countRows, countColumns = csvcol_deleteColumns(source, [1,2,3,4,5,6])
        end = time.time()
        print("Time test function csvcol_deleteColumns: " + str(end - start))

        # function csvcol_duplicateColumn
        start = time.time()
        result, msg, newData, countRows, countColumns = csvcol_duplicateColumn(source, 2, 5, "教科2")
        end = time.time()
        print("Time test function csvcol_duplicateColumn: " + str(end - start))

        # function csvcol_countEvery
        start = time.time()
        result, msg, newData, countRows, countColumns = csvcol_countEvery(source, [1,2,3])
        end = time.time()
        print("Time test function csvcol_countEvery: " + str(end - start))

if __name__=='__main__':
    unittest.main()
