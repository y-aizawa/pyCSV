# -*- coding: utf-8 -*-
"""
匿名化処理を行うモジュール
"""

import pandas
import numpy as np
import constants as const
import csv_column
import csv_row

"""
機能   :  都道府県ごとにサンプリングをする
引数   :
            DataFrame   :   DataFrame形式のデータ
            float       :   samplingの割合 (e.g.: 10%の場合-.1、1%の場合0.01)
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   sampling後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def anony_reagionalSampling (source, samplingRatio):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # sampling後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0
    
    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame: 
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [samplingRatio]が[float]のデータ型以外の場合
        if type(samplingRatio) is not float:
            raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合
        if (samplingRatio < 0 or samplingRatio > 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_SAMPLING.format(samplingRatio)
            return
        
        #データから都道府県コードを抽出（行指定は実際のデータに合わせて変える必要あり）
        regionList = csv_column.csvcol_countEvery(source,[1])[2][0][1:]
        csv_column.csvcol_countEvery(source,[1])[2]
        
        #都道府県ごとのデータを抽出
        sourcesByRegion=[]
        for i in range(regionList.shape[0]):
            hedder = pandas.DataFrame(["都道府県コード","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"]).T
            data = source[source[1] == regionList[i+1]]
            data.columns = range(0, len(data.columns))
            data = pandas.concat([hedder,data])
            sourcesByRegion.append(data)
            
        #都道府県ごとにサンプリングする
        sampledSources=[]
        for i in range(regionList.shape[0]):
            sampledSource = csv_row.csvrow_sampling(sourcesByRegion[i], 0.5)
            sampledSources.append(sampledSource[2])
            
        #都道府県ごとにサンプリングしたデータを結合
        combinedSampledSource = pandas.DataFrame
        for i in range(regionList.shape[0]-1):
            if i == 0:
                combinedSampledSource = pandas.concat([sampledSources[i][1:],sampledSources[i+1][1:]])
            else:
                combinedSampledSource = pandas.concat([combinedSampledSource,sampledSources[i+1][1:]])
                
        #結合したデータにhedder列を付与
        hedder = pandas.DataFrame(["都道府県コード","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"]).T
        combinedSampledSource = combinedSampledSource.reindex(np.random.permutation(combinedSampledSource.index))
        combinedSampledSource = pandas.concat([hedder, combinedSampledSource]).reset_index(drop=True)
        
        newData = combinedSampledSource
        countRows = newData.shape[0]
        countColumns = newData.shape[1]
        
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
        
    finally:
        return result, msg, newData, countRows, countColumns
 
if __name__ == '__main__':
    source = pandas.DataFrame([["都道府県コード","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                               ["01","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                               ["02","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                               ["01","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                               ["03","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                               ["04","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                               ["01","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                               ["01","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                               ["03","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                               ["01","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                               ["04","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                               ["04","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                               ["05","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                               ["03","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"],
                               ["02","2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                               ["03","2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                               ["05","2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                               ["01","2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

    result, msg, newData, countRows, countColumns = anony_reagionalSampling(source, 0.5)
    print (newData)