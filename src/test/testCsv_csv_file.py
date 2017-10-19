# -*- coding: utf-8 -*-
"""
Unit test for csv_file.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
import pandas
import time
import os

from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv
from pandas.util.testing import assert_frame_equal

dataDir = r".\data"
dataDirErr = r".\dataError"

csvFullPath = dataDir + r'\sample_data.csv'
csvFullPathNotExist = dataDir + r'\file_not_exist.csv'
csvFullPathNotOpen = dataDir + r'\file_not_open.csv'
csvFullPathEmpty = dataDir + r'\sample_empty_file.csv'
csvFullPathInvalid = dataDir + r'\sample_invalid_file.tsv'
csvFullPathLarge = dataDir + r'\sample_large_data.csv'

csvOutput = r"output.csv"
csvOutput_w_header = r"output_w_header.csv"
csvOutput_wo_header = r"output_wo_header.csv"
csvOutputLargeData = r'output_large_data.csv'
csv_invalid = r'data???.csv'
csv_not_write = r"csv_not_write.csv"

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

# PG_11
    # [csvFullPath]が[string]のデータ型以外の場合
    def testCsvfl_csvToDataFrame_1(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (11, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # [existHeaderFlag]が[int]のデータ型以外の場合
    def testCsvfl_csvToDataFrame_2(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPath, "1")
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # [existHeaderFlag]が[int]のデータ型であり、且つ０、１以外の場合
    def testCsvfl_csvToDataFrame_3(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPath, 2)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # CSVファイルがない
    # Error: File not exist
    def testCsvfl_csvToDataFrame_4(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPathNotExist, 1)
        self.assertEqual((0, r"Error : Cannot find the CSV file specified. [" + csvFullPathNotExist + "]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # CSVファイルがない
    # Error: File not open
    # Note: set permission not read in file
    @unittest.skip("testCsvfl_csvToDataFrame_5 skipping")
    def testCsvfl_csvToDataFrame_5(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPathNotOpen, 1)
        self.assertEqual((0, r"Error : Cannot open the CSV file specified. [" + csvFullPathNotOpen + "]", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # CSVファイルのフォーマットの中身がNULL
    def testCsvfl_csvToDataFrame_6(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPathEmpty, 1)
        self.assertEqual((0, "Error : The file specified was empty.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # CSVファイルのフォーマットが不正
    def testCsvfl_csvToDataFrame_7(self):
        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPathInvalid, 1)
        self.assertEqual((0, "Error : Invalid CSV file format.", 0, 0), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した（header行が有る）
    def testCsvfl_csvToDataFrame_8(self):
        data_expected = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                          columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPath, 1)
        self.assertEqual((1, "Complete.", 3, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 処理が問題なく完了した（header行が無い）
    def testCsvfl_csvToDataFrame_9(self):
        data_expected  = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                           ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                           ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                           columns=[1,2,3,4,5,6,7,8,9])

        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPath, 0)
        self.assertEqual((1, "Complete.", 4, 9), (result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

# PG_12
    # sourceのformatが不正
    def testCsvfl_dataFrameToCsv_1(self):
        source = [["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]

        result, msg, newName = csvfl_dataFrameToCsv (source, 1, True, dataDir, csvOutput)
        self.assertEqual((0, "Error : The source was invalid format.", csvOutput), (result, msg, newName))

    # sourceがNULL
    def testCsvfl_dataFrameToCsv_2(self):
        source = pandas.DataFrame()
        result, msg, newName = csvfl_dataFrameToCsv (source, 1, True, dataDir, csvOutput)
        self.assertEqual((0, "Error : The source was empty.", csvOutput), (result, msg, newName))

        # [existHeaderFlag]が[int]のデータ型以外の場合
    def testCsvfl_dataFrameToCsv_3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv ( source,"1",True, dataDir, csvOutput)
        self.assertEqual((-1, "Error : An unexpected error occurred.",csvOutput), (result, msg, newName))

    # [existHeaderFlag]が[int]のデータ型であり、且つ０、１以外の場合
    def testCsvfl_dataFrameToCsv_4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv ( source, 3,True, dataDir, csvOutput)
        self.assertEqual((-1, "Error : An unexpected error occurred.",csvOutput), (result, msg, newName))

    # [ovwFlag]が[bool]のデータ型以外の場合
    def testCsvfl_dataFrameToCsv_5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv ( source, 1, "true", dataDir, csvOutput)
        self.assertEqual((-1, "Error : An unexpected error occurred.",csvOutput), (result, msg, newName))

    # [ovwFlag]が[int]のデータ型であり、且つ０、１以外の場合
    def testCsvfl_dataFrameToCsv_6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv ( source, 1, 3, dataDir, csvOutput)
        self.assertEqual((-1, "Error : An unexpected error occurred.",csvOutput), (result, msg, newName))

    # directory = ""
    def testCsvfl_dataFrameToCsv_7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv ( source, 1, True, "", csvOutput)
        self.assertEqual((0, "Error : Cannot find the directory specified. []", csvOutput), (result, msg, newName))

    # [directory]が[string]のデータ型以外の場合
    def testCsvfl_dataFrameToCsv_8(self):
        source = pandas.DataFrame([])
        result, msg, newName = csvfl_dataFrameToCsv ( source, 1, True, 123, csvOutput)
        self.assertEqual(( -1, "Error : An unexpected error occurred.", csvOutput), (result, msg, newName))

    # 指定されたdirectoryがない
    def testCsvfl_dataFrameToCsv_9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv (source,1,True,dataDirErr,csvOutput)
        self.assertEqual((0,r"Error : Cannot find the directory specified. [" + dataDirErr + "]", csvOutput), (result, msg, newName))

    # [csvName]が[string]のデータ型以外の場合
    def testCsvfl_dataFrameToCsv_10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv (source,1,True,dataDir,123)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 123), (result, msg, newName))

    # ファイル名が不正。(¥　/　:　*　?　"　<　>　|が含まれる
    def testCsvfl_dataFrameToCsv_11(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv (source,1,True,dataDir,csv_invalid)
        self.assertEqual((0, "Error : Invalid CSV file name. [" + csv_invalid +"]", csv_invalid), (result, msg, newName))

    # csvName = ""
    def testCsvfl_dataFrameToCsv_12(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv (source,1,True,dataDir,"")
        self.assertEqual((0, "Error : Invalid CSV file name. []", ""), (result, msg, newName))

    # CSV ファイルが保存できない
    @unittest.skip("testCsvfl_dataFrameToCsv_13 skipping")
    def testCsvfl_dataFrameToCsv_13(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                    ["2017-06-25","国","2","M","","12893","0","0","12893"],
                                    ["2017-06-25","国","3","短","","12893","0","0","0"]])

        result, msg, newName = csvfl_dataFrameToCsv (source, 1, True, dataDir, csv_not_write)
        self.assertEqual((0, r"Error : Cannot create or save this file. [" + os.path.join(dataDir, csv_not_write)+ "]", csv_not_write), (result, msg, newName))

    # 処理が問題なく完了した（existHeaderFlag　＝　１）
    def testCsvfl_dataFrameToCsv_14(self):
        source = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                          columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])        
        
        result, msg, newName = csvfl_dataFrameToCsv (source, 1, True, dataDir, csvOutput_w_header)
        self.assertEqual((1, "Complete.", csvOutput_w_header), (result, msg, newName))

    # 処理が問題なく完了した（existHeaderFlag　＝　0）
    def testCsvfl_dataFrameToCsv_15(self):
        source = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                          columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])   

        result, msg, newName = csvfl_dataFrameToCsv (source, 0, True, dataDir, csvOutput_wo_header)
        self.assertEqual((1, "Complete.", csvOutput_wo_header), (result, msg, newName))

    # 処理が問題なく完了した（ovwFlag　＝　True）
    def testCsvfl_dataFrameToCsv_16(self):
        source = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                          columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])   

        result, msg, newName = csvfl_dataFrameToCsv (source, 1, True, dataDir, csvOutput)
        self.assertEqual((1, "Complete.", csvOutput), (result, msg, newName))

    # 処理が問題なく完了した（ovwFlag　＝　False）
    def testCsvfl_dataFrameToCsv_17(self):
        source = pandas.DataFrame([["2017-06-25","国","2","M","","12893","0","0","12893"],
                                          ["2017-06-25","国","3","短","","12893","0","0","0"]],
                                          columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])   

        result, msg, newName = csvfl_dataFrameToCsv (source, 1, False, dataDir, csvOutput)
        self.assertEqual((1, "Complete.", "output(1).csv"), (result, msg, newName))
        if os.path.isfile(os.path.join(dataDir, 'output(1).csv')):
            os.unlink(os.path.join(dataDir, 'output(1).csv'))

    @unittest.skip("testPerformance skipping")
    def testPerformance(self):
        # function csvToDataFrame
        start = time.time()
        result, msg, data_actual, countRows, countColumns = csvfl_csvToDataFrame (csvFullPathLarge, 1)
        end = time.time()
        self.assertEqual((1, "Complete."), (result, msg))
        print("Time test function Csvfl_csvToDataFrame: " + str(end - start))

        # function csvfl_dataFrameToCsv
        start = time.time()
        result, msg, newName = csvfl_dataFrameToCsv (data_actual,1,True,dataDir,csvOutputLargeData)
        end = time.time()
        self.assertEqual((1, "Complete.", csvOutputLargeData), (result, msg, newName))
        print("Time test function Csvfl_dataFrameToCsv: " + str(end - start))

if __name__=='__main__':
    unittest.main()