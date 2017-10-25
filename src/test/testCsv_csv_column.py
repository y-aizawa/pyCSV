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
from csv_column import csvcol_deleteColumnsExcept
from csv_column import csvcol_getHeaderColumnNumberPartialMatch
from csv_column import csvcol_fillRandomNumber
from csv_column import csvcol_fillSequentialNumber
from pandas.util.testing import assert_frame_equal
from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv

dataPath = r".\data\sample_large_data.csv"
dataDir =  r".\data"

class TestCsvColumn(unittest.TestCase):
    def setUp(self):
        self.source_empty = pandas.DataFrame()

        self.source_invalid = [["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"],
                               ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]

        self.source = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                        ["2017-06-25","国","3","短","","12893","0","0","0"],
                                        ["2017-06-25","国","4","記述","","12893","0","0","0"],
                                        ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                        ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                        ["2017-06-26","数","8","記述","","12323","0","0","1000"]],
                                        columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        self.source_header_number = pandas.DataFrame([["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"],
                                                      ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                                      ["2017-06-25","国","3","短","","12893","0","0","0"],
                                                      ["2017-06-25","国","4","記述","","12893","0","0","0"],
                                                      ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                                      ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                                      ["2017-06-26","数","8","記述","","12323","0","0","1000"]],
                                                      columns=[1,2,3,4,5,6,7,8,9])

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

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(source, [1,3,5], 8, True)
        self.assertEqual((1, "Complete.", countRows, countColumns), (result, msg, countRows, countColumns))

        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_3.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_3.csv"), (result, msg, newName))

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(source, [1,3,5], 8, True)
        self.assertEqual((1, "Complete.", countRows, countColumns), (result, msg, countRows, countColumns))

        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvcol_combined_test_4.csv")
        self.assertEqual((1, "Complete.",  "output_csvcol_combined_test_4.csv"), (result, msg, newName))

# PG_21
    # sourceのformatが不正
    def testCsv_csvcol_getHeaderColumnNumber1(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source_invalid, "ﾔﾏｸﾞﾁｹﾝ")
        self.assertEqual((0, "Error : The source was invalid format.", 0), (result, msg, headerColumnNumber))

    # sourceがNULL
    def testCsv_csvcol_getHeaderColumnNumber2(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source_empty, "ﾔﾏｸﾞﾁｹﾝ")
        self.assertEqual((0, "Error : The source was empty.", 0), (result, msg, headerColumnNumber))

    # [headerName]が[string]のデータ型以外の場合
    def testCsv_csvcol_getHeaderColumnNumber3(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, 12345)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: headerName input 1 byte
    def testCsv_csvcol_getHeaderColumnNumber4(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "ﾃｽﾄ")
        self.assertEqual((0, "Error : Cannot find the header specified.[ﾃｽﾄ]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: headerName input 2 byte
    def testCsv_csvcol_getHeaderColumnNumber5(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "ヤマグチケン")
        self.assertEqual((0, "Error : Cannot find the header specified.[ヤマグチケン]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    def testCsv_csvcol_getHeaderColumnNumber6(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "33")
        self.assertEqual((0, "Error : Cannot find the header specified.[33]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    # Error: upper and lower values
    def testCsv_csvcol_getHeaderColumnNumber7(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "ABC")
        self.assertEqual((0, "Error : Cannot find the header specified.[ABC]", 0), (result, msg, headerColumnNumber))

    # headerが見つからない
    def testCsv_csvcol_getHeaderColumnNumber8(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source_header_number, "9")
        self.assertEqual((0, "Error : Cannot find the header specified.[9]", 0), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber9(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "設問番号")
        self.assertEqual((1, "Complete.", 3), (result, msg, headerColumnNumber)) 

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber10(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "集計日")
        self.assertEqual((1, "Complete.", 1), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderColumnNumber11(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumber(self.source, "abc")
        self.assertEqual((1, "Complete.", 9), (result, msg, headerColumnNumber))

# PG_22
    # sourceのformatが不正
    def testCsv_csvcol_getHeaderName1(self):
        result, msg, headerName = csvcol_getHeaderName(self.source_invalid, 2)
        self.assertEqual((0, "Error : The source was invalid format.", ""), (result, msg, headerName))

    # sourceがNULL
    def testCsv_csvcol_getHeaderName2(self):
        result, msg, headerName = csvcol_getHeaderName(self.source_empty, 2)
        self.assertEqual((0, "Error : The source was empty.", ""), (result, msg, headerName))

    # [headerColumnNumber]が[int]のデータ型以外の場合
    def testCsv_csvcol_getHeaderName3(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, "2")
        self.assertEqual((-1, "Error : An unexpected error occurred.", ""), (result, msg, headerName))

    # headerが見つからない
    def testCsv_csvcol_getHeaderName4(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, 0)
        self.assertEqual((0,"Error : The specified headerColumnNumber was out of range. [0]",""), (result, msg, headerName))

    # headerが見つからない
    def testCsv_csvcol_getHeaderName5(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, 10)
        self.assertEqual((0,"Error : The specified headerColumnNumber was out of range. [10]",""), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName6(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, 5)
        self.assertEqual((1,"Complete.","白紙検出数"), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName7(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, 1)
        self.assertEqual((1,"Complete.","集計日"), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName8(self):
        result, msg, headerName = csvcol_getHeaderName(self.source, 9)
        self.assertEqual((1,"Complete.","abc"), (result, msg, headerName))

    # 処理が問題なく完了した
    def testCsv_csvcol_getHeaderName9(self):
        result, msg, headerName = csvcol_getHeaderName(self.source_header_number, 9)
        self.assertEqual((1,"Complete.", 9), (result, msg, headerName))

# PG_23
    # sourceのformatが不正
    def testCsv_csvcol_deleteColumn1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source_invalid, 2)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvcol_deleteColumn2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source_empty, 2)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # [columnNumber]が[int]のデータ型以外の場合
    def testCsv_csvcol_deleteColumn3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, "2")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumn4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, 0)
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [0]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumn5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, 10)
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn6(self):
        data_expected = pandas.DataFrame([["2017-06-25","国","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","短","","12893","0","0","0"],
                                          ["2017-06-25","国","記述","","12893","0","0","0"],
                                          ["2017-06-26","国","M","","12323","0","0","1000"],
                                          ["2017-06-26","国","短","","12323","0","0","1000"],
                                          ["2017-06-26","数","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, 3)
        self.assertEqual((1, "Complete.", 7, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn7(self):
        data_expected = pandas.DataFrame([["国","2","M","","12893","0","0","12893"],
                                          ["国","3","短","","12893","0","0","0"],
                                          ["国","4","記述","","12893","0","0","0"],
                                          ["国","2","M","","12323","0","0","1000"],
                                          ["国","3","短","","12323","0","0","1000"],
                                          ["数","8","記述","","12323","0","0","1000"]],
                                          columns=["採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, 1)
        self.assertEqual((1, "Complete.", 7, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn8(self):
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0"],
                                          ["2017-06-25","国","3","短","","12893","0","0"],
                                          ["2017-06-25","国","4","記述","","12893","0","0"],
                                          ["2017-06-26","国","2","M","","12323","0","0"],
                                          ["2017-06-26","国","3","短","","12323","0","0"],
                                          ["2017-06-26","数","8","記述","","12323","0","0"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source, 9)
        self.assertEqual((1, "Complete.", 7, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumn9(self):
        data_expected = pandas.DataFrame([["集計日","採点完了件数","設問番号","設問種別","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"],
                                          ["2017-06-25","国","2","M","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","12893","0","0","0"],
                                          ["2017-06-25","国","4","記述","12893","0","0","0"],
                                          ["2017-06-26","国","2","M","12323","0","0","1000"],
                                          ["2017-06-26","国","3","短","12323","0","0","1000"],
                                          ["2017-06-26","数","8","記述","12323","0","0","1000"]],
                                          columns=[1,2,3,4,6,7,8,9])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumn(self.source_header_number, 5)
        self.assertEqual((1, "Complete.", 8, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

# PG_24
    # sourceのformatが不正
    def testCsv_csvcol_deleteColumns1(self):
        columnNumbers = [1,6]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source_invalid, columnNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_deleteColumns2(self):
        columnNumbers = [1,6]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source_empty, columnNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]が[list]のデータ型以外の場合
    def testCsv_csvcol_deleteColumns3(self):
        columnNumbers = 1
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumbersがNULL
    def testCsv_csvcol_deleteColumns4(self):
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvcol_deleteColumns5(self):
        columnNumbers = [1,"6"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumns6(self):
        columnNumbers = [0,7]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[0, 7]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumns7(self):
        columnNumbers = [1,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[1, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns8(self):
        columnNumbers = [1,9]
        data_expected = pandas.DataFrame([["国","2","M","","12893","0","0"],
                                          ["国","3","短","","12893","0","0"],
                                          ["国","4","記述","","12893","0","0"],
                                          ["国","2","M","","12323","0","0"],
                                          ["国","3","短","","12323","0","0"],
                                          ["数","8","記述","","12323","0","0"]],
                                          columns=["採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 7), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns9(self):
        columnNumbers = [2]
        data_expected = pandas.DataFrame([["2017-06-25","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","3","短","","12893","0","0","0"],
                                          ["2017-06-25","4","記述","","12893","0","0","0"],
                                          ["2017-06-26","2","M","","12323","0","0","1000"],
                                          ["2017-06-26","3","短","","12323","0","0","1000"],
                                          ["2017-06-26","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 8), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns10(self):
        columnNumbers = [7,8,9,1,2,3,4,5,6,]
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_deleteColumns11(self):
        columnNumbers = [5, 8, 2, 4, 1]
        data_expected = pandas.DataFrame([["設問番号","取込済解答数","テスト","abc"],
                                          ["2","12893","0","12893"],
                                          ["3","12893","0","0"],
                                          ["4","12893","0","0"],
                                          ["2","12323","0","1000"],
                                          ["3","12323","0","1000"],
                                          ["8","12323","0","1000"]],
                                          columns=[3,6,7,9])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source_header_number, columnNumbers)
        self.assertEqual((1, "Complete.", 8, 4), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # Compelete delete many column
    def testCsv_csvcol_deleteColumns12(self):
        columnNumbers = [5,4,6]
        data_expected = pandas.DataFrame([["2017-06-25","国","2","0","0","12893"],
                                          ["2017-06-25","国","3","0","0","0"],
                                          ["2017-06-25","国","4","0","0","0"],
                                          ["2017-06-26","国","2","0","0","1000"],
                                          ["2017-06-26","国","3","0","0","1000"],
                                          ["2017-06-26","数","8","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 6), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # Compelete delete many column
    def testCsv_csvcol_deleteColumns13(self):
        columnNumbers = [4, 5, 6]
        data_expected = pandas.DataFrame([["集計日","採点完了件数","設問番号","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"],
                                          ["2017-06-25","国","2","0","0","12893"],
                                          ["2017-06-25","国","3","0","0","0"],
                                          ["2017-06-25","国","4","0","0","0"],
                                          ["2017-06-26","国","2","0","0","1000"],
                                          ["2017-06-26","国","3","0","0","1000"],
                                          ["2017-06-26","数","8","0","0","1000"]],
                                          columns=[1,2,3,7,8,9])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumns(self.source_header_number, columnNumbers)
        self.assertEqual((1, "Complete.", 8, 6), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

# PG_25
    # sourceのformatが不正
    def testCsv_csvcol_duplicateColumn1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source_invalid, 2, 10, "採点完了件数")
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_duplicateColumn2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source_empty, 2, 10, "採点完了件数")
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumber_From]が[int]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, "2", 10, "採点完了件数")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Fromがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 0, 5, "採点完了件数")
        self.assertEqual((0, "Error : The specified columnNumber_From was out of range. [0]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Fromがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 10, 5, "採点完了件数")
        self.assertEqual((0, "Error : The specified columnNumber_From was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumber_To]が[int]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, "5", "採点完了件数")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Toがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn7(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, -1, "採点完了件数")
        self.assertEqual((0, "Error : The specified columnNumber_To was out of range. [-1]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumber_Toがsourceの範囲を超えていた
    def testCsv_csvcol_duplicateColumn8(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, 10, "採点完了件数")
        self.assertEqual((0, "Error : The specified columnNumber_To was out of range. [10]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [headerName_To]が[string]のデータ型以外の場合
    def testCsv_csvcol_duplicateColumn9(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, 10, 123)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # headerName_Toで指定されたヘッダ名が既に存在していた場合
    def testCsv_csvcol_duplicateColumn10(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, 3, "集計日")
        self.assertEqual((0, "Error : The specified headerName_To is duplicated. [集計日]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_duplicateColumn11(self):
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","国","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","国","","12893","0","0","0"],
                                          ["2017-06-25","国","4","記述","国","","12893","0","0","0"],
                                          ["2017-06-26","国","2","M","国","","12323","0","0","1000"],
                                          ["2017-06-26","国","3","短","国","","12323","0","0","1000"],
                                          ["2017-06-26","数","8","記述","数","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","採点完了件数2","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, 5, "採点完了件数2")
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_duplicateColumn12(self):
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893","国"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","国"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0","国"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000","国"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000","国"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000","数"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc","採点完了件数2"])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 2, 0, "採点完了件数2")
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した
    def testCsv_csvcol_duplicateColumn13(self):
        data_expected = pandas.DataFrame([["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc","採点完了件数"],
                                          ["2017-06-25","国","2","M","","12893","0","0","12893","国"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","国"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0","国"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000","国"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000","国"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000","数"]],
                                          columns=[1,2,3,4,5,6,7,8,9,"10"])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source_header_number, 2, 0, "10")
        self.assertEqual((1, "Complete.", 8, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（colulmnNumber_From　＝　colulmnNumber_To）
    def testCsv_csvcol_duplicateColumn14(self):
        data_expected = pandas.DataFrame([["2017-06-25","2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","2017-06-25","国","3","短","","12893","0","0","0"],
                                          ["2017-06-25","2017-06-25","国","4","記述","","12893","0","0","0"],
                                          ["2017-06-26","2017-06-26","国","2","M","","12323","0","0","1000"],
                                          ["2017-06-26","2017-06-26","国","3","短","","12323","0","0","1000"],
                                          ["2017-06-26","2017-06-26","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日2","集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 1, 1, "集計日2")
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（colulmnNumber_From　＞　colulmnNumber_To）
    def testCsv_csvcol_duplicateColumn15(self):
        data_expected = pandas.DataFrame([["2017-06-25","","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","","国","3","短","","12893","0","0","0"],
                                          ["2017-06-25","","国","4","記述","","12893","0","0","0"],
                                          ["2017-06-26","","国","2","M","","12323","0","0","1000"],
                                          ["2017-06-26","","国","3","短","","12323","0","0","1000"],
                                          ["2017-06-26","","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数2","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_duplicateColumn(self.source, 5, 2, "採点完了件数2")
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

#PG_42
    # sourceのformatが不正
    def testCsv_csvcol_countEvery1(self):
        keyColumnNumbers = [1,2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source_invalid, keyColumnNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_countEvery2(self):
        keyColumnNumbers = [1,2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source_empty, keyColumnNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbers]が[list]のデータ型以外の場合
    def testCsv_csvcol_countEvery3(self):
        keyColumnNumbers = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがNULL
    def testCsv_csvcol_countEvery4(self):
        keyColumnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbersがNULL] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvcol_countEvery5(self):
        keyColumnNumbers = [1,"5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがsourceの範囲を超えていた
    def testCsv_csvcol_countEvery6(self):
        keyColumnNumbers = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((0, "Error : The specified keyColumnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがsourceの範囲を超えていた
    def testCsv_csvcol_countEvery7(self):
        keyColumnNumbers = [2,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((0, "Error : The specified keyColumnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_csvcol_countEvery8(self):
        keyColumnNumbers = [1]
        data_expected = pandas.DataFrame([["2017-06-25","3"],
                                          ["2017-06-26","3"]],
                                          columns = ["集計日","count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 3, 2), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate column)
    def testCsv_csvcol_countEvery9(self):
        keyColumnNumbers = [1,1,1]
        data_expected = pandas.DataFrame([["2017-06-25","3"],
                                          ["2017-06-26","3"]],
                                          columns = ["集計日","count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 3, 2), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_countEvery10(self):
        keyColumnNumbers = [1,2]
        data_expected = pandas.DataFrame([["2017-06-25","国","3"],
                                          ["2017-06-26","国","2"],
                                          ["2017-06-26","数","1"]],
                                          columns=["集計日","採点完了件数","count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 4, 3), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_countEvery11(self):
        keyColumnNumbers = [2, 3, 4]
        data_expected = pandas.DataFrame([["採点完了件数","設問番号","設問種別","1"],
                                          ["国","2","M","2"],
                                          ["国","3","短","2"],
                                          ["国","4","記述","1"],
                                          ["数","8","記述","1"]],
                                          columns = [2, 3, 4,"count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source_header_number, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 6, 4), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_csvcol_countEvery12(self):
        keyColumnNumbers = [1,2,3,4,5,6,7,8,9]
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893","1"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","1"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0","1"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000","1"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000","1"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000","1"]],
                                          columns = ["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc","count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_csvcol_countEvery13(self):
        keyColumnNumbers = [7, 3, 8, 4, 1, 5, 9, 2, 6]
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893","1"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0","1"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0","1"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000","1"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000","1"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000","1"]],
                                          columns = ["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc","count"])

        result, msg, data_actual, countRows, countColumns = csvcol_countEvery(self.source, keyColumnNumbers)
        self.assertEqual((1, "Complete.", 7, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

#PG_51
    # sourceのformatが不正
    def testCsv_csvcol_deleteColumnsExcept1(self):
        columnNumbers = [1,2,3]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source_invalid, columnNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvcol_deleteColumnsExcept2(self):
        columnNumbers = [1, 2, 3]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source_empty, columnNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]が[list]のデータ型以外の場合
    def testCsv_csvcol_deleteColumnsExcept3(self):
        columnNumbers = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # columnNumbersがNULL
    def testCsv_csvcol_deleteColumnsExcept4(self):
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]内の要素が[int]のデータ型以外の場合
    def testCsv_csvcol_deleteColumnsExcept5(self):
        columnNumbers = [1, "5", 2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]がsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumnsExcept6(self):
        columnNumbers = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [columnNumbers]がsourceの範囲を超えていた
    def testCsv_csvcol_deleteColumnsExcept7(self):
        columnNumbers = [2, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified columnNumber in the columnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_csvcol_deleteColumnsExcept8(self):
        columnNumbers = [1]
        data_expected = pandas.DataFrame([["2017-06-25"],
                                          ["2017-06-25"],
                                          ["2017-06-25"],
                                          ["2017-06-26"],
                                          ["2017-06-26"],
                                          ["2017-06-26"]],
                                          columns=["集計日"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 1), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate column)
    def testCsv_csvcol_deleteColumnsExcept9(self):
        columnNumbers = [1, 1, 6, 6, 9, 9]
        data_expected = pandas.DataFrame([["2017-06-25","12893","12893"],
                                          ["2017-06-25","12893","0"],
                                          ["2017-06-25","12893","0"],
                                          ["2017-06-26","12323","1000"],
                                          ["2017-06-26","12323","1000"],
                                          ["2017-06-26","12323","1000"]],
                                          columns=["集計日","取込済解答数","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 3), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_deleteColumnsExcept10(self):
        columnNumbers = [1, 2]
        data_expected = pandas.DataFrame([["2017-06-25","国"],
                                          ["2017-06-25","国"],
                                          ["2017-06-25","国"],
                                          ["2017-06-26","国"],
                                          ["2017-06-26","国"],
                                          ["2017-06-26","数"]],
                                          columns=["集計日","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 2), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_deleteColumnsExcept11(self):
        columnNumbers = [8, 9]
        data_expected = pandas.DataFrame([["0","12893"],
                                          ["0","0"],
                                          ["0","0"],
                                          ["0","1000"],
                                          ["0","1000"],
                                          ["0","1000"]],
                                          columns=["ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 2), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_csvcol_deleteColumnsExcept12(self):
        columnNumbers = [8, 9]
        data_expected = pandas.DataFrame([["ﾔﾏｸﾞﾁｹﾝ","abc"],
                                          ["0","12893"],
                                          ["0","0"],
                                          ["0","0"],
                                          ["0","1000"],
                                          ["0","1000"],
                                          ["0","1000"]],
                                          columns=[8, 9])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source_header_number, columnNumbers)
        self.assertEqual((1, "Complete.", 8, 2), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_csvcol_deleteColumnsExcept13(self):
        columnNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_csvcol_deleteColumnsExcept14(self):
        columnNumbers = [7, 3, 6, 4, 8, 2, 9, 1, 5]
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"],
                                          ["2017-06-25","国","4","記述","","12893","0","0","0"],
                                          ["2017-06-26","国","2","M","","12323","0","0","1000"],
                                          ["2017-06-26","国","3","短","","12323","0","0","1000"],
                                          ["2017-06-26","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_deleteColumnsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

# PG_52
    # sourceのformatが不正
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch1(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source_invalid, "設問")
        self.assertEqual((0, "Error : The source was invalid format.", []), (result, msg, headerColumnNumber))

    # sourceがNULL
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch2(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source_empty, "設問")
        self.assertEqual((0, "Error : The source was empty.", []), (result, msg, headerColumnNumber))

    # [headerName]が[string]のデータ型以外の場合
    def testCsv_csvcol_getHeaderColumnNumberPartialMatch3(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, 12345)
        self.assertEqual((-1, "Error : An unexpected error occurred.", []), (result, msg, headerColumnNumber))

    # [headerName]が[string]のデータ型以外の場合
    def testCsv_csvcol_getHeaderColumnNumberPartialMatch4(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source_header_number, "3")
        self.assertEqual((-1, "Error : An unexpected error occurred.", []), (result, msg, headerColumnNumber))

    # [headerName]が空白の場合
    def testCsv_csvcol_getHeaderColumnNumberPartialMatch5(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "")
        self.assertEqual((-1, "Error : An unexpected error occurred.", []), (result, msg, headerColumnNumber))

    # [headerName]が見つからない
    # Error: headerName input 1 byte
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch6(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "ﾃｽﾄ")
        self.assertEqual((0, "Error : Cannot find the header specified.[ﾃｽﾄ]", []), (result, msg, headerColumnNumber))

    # [headerName]が見つからない
    # Error: headerName input 2 byte
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch7(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "ヤマグチケン")
        self.assertEqual((0, "Error : Cannot find the header specified.[ヤマグチケン]", []), (result, msg, headerColumnNumber))

    # [headerName]が見つからない
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch8(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "33")
        self.assertEqual((0, "Error : Cannot find the header specified.[33]", []), (result, msg, headerColumnNumber))

    # [headerName]が見つからない
    # Error: upper and lower values
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch9(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "ABC")
        self.assertEqual((0, "Error : Cannot find the header specified.[ABC]", []), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch10(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "設問")
        self.assertEqual((1, "Complete.", [3, 4]), (result, msg, headerColumnNumber))

    # 処理が問題なく完了した
    def testCSV_csvcol_getHeaderColumnNumberPartialMatch11(self):
        result, msg, headerColumnNumber = csvcol_getHeaderColumnNumberPartialMatch(self.source, "数")
        self.assertEqual((1, "Complete.", [2, 5, 6]), (result, msg, headerColumnNumber))

#Test for svcol_fillRandomNumber
    # sourceのformatが不正
    def testCsv_svcol_fillRandomNumber1(self):
        columnNumbers = [1,2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source_invalid, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_svcol_fillRandomNumber2(self):
        columnNumbers = [1,2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source_empty, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbers]が[list]のデータ型以外の場合
    def testCsv_svcol_fillRandomNumber3(self):
        columnNumbers = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがNULL
    def testCsv_svcol_fillRandomNumber4(self):
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbersがNULL] 内の要素が[int]のデータ型以外の場合
    def testCsv_svcol_fillRandomNumber5(self):
        columnNumbers = [1,"5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillRandomNumber6(self):
        columnNumbers = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillRandomNumber7(self):
        columnNumbers = [2,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_svcol_fillRandomNumber8(self):
        columnNumbers = [1]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))

    # 処理が問題なく完了した(duplicate column)
    def testCsv_svcol_fillRandomNumber9(self):
        columnNumbers = [1,1,1]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))

    # 処理が問題なく完了した（many column）
    def testCsv_svcol_fillRandomNumber10(self):
        columnNumbers = [1,2]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))

    # 処理が問題なく完了した（all column）
    def testCsv_svcol_fillRandomNumber11(self):
        columnNumbers = [1,2,3,4,5,6,7,8,9]
        result, msg, data_actual, countRows, countColumns = csvcol_fillRandomNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))

#Test for svcol_fillSequentialNumber
    # sourceのformatが不正
    def testCsv_svcol_fillSequentialNumber1(self):
        columnNumbers = [1, 2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source_invalid, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_svcol_fillSequentialNumber2(self):
        columnNumbers = [1, 2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source_empty, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbers]が[list]のデータ型以外の場合
    def testCsv_svcol_fillSequentialNumber3(self):
        columnNumbers = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyColumnNumbersがNULL
    def testCsv_svcol_fillSequentialNumber4(self):
        columnNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [keyColumnNumbersがNULL] 内の要素が[int]のデータ型以外の場合
    def testCsv_svcol_fillSequentialNumber5(self):
        columnNumbers = [1,"5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillSequentialNumber6(self):
        columnNumbers = [0, 5]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[0, 5]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # keyUniqueがsourceの範囲を超えていた
    def testCsv_svcol_fillSequentialNumber7(self):
        columnNumbers = [2,10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((0, "Error : The specified columnNumbers was out of range. [[2, 10]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 column）
    def testCsv_svcol_fillSequentialNumber8(self):
        columnNumbers = [1]
        data_expected = pandas.DataFrame([["00000001","国","2","M","","12893","0","0","12893"],
                                          ["00000002","国","3","短","","12893","0","0","0"],
                                          ["00000003","国","4","記述","","12893","0","0","0"],
                                          ["00000004","国","2","M","","12323","0","0","1000"],
                                          ["00000005","国","3","短","","12323","0","0","1000"],
                                          ["00000006","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate column)
    def testCsv_svcol_fillSequentialNumber9(self):
        columnNumbers = [1,1]
        data_expected = pandas.DataFrame([["00000001","国","2","M","","12893","0","0","12893"],
                                          ["00000002","国","3","短","","12893","0","0","0"],
                                          ["00000003","国","4","記述","","12893","0","0","0"],
                                          ["00000004","国","2","M","","12323","0","0","1000"],
                                          ["00000005","国","3","短","","12323","0","0","1000"],
                                          ["00000006","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column）
    def testCsv_svcol_fillSequentialNumber10(self):
        columnNumbers = [1,2]
        data_expected = pandas.DataFrame([["00000001","00000001","2","M","","12893","0","0","12893"],
                                          ["00000002","00000002","3","短","","12893","0","0","0"],
                                          ["00000003","00000003","4","記述","","12893","0","0","0"],
                                          ["00000004","00000004","2","M","","12323","0","0","1000"],
                                          ["00000005","00000005","3","短","","12323","0","0","1000"],
                                          ["00000006","00000006","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column）
    def testCsv_svcol_fillSequentialNumber11(self):
        columnNumbers = [1,2,3,4,5,6,7,8,9]
        data_expected = pandas.DataFrame([["00000001","00000001","00000001","00000001","00000001","00000001","00000001","00000001","00000001"],
                                          ["00000002","00000002","00000002","00000002","00000002","00000002","00000002","00000002","00000002"],
                                          ["00000003","00000003","00000003","00000003","00000003","00000003","00000003","00000003","00000003"],
                                          ["00000004","00000004","00000004","00000004","00000004","00000004","00000004","00000004","00000004"],
                                          ["00000005","00000005","00000005","00000005","00000005","00000005","00000005","00000005","00000005"],
                                          ["00000006","00000006","00000006","00000006","00000006","00000006","00000006","00000006","00000006"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, True)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate column) 0パディングなし
    def testCsv_svcol_fillSequentialNumber12(self):
        columnNumbers = [1,1]
        data_expected = pandas.DataFrame([["1","国","2","M","","12893","0","0","12893"],
                                          ["2","国","3","短","","12893","0","0","0"],
                                          ["3","国","4","記述","","12893","0","0","0"],
                                          ["4","国","2","M","","12323","0","0","1000"],
                                          ["5","国","3","短","","12323","0","0","1000"],
                                          ["6","数","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, False)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many column） 0パディングなし
    def testCsv_svcol_fillSequentialNumber13(self):
        columnNumbers = [1,2]
        data_expected = pandas.DataFrame([["1","1","2","M","","12893","0","0","12893"],
                                          ["2","2","3","短","","12893","0","0","0"],
                                          ["3","3","4","記述","","12893","0","0","0"],
                                          ["4","4","2","M","","12323","0","0","1000"],
                                          ["5","5","3","短","","12323","0","0","1000"],
                                          ["6","6","8","記述","","12323","0","0","1000"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, False)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all column） 0パディングなし
    def testCsv_svcol_fillSequentialNumber14(self):
        columnNumbers = [1,2,3,4,5,6,7,8,9]
        data_expected = pandas.DataFrame([["1","1","1","1","1","1","1","1","1"],
                                          ["2","2","2","2","2","2","2","2","2"],
                                          ["3","3","3","3","3","3","3","3","3"],
                                          ["4","4","4","4","4","4","4","4","4"],
                                          ["5","5","5","5","5","5","5","5","5"],
                                          ["6","6","6","6","6","6","6","6","6"]],
                                          columns=["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"])

        result, msg, data_actual, countRows, countColumns = csvcol_fillSequentialNumber(self.source, columnNumbers, 8, False)
        self.assertEqual((1, "Complete.", 7, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

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
