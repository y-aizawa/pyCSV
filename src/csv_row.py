# -*- coding: utf-8 -*-
"""
csvファイルをlistにconvertしたデータに対して、row（行）を編集するmodule。
"""

import pandas
import constants as const
import math
import random

"""
機能   :  指定した行を削除する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ。
          削除する行番号
戻り値  :  ステータス
          メッセージ
          行削除後のデータをlistにしたもの
          csvファイルにしたときのデータの行数
          csvファイルにしたときのデータの列数
"""
def csvrow_deleteRow(source, rowNumber):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    newData = []
    countRows = 0
    countColumns = 0
    
    try:
        # sourceのformatが不正。
        if(type(source) != list):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return
    
        # sourceがNULL。
        if not len(source):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        df = pandas.DataFrame(source)
        if (rowNumber <= len(source) and rowNumber > 0):
            df.drop(df.index[rowNumber-1], inplace=True)
            newData = df.values.tolist()
            countRows = df.shape[0]
            countColumns = df.shape[1]
        else:
            # rowNumberがListの範囲を超えていた。
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_ROW_NUMBER, rowNumber)

    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  rowNumbers(list)で指定した複数の行を削除する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ。
          削除する行番号のlist
戻り値  :  ステータス
          メッセージ
          行削除後のデータをlistにしたもの
          csvファイルにしたときのデータの行数
          csvファイルにしたときのデータの列数
"""
def csvrow_deleteRows(source, rowNumbers):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    newData = []
    countRows = 0
    countColumns = 0
    
    try:
        # sourceのformatが不正。
        if(type(source) != list):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return
    
        # sourceがNULL。
        if not len(source):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        for i in range(len(rowNumbers)):
            if(rowNumbers[i] > len(source) or rowNumbers[i] < 1):
                #指定されたrowNumberがListの範囲を超えていた。
                result = const.RESULT_ERR
                msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_ROW_NUMBER, const.NAME_ROW_NUMBERS, rowNumbers)
                return

        df = pandas.DataFrame(source)
        # 2行目を削除したい場合[2]が渡されるので、-1する。
        rowNumbers[:] = [x - 1 for x in rowNumbers]
        df.drop(df.index[rowNumbers], inplace=True)
        countRows = df.shape[0]
        if(countRows == 0):
            countColumns = 0
            newData = []
        else:
            countColumns = df.shape[1]
            newData = df.values.tolist()
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  samplingRatioに従って、sourceの中から要素をsamplingする。
          samplingする際は、重複しない疑似乱数を用いたランダンプサンプリングを行う。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ。
          samplingの割合 (e.g.: 10%の場合-.1、1%の場合0.01)
戻り値  :  ステータス
          メッセージ
          sampling後のcsvデータのlist
          csvファイルにしたときのデータの行数
          csvファイルにしたときのデータの列数
"""
def csvrow_sampling(source, samplingRatio):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    newData = []
    countRows = 0
    countColumns = 0
    
    try:
        # sourceのformatが不正。
        if(type(source) != list):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return
    
        # sourceがNULL。
        if not len(source):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合。        
        if (samplingRatio < 0 or samplingRatio > 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_SAMPLING.format(samplingRatio)
            return

        df = pandas.DataFrame(source)
        numberOfSamples = math.ceil((len(source) - 1) * samplingRatio)
        # サンプリング対象Indexを取得
        tgtIndex = random.sample(range(1, len(source)), numberOfSamples)
        tgtIndex.insert(0, 0)
        df = df.loc[tgtIndex]
        newData = df.values.tolist()        
        countRows = df.shape[0]
        countColumns = df.shape[1]        
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, newData, countRows, countColumns
    
"""
機能   :  source(list)の中の、指定した列(targetColumnNumber)を検索し、keyと一致する行の郷番号を全てを取得する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ。
          検索する対象の列番号
          検索する値
戻り値  :  ステータス
          メッセージ
          一致した行番号のlist
"""
def csvrow_matchRowNumbers(source, targetColumnNumber, key):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    rowNumbers = []
    
    try:
        key = key.strip()
        
        # sourceのformatが不正。
        if(type(source) != list):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return
    
        # sourceがNULL。
        if not len(source):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # targetColumnNumberがListの範囲を超えていた。
        if (targetColumnNumber < 1 or targetColumnNumber > len(source[0])):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_TARGET_COLUMN_NUMBER, targetColumnNumber)
            return

        df = pandas.DataFrame(source)
        recordIndexes = df[df[targetColumnNumber-1] == key].index + 1
        # keyと一致する列が一つもなかった。
        if (len(recordIndexes) == 0):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_KEY_NOT_FOUND.format(key, targetColumnNumber)
            return
        else:
            rowNumbers = recordIndexes.tolist()
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, rowNumbers


if __name__=='__main__':
    print("")