# -*- coding: utf-8 -*-
"""
Unit test for csv_row.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
import time
import pandas
import random
import math
from pandas.util.testing import assert_frame_equal
from csv_row import csvrow_deleteRow
from csv_row import csvrow_deleteRows
from csv_row import csvrow_sampling
from csv_row import csvrow_samplingByItemInColumn
from csv_row import csvrow_matchRowNumbers
from csv_row import csvrow_deleteRowsExcept
from csv_row import csvrow_setValueInRowsSearchedByKey
from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv

dataPath = r".\data\sample_large_data.csv"
dataDir =  r".\data"

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        self.source_empty = pandas.DataFrame()

        self.source_invalid = [["集計日","採点完了件数","設問番号","設問種別","白紙検出数","取込済解答数","テスト","ﾔﾏｸﾞﾁｹﾝ","abc"],
                               ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]

        self.source = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                        ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                        ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                        ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                        ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                        ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                        ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                        ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                        ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                        ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                        ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                        columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        self.source_header_number = pandas.DataFrame([["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                                      ["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                                      ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                                      ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                                      ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                                      ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                                      ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                                      ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                                      ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                                      ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                                      ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                                      ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                                      columns=[1,2,3,4,5,6,7,8,9,10])

    def tearDown(self):
        pass

    #  csv_fileとの連携テスト
    def testCsv_csvrow_combined_test(self):
        result, msg, source, countRows, countColumns = csvfl_csvToDataFrame (dataPath, 1)

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "北海道")
        self.assertEqual((1, "Complete.", 8251),(result, msg, len(rowNumbers)))

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "愛知県")
        self.assertEqual((1, "Complete.", 7693),(result, msg, len(rowNumbers)))

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.1)
        self.assertEqual((1, "Complete.", math.ceil((124118-1) * 0.1) + 1, 7),(result, msg, countRows, countColumns))

        result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "output_csvrow_combined_test_1.csv")
        self.assertEqual((1, "Complete.",  "output_csvrow_combined_test_1.csv"), (result, msg, newName))

    # sourceのformatが不正
    def testCsv_csvrow_deleteRow1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source_invalid, 2)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_deleteRow2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source_empty, 2)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumber]が[int]のデータ型以外の場合
    def testCsv_csvrow_deleteRow3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, '2')
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumberがsourceの範囲を超えていた（rowNumber　＜　１）
    def testCsv_csvrow_deleteRow4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, 0)
        self.assertEqual((0, "Error : The specified rowNumber was out of range. [0]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumberがsourceの範囲を超えていた
    #TODO: rownumber > source's total row
    def testCsv_csvrow_deleteRow5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, 13)
        self.assertEqual((0, "Error : The specified rowNumber was out of range. [13]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumber=1の場合Errorとする
    def testCsv_csvrow_deleteRow6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, 1)
        self.assertEqual((0, "Error : Cannot delete the header row.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    def testCsv_csvrow_deleteRow7(self):
        data_expected = pandas.DataFrame([["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, 2)
        self.assertEqual((1, "Complete.", 11, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(Delete last row)
    def testCsv_csvrow_deleteRow8(self):
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source, 6)
        self.assertEqual((1, "Complete.", 11, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(Delete last row)
    def testCsv_csvrow_deleteRow9(self):
        data_expected = pandas.DataFrame([["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=[1,2,3,4,5,6,7,8,9,10])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(self.source_header_number, 8)
        self.assertEqual((1, "Complete.", 12, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

# PG_32
    # sourceのformatが不正
    def testCsv_csvrow_deleteRows1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source_invalid, [1])
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_deleteRows2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source_empty, [1])
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumbers]が[list]のデータ型以外の場合
    def testCsv_csvrow_deleteRows3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # rowNumbersがNULL
    def testCsv_csvrow_deleteRows4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [])
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvrow_deleteRows5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, ['2'])
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたrowNumbersがsourceの範囲を超えていた（rowNumbers　＜　1）
    def testCsv_csvrow_deleteRows6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [0,2])
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[0, 2]]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたrowNumbersがsourceの範囲を超えていた(rownumbers > source's total row)
    def testCsv_csvrow_deleteRows7(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [4,13])
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[4, 13]]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumbersに「1」が含まれていた場合Errorとする
    def testCsv_csvrow_deleteRows8(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [1,2])
        self.assertEqual((0, "Error : Cannot delete the header row.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(delete 1 row)
    def testCsv_csvrow_deleteRows9(self):
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [5])
        self.assertEqual((1, "Complete.", 11, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(delete many rows)
    def testCsv_csvrow_deleteRows10(self):
        data_expected = pandas.DataFrame([["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [2, 3, 6])
        self.assertEqual((1, "Complete.", 9, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(delete many rows)
    def testCsv_csvrow_deleteRows11(self):
        data_expected = pandas.DataFrame([["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=[1,2,3,4,5,6,7,8,9,10])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source_header_number, [2, 3, 6])
        self.assertEqual((1, "Complete.", 10, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(delete all rows)
    def testCsv_csvrow_deleteRows12(self):
        data_expected = pandas.DataFrame(columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected.set_axis(0, range(data_expected.shape[0]))

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.assertEqual((1, "Complete.", 1, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(delete all rows)
    def testCsv_csvrow_deleteRows13(self):
        data_expected = pandas.DataFrame(columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected.set_axis(0, range(data_expected.shape[0]))

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(self.source, [5, 3, 7, 11, 12, 4, 8, 9, 10, 2, 6])
        self.assertEqual((1, "Complete.", 1, 10),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

# PG_33
    # sourceのformatが不正
    def testCsv_csvrow_sampling1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source_invalid, 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_sampling2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source_empty, 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [samplingRatio]が[float]のデータ型以外の場合
    def testCsv_csvrow_sampling3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合（samplingRatio　＜　0）
    def testCsv_csvrow_sampling4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, -0.2)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [-0.2]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio > 1）
    def testCsv_csvrow_sampling5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 1.1)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [1.1]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 0）
    def testCsv_csvrow_sampling6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 0.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [0.0]', 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 1）
    def testCsv_csvrow_sampling7(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 1.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [1.0]', 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling8(self):
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 0.5)
        self.assertEqual((1, "Complete.", 7, 10),(result, msg, countRows, countColumns))

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling9(self):
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 0.2)
        self.assertEqual((1, "Complete.", 4, 10),(result, msg, countRows, countColumns))

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling10(self):
        source = pandas.DataFrame([["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.5)
        self.assertEqual((1, "Complete.", 1, 9),(result, msg, countRows, countColumns)) 

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling11(self):
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(self.source, 0.99)
        self.assertEqual((1, "Complete.", 11, 10),(result, msg, countRows, countColumns)) 

# PG_34
    # sourceのformatが不正
    def testCsv_csvrow_matchRowNumbers1(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source_invalid, 2, "国")
        self.assertEqual((0, "Error : The source was invalid format.", []),(result, msg, rowNumbers))

    # sourceがNULL
    def testCsv_csvrow_matchRowNumbers2(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source_empty, 2, "国")
        self.assertEqual((0, "Error : The source was empty.", []),(result, msg, rowNumbers))

    # 予期しなかったError
    # [targetColumnNumber]が[int]のデータ型以外の場合
    def testCsv_csvrow_matchRowNumbers3(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, '2', "国")
        self.assertEqual((-1, "Error : An unexpected error occurred.", []),(result, msg, rowNumbers))

    # targetColumnNumberがsourceの範囲を超えていた（targetColumnNumber　＜　１）
    def testCsv_csvrow_matchRowNumbers4(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 0, "国")
        self.assertEqual((0, "Error : The specified targetColumnNumber was out of range. [0]", []),(result, msg, rowNumbers))

    # targetColumnNumberがsourceの範囲を超えていた(rownumbers > source's total row)
    def testCsv_csvrow_matchRowNumbers5(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 13, "国")
        self.assertEqual((0, "Error : The specified targetColumnNumber was out of range. [13]", []),(result, msg, rowNumbers))

    # 予期しなかったError
    # [key]が[string]のデータ型以外の場合
    def testCsv_csvrow_matchRowNumbers6(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 2, 3)
        self.assertEqual((-1, "Error : An unexpected error occurred.", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった(Error key 1 byte, value soure 2 byte)
    def testCsv_csvrow_matchRowNumbers7(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 5, "ﾃｽﾄ")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ﾃｽﾄ, targetColumnNumber = 5]", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった(Error key 2 byte, value soure 1 byte)
    def testCsv_csvrow_matchRowNumbers8(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 5, "ヤマグチケン")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ヤマグチケン, targetColumnNumber = 5]", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった(upper and lower values)
    def testCsv_csvrow_matchRowNumbers9(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 5, "mmmmmm")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = mmmmmm, targetColumnNumber = 5]", []),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers10(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 2, '2017-06-27')
        self.assertEqual((1, "Complete.", [4, 5, 9]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers11(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 10, "10200")
        self.assertEqual((1, "Complete.", [4, 9]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers12(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source, 7, "11111")
        self.assertEqual((1, "Complete.", [3, 5, 6, 8, 10, 12]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers13(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source_header_number, 7, "11111")
        self.assertEqual((1, "Complete.", [4,6 ,7, 9, 11, 13]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers14(self):
        result, msg, rowNumbers = csvrow_matchRowNumbers(self.source_header_number, 7, "111")
        self.assertEqual((1, "Complete.", [3]),(result, msg, rowNumbers))

# PG_53
    # sourceのformatが不正
    def testCsv_csvrow_deleteRowsExcept1(self):
        rowNumbers = [2, 3]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source_invalid, rowNumbers)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # sourceがNULL
    def testCsv_csvrow_deleteRowsExcept2(self):
        rowNumbers = [2, 3]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source_empty, rowNumbers)
        self.assertEqual((0, "Error : The source was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [rowNumbers]が[list]のデータ型以外の場合
    def testCsv_csvrow_deleteRowsExcept3(self):
        rowNumbers = "1"
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, rowNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # rowNumbersがNULL
    def testCsv_csvrow_deleteRowsExcept4(self):
        rowNumbers = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, rowNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # [rowNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvrow_deleteRowsExcept5(self):
        rowNumbers = [1, "5"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, rowNumbers)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # rowUniqueがsourceの範囲を超えていた
    def testCsv_csvrow_deleteRowsExcept6(self):
        columnNumbers = [0, 2]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[0, 2]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # rowUniqueがsourceの範囲を超えていた
    def testCsv_csvrow_deleteRowsExcept7(self):
        columnNumbers = [2, 13]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[2, 13]]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（1 row）
    def testCsv_csvrow_deleteRowsExcept8(self):
        columnNumbers = [2]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 2, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した(duplicate row)
    def testCsv_csvrow_deleteRowsExcept9(self):
        columnNumbers = [2, 2, 6, 6]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 3, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many row)
    def testCsv_csvrow_deleteRowsExcept10(self):
        columnNumbers = [2, 3, 4]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 4, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（many row)
    def testCsv_csvrow_deleteRowsExcept11(self):
        columnNumbers = [2, 3, 4]
        data_expected = pandas.DataFrame([["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=[1,2,3,4,5,6,7,8,9,10])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source_header_number, columnNumbers)
        self.assertEqual((1, "Complete.", 4, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all row）
    def testCsv_csvrow_deleteRowsExcept12(self):
        columnNumbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 12, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # 処理が問題なく完了した（all row）
    def testCsv_csvrow_deleteRowsExcept13(self):
        columnNumbers = [5, 3, 4, 6, 2, 7, 8, 9, 10, 11, 12]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(self.source, columnNumbers)
        self.assertEqual((1, "Complete.", 12, 10), (result, msg, countRows, countColumns))
        assert_frame_equal(data_actual, data_expected)

    # Case: input correct values
    # source's large size (110万行 x 700列)
    def testPerformance(self):
        result_csv, msg_csv, source, countRows_csv, countColumns_csv = csvfl_csvToDataFrame(dataPath, 1)
        print(countRows_csv)
        # function csvrow_deleteRow
        start = time.time()
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_deleteRow(source, 10)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_csv - 1, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_deleteRow : " + str(end - start))

        # function csvrow_deleteRows
        rowNumbers = random.sample(range(2, countRows_actual), 100)
        start = time.time()
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_deleteRows(source, rowNumbers)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_csv - 101, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_deleteRows : " + str(end - start))

        # function csvrow_sampling
        start = time.time()
        countRows_expected = math.ceil((countRows_actual - 1) * 0.1)
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_sampling(source, 0.1)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_expected + 1, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_sampling : " + str(end - start))

        # function csvrow_matchRowNumbers
        start = time.time()
        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, '0')
        end = time.time()
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = 0, targetColumnNumber = 2]"),(result, msg))
        print('Time test function csvrow_matchRowNumbers : ' + str(end - start))

        # function csvrow_deleteRowsExcept
        start = time.time()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRowsExcept(source, [1,2,3,4,5,6,7,8,9])
        end = time.time()
        print('Time test function csvrow_deleteRowsExcept : ' + str(end - start))

# PG_54
    # sourceのformatが不正
    def testCsv_csvrow_samplingByItemInColumn1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source_invalid, "都道府県", 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_samplingByItemInColumn2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source_empty, "都道府県", 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがヘッダのみ
    def testCsv_csvrow_samplingByItemInColumn3(self):
        source = pandas.DataFrame([],columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(source, "都道府県", 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceに都道府県列が存在しない
    def testCsv_csvrow_samplingByItemInColumn4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県1", 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [samplingRatio]が[float]のデータ型以外の場合
    def testCsv_csvrow_samplingByItemInColumn5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合（samplingRatio　＜　0）
    def testCsv_csvrow_samplingByItemInColumn6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", -0.2,)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [-0.2]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 0）
    def testCsv_csvrow_samplingByItemInColumn7(self):
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 0.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [0.0]', 0, 0),(result, msg, countRows, countColumns))

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 1）
    def testCsv_csvrow_samplingByItemInColumn8(self):
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 1.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [1.0]', 0, 0),(result, msg, countRows, countColumns))

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（1≦samplingRatio）
    def testCsv_csvrow_samplingByItemInColumn9(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 1.1)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [1.1]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_samplingByItemInColumn10(self):
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 0.5)
        self.assertEqual((1, "Complete.", 7, 10),(result, msg, countRows, countColumns))

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_samplingByItemInColumn11(self):
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 0.2)
        self.assertEqual((1, "Complete.", 4, 10),(result, msg, countRows, countColumns))  

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_samplingByItemInColumn12(self):
        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(self.source, "都道府県", 0.99)
        self.assertEqual((1, "Complete.", 9, 10),(result, msg, countRows, countColumns))  

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_samplingByItemInColumn13(self):
        source = pandas.DataFrame([["群馬県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["沖縄県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["兵庫県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["北海道","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvrow_samplingByItemInColumn(source, "都道府県", 0.99)
        self.assertEqual((1, "Complete.", 1, 10),(result, msg, countRows, countColumns))  

# PG_55
    # sourceのformatが不正
    def testCsv_csvrow_setValueInRowsSearchedByKey1(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source_invalid, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0),(result))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_setValueInRowsSearchedByKey2(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source_empty, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0, "Error : The source was empty."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # [columnNumber]が[int]のデータ型以外の場合
    def testCsv_csvrow_setValueInRowsSearchedByKey3(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, "1", "和歌山県", targetColumns, "NNN")
        self.assertEqual((-1, "Error : An unexpected error occurred."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvrow_setValueInRowsSearchedByKey4(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 0, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [0]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvrow_setValueInRowsSearchedByKey5(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 11, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified columnNumber was out of range. [11]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # [key]が[string]のデータ型以外の場合
    def testCsv_csvrow_setValueInRowsSearchedByKey6(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, 2, targetColumns, "NNN")
        self.assertEqual((-1, "Error : An unexpected error occurred."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # keyと一致する列が一つもなかった(Error key 1 byte, value soure 2 byte)
    def testCsv_csvrow_setValueInRowsSearchedByKey7(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 5, "ﾃｽﾄ", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ﾃｽﾄ, targetColumnNumber = 5]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # keyと一致する列が一つもなかった(Error key 2 byte, value soure 1 byte)
    def testCsv_csvrow_setValueInRowsSearchedByKey8(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 5, "ヤマグチケン", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ヤマグチケン, targetColumnNumber = 5]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # keyと一致する列が一つもなかった(upper and lower values)
    def testCsv_csvrow_setValueInRowsSearchedByKey9(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 5, "mmmmmm", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = mmmmmm, targetColumnNumber = 5]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # columnNumbersがNULL
    def testCsv_csvrow_setValueInRowsSearchedByKey10(self):
        targetColumns = []
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((-1, "Error : An unexpected error occurred."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # [columnNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvrow_setValueInRowsSearchedByKey11(self):
        targetColumns = [8, "10"]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((-1, "Error : An unexpected error occurred."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvrow_setValueInRowsSearchedByKey12(self):
        targetColumns = [0, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified targetColumn in the targetColumns was out of range. [[0, 10]]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # columnNumberがsourceの範囲を超えていた
    def testCsv_csvrow_setValueInRowsSearchedByKey13(self):
        targetColumns = [8, 11]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((0, "Error : The specified targetColumn in the targetColumns was out of range. [[8, 11]]"),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # [value]が[string]のデータ型以外の場合
    def testCsv_csvrow_setValueInRowsSearchedByKey14(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame()

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した(1 column)
    def testCsv_csvrow_setValueInRowsSearchedByKey15(self):
        targetColumns = [10]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","記述"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","記述"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","記述"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 3, "問", targetColumns, "記述")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した(duplicate column)
    def testCsv_csvrow_setValueInRowsSearchedByKey16(self):
        targetColumns = [8, 8, 8, 8, 8, 8, 8]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","HHHH","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","HHHH","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","HHHH","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 2, "2017-06-27", targetColumns, "HHHH")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した(many column)
    def testCsv_csvrow_setValueInRowsSearchedByKey17(self):
        targetColumns = [8, 10]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","NNN","10","NNN"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","NNN","20","NNN"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","NNN","50","NNN"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","NNN","30","NNN"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 1, "和歌山県", targetColumns, "NNN")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した(many column)
    def testCsv_csvrow_setValueInRowsSearchedByKey18(self):
        targetColumns = [6, 10]
        data_expected = pandas.DataFrame([["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","520","11111","20","20","520"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","520","11111","20","20","520"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","520","11111","20","20","520"]],
                                          columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source_header_number, 8, "20", targetColumns, "520")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した(many duplicate column)
    def testCsv_csvrow_setValueInRowsSearchedByKey19(self):
        targetColumns = [2, 2, 2, 4, 4, 4, 4, 9, 9, 9, 9, 9]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","TEST","番","TEST","MMMMMM","","11111","20","TEST","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","TEST","番","TEST","MMMMMM","","11111","20","TEST","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","TEST","番","TEST","MMMMMM","","11111","20","TEST","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 5, "MMMMMM", targetColumns, "TEST")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した（all column）
    def testCsv_csvrow_setValueInRowsSearchedByKey20(self):
        targetColumns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["","","","","","","","","",""],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["","","","","","","","","",""],
                                          ["","","","","","","","","",""],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["","","","","","","","","",""],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["","","","","","","","","",""],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["","","","","","","","","",""]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 7, "11111", targetColumns, "")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した（all column）
    def testCsv_csvrow_setValueInRowsSearchedByKey21(self):
        targetColumns = [1, 2, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10]
        data_expected = pandas.DataFrame([["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["","","","","","","","","",""],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["","","","","","","","","",""],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                          columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source, 4, "   4   ", targetColumns, "")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した（all column）
    def testCsv_csvrow_setValueInRowsSearchedByKey22(self):
        targetColumns = [1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10]
        data_expected = pandas.DataFrame([["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["群馬県","2017-06-25","問","3","テスト","","111","30","10","12100"],
                                          ["IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII"],
                                          ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["群馬県","2017-06-27","数","2","ﾔﾏｸﾞﾁｹﾝ","","11111","60","30","10400"],
                                          ["IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII"],
                                          ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII"],
                                          ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII"],
                                          ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII","IIII"]],
                                          columns=[1,2,3,4,5,6,7,8,9,10])

        result, msg, data_actual = csvrow_setValueInRowsSearchedByKey(self.source_header_number, 3, "番", targetColumns, "IIII")
        self.assertEqual((1, "Complete."),(result, msg))
        assert_frame_equal(data_expected, data_actual)

if __name__=='__main__':
    unittest.main()
