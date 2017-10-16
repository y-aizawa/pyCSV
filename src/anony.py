# -*- coding: utf-8 -*-
"""
匿名化処理を行うモジュール
"""

import pandas as pd
import numpy as np
import constants as const
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
    newData = pd.DataFrame()            # sampling後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0
    
    try:
        # sourceのformatが不正
        if type(source) is not pd.core.frame.DataFrame: 
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
        
        #データから都道府県コードを抽出
        regionList = source["都道府県コード"].unique()
        
        #都道府県ごとのデータを抽出
        sourcesByRegion=[]
        for i in range(regionList.shape[0]):
            data = source[source["都道府県コード"] == regionList[i]]
            sourcesByRegion.append(data)
            
        #都道府県ごとにサンプリングする
        sampledSources=[]
        for i in range(regionList.shape[0]):
            sampledSource = csv_row.csvrow_sampling(sourcesByRegion[i], samplingRatio)
            sampledSources.append(sampledSource[2])
            
        #都道府県ごとにサンプリングしたデータを結合
        combinedSampledSource = sampledSources[0]
        for i in range(regionList.shape[0]-1):
            combinedSampledSource = pd.concat([combinedSampledSource,sampledSources[i+1]])
                
        #結合したデータをシャッフルしてインデックスを振りなおす
        combinedSampledSource = combinedSampledSource.reindex(np.random.permutation(combinedSampledSource.index)).reset_index(drop=True)
        
        newData = combinedSampledSource
        countRows = newData.shape[0]
        countColumns = newData.shape[1]
        
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
        
    finally:
        return result, msg, newData, countRows, countColumns
 
if __name__ == '__main__':
    source = pd.DataFrame([["01","2017-06-25","数","3","aaaaa","","23242","30","10","12100"],
                               ["02","2017-06-26","理","2","bbbbb","","11111","20","20","10800"],
                               ["01","2017-06-27","国","3","ccccc","","12893","90","50","10200"],
                               ["03","2017-06-27","数","2","ddddd","","11111","60","30","10400"],
                               ["04","2017-06-28","英","4","eeeee","","11111","50","30","23242"],
                               ["01","2017-06-25","英","3","fffff","","23242","30","10","12100"],
                               ["01","2017-06-26","社","2","ggggg","","11111","20","20","10800"],
                               ["03","2017-06-27","国","3","hhhhh","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","iiiii","","11111","60","30","10400"],
                               ["01","2017-06-28","理","4","jjjjj","","11111","50","30","23242"],
                               ["04","2017-06-25","社","3","kkkkk","","23242","30","10","12100"],
                               ["04","2017-06-26","英","2","lllll","","11111","20","20","10800"],
                               ["05","2017-06-27","国","3","mmmmm","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","nnnnn","","11111","60","30","10400"],
                               ["03","2017-06-28","社","4","ooooo","","11111","50","30","23242"],
                               ["02","2017-06-25","理","3","ppppp","","23242","30","10","12100"],
                               ["03","2017-06-26","刻","2","qqqqq","","11111","20","20","10800"],
                               ["05","2017-06-27","国","3","rrrrr","","12893","90","50","10200"],
                               ["02","2017-06-27","数","2","sssss","","11111","60","30","10400"],
                               ["01","2017-06-28","英","4","ttttt","","11111","50","30","23242"]],
    columns=["都道府県コード","集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"])

    result, msg, newData, countRows, countColumns = anony_reagionalSampling(source, 0.5)
    print (newData)