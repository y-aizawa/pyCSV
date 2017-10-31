# -*- coding: utf-8 -*-
"""
csvファイルをDataFrameにconvertしたデータに対して、row（行）を編集するmodule
"""

import pandas
import constants as const
import math
import random
import numpy as np

"""
機能   :  指定した行を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   削除する行番号
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   行削除後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_deleteRow(source, rowNumber):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # 行削除後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [rowNumber]が[int]のデータ型以外の場合
        if type(rowNumber) is not int:
           raise Exception

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # rowNumberがsourceの範囲を超えていた
        if (rowNumber > (source.shape[0] + 1) or rowNumber < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_ROW_NUMBER, rowNumber)
            return

        # rowNumber=1の場合Errorとする
        if (rowNumber == 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_DELETE_HEADER_ROW
            return

        # 2行目を削除したい場合[2]が渡されるので、-2する
        source.drop(source.index[rowNumber - const.PANDAS_FIRST_ROW_INDEX], inplace=True)
        source.set_axis(0, range(source.shape[0]))
        newData = source
        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  rowNumbers(list)で指定した複数の行を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   削除する行番号のlist
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   行削除後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_deleteRows(source, rowNumbers):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    newData = pandas.DataFrame()    # 行削除後のDataFrame形式のデータ
    countRows = 0                   # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [rowNumbers]が[list]のデータ型以外の場合
        # rowNumbersがNULL
        if (type(rowNumbers) is not list) or (not len(rowNumbers)):
            raise Exception

        # [rowNumbers] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in rowNumbers):
            raise Exception

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        #指定されたrowNumbersがsourceの範囲を超えていた
        if (max(rowNumbers) > (source.shape[0] + 1) or min(rowNumbers) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_ROW_NUMBER, const.NAME_ROW_NUMBERS, rowNumbers)
            return

        # rowNumbersに「1」が含まれていた場合Errorとする
        if 1 in rowNumbers:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_DELETE_HEADER_ROW
            return

        # 2行目を削除したい場合[2]が渡されるので、-2する
        rowNumbers[:] = [x - const.PANDAS_FIRST_ROW_INDEX for x in rowNumbers]
        source.drop(source.index[rowNumbers], inplace=True)
        source.set_axis(0, range(source.shape[0]))
        newData = source
        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  samplingRatioに従って、sourceの中から要素をsamplingする
         samplingする際は、重複しない疑似乱数を用いたランダンプサンプリングを行う
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
def csvrow_sampling(source, samplingRatio):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # sampling後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

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
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合
        if (samplingRatio <= 0 or samplingRatio >= 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_SAMPLING.format(samplingRatio)
            return

		# サンプリング数を計算:
        # 対象が1行しかない場合は、サンプリングしない。
        if source.shape[0] == 1:
            numberOfSamples = 0
        # 小数点以下を切り上げする事で全対象をサンプリングしてしまう場合は、小数点以下を切り捨てとする。
        elif source.shape[0] == math.ceil(source.shape[0] * samplingRatio):
            numberOfSamples = math.floor(source.shape[0] * samplingRatio)
        # 基本的に多めにサンプリングする為、小数点以下を切り上げる。
        else:
            numberOfSamples = math.ceil(source.shape[0] * samplingRatio)
        
        # サンプリング対象Indexを取得
        tgtIndex = random.sample(range(0, source.shape[0]), numberOfSamples)
        
        # サンプリング
        newData = source.iloc[tgtIndex]
        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  キー（columnName）の種類ごとにサンプリングをする
引数   :
            DataFrame   :   DataFrame形式のデータ
            string      :   キーとする文字列=カラム名
            float       :   samplingの割合 (e.g.: 10%の場合-.1、1%の場合0.01)
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   sampling後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""

def csvrow_samplingByItemInColumn (source, columnName, samplingRatio):
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
        
        # sourceに指定されたcolumnNameが存在しない
        if not columnName in source.columns:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合
        if (samplingRatio <= 0 or samplingRatio >= 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_SAMPLING.format(samplingRatio)
            return

        #データからcolumnNameを重複除外して取得
        uniqueColumnNameList = source[columnName].unique()
        
        #columnNameごとのデータを抽出
        sourcesByColumnName=[]
        for i in range(uniqueColumnNameList.shape[0]):
            data = source[source[columnName] == uniqueColumnNameList[i]]
            sourcesByColumnName.append(data)
            
        #columnNameごとにサンプリングする
        sampledSources=[]
        for i in range(uniqueColumnNameList.shape[0]):
            sampledSource = csvrow_sampling(sourcesByColumnName[i], samplingRatio)
            sampledSources.append(sampledSource[2])
            
        #サンプリングしたデータを結合
        combinedSampledSource = sampledSources[0]
        for i in range(1, uniqueColumnNameList.shape[0]):
            combinedSampledSource = pandas.concat([combinedSampledSource,sampledSources[i]])
                
        #結合したデータをシャッフルしてインデックスを振りなおす
        combinedSampledSource = combinedSampledSource.reindex(np.random.permutation(combinedSampledSource.index)).reset_index(drop=True)
        
        newData = combinedSampledSource
        
        #行数はヘッダ付きでcsvに変換した際の行数とする為+1
        countRows = newData.shape[0]+1
        countColumns = newData.shape[1]
        
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
        
    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  source(DataFrame)の中の、指定した列(targetColumnNumber)を検索し、keyと一致する行の番号を全てを取得する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   検索する対象の列番号
            string      :   検索する値
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            list        :   一致した行番号のlist
"""
def csvrow_matchRowNumbers(source, targetColumnNumber, key):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    rowNumbers = []                 # 一致した行番号のlist

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [targetColumnNumber]が[int]のデータ型以外の場合
        if type(targetColumnNumber) is not int:
            raise Exception

        # [key]が[string]のデータ型以外の場合
        if type(key) is not str:
            raise Exception
        key = key.strip()

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # targetColumnNumberがsourceの範囲を超えていた
        if (targetColumnNumber < 1 or targetColumnNumber > source.shape[1]):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_TARGET_COLUMN_NUMBER, targetColumnNumber)
            return

        source.set_axis(0, range(source.shape[0]))
        recordIndexes = source[source.iloc[:, targetColumnNumber-1] == key].index + const.PANDAS_FIRST_ROW_INDEX
        # keyと一致する列が一つもなかった
        if (len(recordIndexes) == 0):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_KEY_NOT_FOUND.format(key, targetColumnNumber)
            return
        else:
            # 処理が問題なく完了した
            rowNumbers = recordIndexes.tolist()

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, rowNumbers

"""
機能   :  rowNumbers(list)で指定した複数の行番号以外の行を削除する
          rowNumbersに1（ヘッダ行を表す行番号）が無い場合は、1があるものとして処理を行う
          つまりrowNumbers =[2,4]と指定された場合rowNumbers =[1,2,4]として処理を行う
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   削除する行番号のlist
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   行削除後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_deleteRowsExcept(source, rowNumbers):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # 行削除後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [rowNumbers]が[list]のデータ型以外の場合
        # rowNumbersがNULL
        if (type(rowNumbers) is not list) or (not len(rowNumbers)):
            raise Exception

        rowUnique = np.unique(rowNumbers).tolist()
        # [rowUnique] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in rowUnique):
            raise Exception

        # 指定されたrowUniqueがsourceの範囲を超えていた
        if(max(rowUnique) > (source.shape[0] + 1) or min(rowUnique) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_ROW_NUMBER, const.NAME_ROW_NUMBERS, rowNumbers)
            return

        rowNumbers[:] = [x - const.PANDAS_FIRST_ROW_INDEX for x in rowUnique if x != 1]
        newData = source.iloc[rowNumbers]
        newData.set_axis(0, range(newData.shape[0]))
        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  DataFrameの指定した列が、指定したkeyと等しいレコードを検索
          keyと一致したレコードの指定した列の値を、指定したvalueで置き換える
引数   :
            DataFrame   :   DataFrame形式のデータ
            int        :   検索する対象の列番号
            string      :   検索する値
            list
            string
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   setValueのDataFrame形式のデータ
"""
def csvrow_setValueInRowsSearchedByKey(source, columnNumber, key, targetColumns, value):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # setValueのDataFrame形式のデータ

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [columnNumber]が[int]のデータ型以外の場合
        if type(columnNumber) is not int:
           raise Exception

        # columnNumberがsourceの範囲を超えていた
        if (columnNumber > source.shape[1] or columnNumber < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER, columnNumber)
            return

        # [key]が[string]のデータ型以外の場合
        # [value]が[string]のデータ型以外の場合
        if type(key) is not str  or type(value) is not str:
            raise Exception
        key = key.strip()

        # [targetColumns]が[list]のデータ型以外の場合
        # targetColumnsがNULL
        if (type(targetColumns) is not list) or (not len(targetColumns)):
            raise Exception

        targetColumnsUnique = np.unique(targetColumns).tolist()
        # [targetColumnsUnique] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in targetColumnsUnique):
            raise Exception

        # 指定されたtargetColumnsUniqueの範囲を超えていた
        if(max(targetColumnsUnique) > (source.shape[1]) or min(targetColumnsUnique) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_TARGET_COLUMN, const.NAME_TARGET_COLUMNS, targetColumnsUnique)
            return

        recordSearch = source[source.iloc[:, columnNumber - 1] == key].index
        # keyと一致する列が一つもなかった
        if (len(recordSearch) == 0):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_KEY_NOT_FOUND.format(key, columnNumber)
        else:
            # 処理が問題なく完了した
            targetColumnsUnique = list(np.asarray(targetColumnsUnique) - 1)
            source.iloc[recordSearch, targetColumnsUnique] = value
            newData = source

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData

if __name__=='__main__':
    pass