# -*- coding: utf-8 -*-
"""
Unit test for anony.py
"""
import sys
sys.path.append('../') # 親ディレクトリの親ディレクトリを読み込む

import unittest
import pandas
from pandas.util.testing import assert_frame_equal
from anony import anony_reagionalSampling

dataPath = r".\data\sample_large_data.csv"
dataDir =  r".\data"

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # sourceのformatが不正
    def testCsv_csvrow_sampling1(self):
        source = [["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["宮城県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_sampling2(self):
        source = pandas.DataFrame()
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)
        
    # sourceがヘッダのみ
    def testCsv_csvrow_sampling3(self):
        source = pandas.DataFrame([],columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)
        
    # sourceに都道府県列が存在しない
    def testCsv_csvrow_sampling4(self):
        source = pandas.DataFrame([["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                   columns=["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()
    
        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [samplingRatio]が[float]のデータ型以外の場合
    def testCsv_csvrow_sampling5(self):
        source = pandas.DataFrame([["鳥取県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["東京都","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合（samplingRatio　＜　0）
    def testCsv_csvrow_sampling6(self):
        source = pandas.DataFrame([["宮崎県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["島根県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, -0.2)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [-0.2]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)


    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 0）
    def testCsv_csvrow_sampling7(self):
        source = pandas.DataFrame([["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["北海道","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["愛媛県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["広島県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["茨城県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        
        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [0.0]', 0, 0),(result, msg, countRows, countColumns))

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（samplingRatio = 1）
    def testCsv_csvrow_sampling8(self):
        source = pandas.DataFrame([["沖縄県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["京都府","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["佐賀県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["香川県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["青森県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 1.0)
        self.assertEqual((0, 'Error : The samplingRatio must be more than 0 and less than 1. [1.0]', 0, 0),(result, msg, countRows, countColumns))

    # 指定されたsamplingRatioが0<samplingRatio<1の範囲外だった場合（1≦samplingRatio）
    def testCsv_csvrow_sampling9(self):
        source = pandas.DataFrame([["群馬県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["兵庫県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["大阪府","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["岡山県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["秋田県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 1.1)
        self.assertEqual((0, "Error : The samplingRatio must be more than 0 and less than 1. [1.1]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling10(self):
        source = pandas.DataFrame([["群馬県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["群馬県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["沖縄県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["沖縄県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["沖縄県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["沖縄県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["沖縄県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["兵庫県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["兵庫県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["兵庫県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["兵庫県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["秋田県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["秋田県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["秋田県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["北海道","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["北海道","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["北海道","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["北海道","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.5)
        self.assertEqual((1, "Complete.", 15, 10),(result, msg, countRows, countColumns))

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling11(self):
        source = pandas.DataFrame([["群馬県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["群馬県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["群馬県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["群馬県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["群馬県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["和歌山県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["和歌山県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["和歌山県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["和歌山県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["沖縄県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["沖縄県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["沖縄県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["沖縄県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["沖縄県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["兵庫県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["兵庫県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["兵庫県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["兵庫県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["秋田県","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["秋田県","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["秋田県","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["秋田県","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["秋田県","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                                   ["北海道","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["北海道","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["北海道","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["北海道","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]],
                                   columns=["都道府県","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

        result, msg, data_actual, countRows, countColumns = anony_reagionalSampling(source, 0.2)
        self.assertEqual((1, "Complete.", 6, 10),(result, msg, countRows, countColumns))  
        
if __name__=='__main__':
    unittest.main()
