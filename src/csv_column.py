# -*- coding: utf-8 -*-
"""
csvファイルをDataFrameにconvertしたデータに対して、column（列）を編集するmodule
"""

import pandas
import constants as const
import numpy as np
import random

"""
機能      :   headerNameとheader名が一致する列番号を取得する
引数      :
              DataFrame     :   DataFrame形式のデータ
              string        :   header名称
戻り値     :
              int           :   ステータス
              string        :   メッセージ
              int           :   headerのcolumnNumber
"""
def csvcol_getHeaderColumnNumber(source, headerName):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    headerColumnNumber = 0          # headerのcolumnNumber

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [headerName]が[string]のデータ型以外の場合
        if type(headerName) is not str:
           raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        #i = 0
        #while (i < source.shape[1]):
        #    if(headerName == source.iloc[0, i]):
        #        headerColumnNumber = i + 1
        #        break
        #    i = i + 1
        headerColumnNumber = -1
        for i, name in enumerate(source.columns.values):
            if headerName == name:
                headerColumnNumber = i + 1
                break

        # headerが見つからない
        if (headerColumnNumber == -1):
            result = const.RESULT_ERR
            headerColumnNumber = 0
            msg = const.MSG_ERR_NOT_FOUND_HEADER_NAME.format(headerName)
            
    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, headerColumnNumber

"""
機能   :    headerColumnNumberと一致するheader名を取得する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   headerのcolumnNumber
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            string      :   header名称
"""
def csvcol_getHeaderName(source, headerColumnNumber):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    headerName = ""                     # header名称

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [headerColumnNumber]が[int]のデータ型以外の場合
        if type(headerColumnNumber) is not int:
           raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # headerColumnNumberがsourceの範囲を超えていた
        if(headerColumnNumber > source.shape[1] or headerColumnNumber < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_HEADER_COLUMN_NUMBER, headerColumnNumber)
            return

        # 処理が問題なく完了した
        #headerName = source.iloc[0, headerColumnNumber-1]
        headerName = source.columns.values[headerColumnNumber-1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, headerName

"""
機能   :  指定した列を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   削除する列番号
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   列削除後のDataFrame形式のデータ
            int         :   csvファイルにした場合のデータの行数
            int         :   csvファイルにした場合のデータの列数
"""
def csvcol_deleteColumn(source, columnNumber):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # 列削除後のDataFrame形式のデータ
    countRows = 0                       # csvファイルにした場合のデータの行数
    countColumns = 0                    # csvファイルにした場合のデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [columnNumber]が[int]のデータ型以外の場合
        if type(columnNumber) is not int:
           raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # columnNumberがsourceの範囲を超えていた
        if (columnNumber > source.shape[1] or columnNumber < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER, columnNumber)
            return

        #2列目を削除したい場合[2]が渡されるので、-1する
        source.drop(source.columns[columnNumber-1], axis=1, inplace=True)
        #source.set_axis(1, range(source.shape[1]))
        countColumns = source.shape[1]
        if(countColumns == 0):
            countRows = 0
            newData = pandas.DataFrame()
        else:
            countRows = source.shape[0] + 1
            newData = source

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  columnNumbers (list)で指定した複数の列を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   削除する列番号のlist
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   列削除後のDataFrame形式のデータ
            int         :   csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvcol_deleteColumns(source, columnNumbers):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # 列削除後のDataFrame形式のデータ
    countRows = 0                       # csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [columnNumbers]が[list]のデータ型以外の場合
        # columnNumbersがNULL
        if (type(columnNumbers) is not list) or (not len(columnNumbers)):
            raise Exception

        # [columnNumbers] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in columnNumbers):
            raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # columnNumberがsourceの範囲を超えていた
        if (max(columnNumbers) > source.shape[1] or min(columnNumbers) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_COLUMN_NUMBER, const.NAME_COLUMN_NUMBERS, columnNumbers)
            return

        # 2列目を削除したい場合[2]が渡されるので、-1する
        columnNumbers[:] = [x - 1 for x in columnNumbers]
        source.drop(source.columns[columnNumbers], axis=1, inplace=True)
        #source.set_axis(1, range(source.shape[1]))
        countColumns = source.shape[1]
        if(countColumns == 0):
            countRows = 0
            newData = pandas.DataFrame()
        else:
            countRows = source.shape[0]+1
            newData = source

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  指定した列(colulmnNumber_From)を、指定した列(colulmnNumber_To)に挿入する
          処理後の列数は、処理前に比べて1増加する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   複写元の列番号
            int         :   複写先の列番号（「0」の場合、最終列に追加）
            string      :   複写先のヘッダ名
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   複写後のDataFrame形式のデータ
            int         :   csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvcol_duplicateColumn(source, columnNumber_From, columnNumber_To, headerName_To):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    newData = pandas.DataFrame()    # 複写後のDataFrame形式のデータ
    countRows = 0                   # csvファイルにしたときのデータの行数
    countColumns = 0                # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [columnNumber_From]が[int]のデータ型以外の場合
        if type(columnNumber_From) is not int:
           raise Exception

        # [columnNumber_To]が[int]のデータ型以外の場合
        if type(columnNumber_To) is not int:
           raise Exception

        # [headerName_To]が[string]のデータ型以外の場合
        if type(headerName_To) is not str:
           raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # columnNumber_FromがListの範囲を超えていた
        if (columnNumber_From < 1 or columnNumber_From > source.shape[1]):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER_FROM, columnNumber_From)
            return

        # colulmnNumber_To = 「0」の場合、最終列に追加する
        if columnNumber_To == 0:
            columnNumber_To = source.shape[1] + 1
        else:
            # columnNumber_Toがsourceの範囲を超えていた
            if (columnNumber_To < 1 or columnNumber_To > source.shape[1]):
                result = const.RESULT_ERR
                msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER_TO, columnNumber_To)
                return

        result1, msg1, headerColumnNumber = csvcol_getHeaderColumnNumber(source, headerName_To)
        # headerName_Toで指定されたヘッダ名が既に存在していた場合
        if headerColumnNumber > 0:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_HEADER_NAME_DUPLICATED.format(headerName_To)
            return
                   
        #source.insert(columnNumber_To - 1, source.shape[1], source.iloc[:, columnNumber_From - 1])
        source.insert(loc=columnNumber_To - 1, column=headerName_To, value=source.iloc[:, columnNumber_From - 1])

        #source.iloc[0, columnNumber_To - 1] = headerName_To
        #source.set_axis(1, range(source.shape[1]))
        
        newData = source
        countRows = source.shape[0]+1
        countColumns = source.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :    keyColumnNumbers (list)で指定した複数列の値を連結してuniqueなkeyとし、
            source(DataFrame)内に出現する数をcountする。そして結果をDataFrameの形式で出力する
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   keyにする列番号のlist
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   count結果をDataFrame形式にしたデータ
            int         :   csvファイルにした場合のデータの行数
            int         :   csvファイルにした場合のデータの列数  
"""
def csvcol_countEvery(source,keyColumnNumbers):
    HEADER_NAME_COUNT = 'count'
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # count結果をDataFrame形式にしたデータ
    countRows = 0                       # csvファイルにした場合のデータの行数
    countColumns = 0                    # csvファイルにした場合のデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [keyColumnNumbers]が[list]のデータ型以外の場合
        # keyColumnNumbersがNULL
        if (type(keyColumnNumbers) is not list) or (not len(keyColumnNumbers)):
            raise Exception

        keyUnique = np.unique(keyColumnNumbers).tolist()
        # [keyUnique] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in keyUnique):
            raise Exception
            
        # keyUniqueがsourceの範囲を超えていた
        if (source.shape[1] < max(keyUnique) or min(keyUnique) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_KEY_COLUMN_NUMBERS, keyColumnNumbers)
            return
        
        # リストの重複を削除
        keyColumnNumbers = list(set(keyColumnNumbers))
            
        # keyColumnNumbersを元にヘッダ名のリストを作成
        headers = []
        for key in keyColumnNumbers:
            result, msg, headerName = csvcol_getHeaderName(source, key)
            headers.append(headerName)
            
        #source.set_axis(1, range(1, source.shape[1] + 1))
        #newData = pandas.DataFrame(source.groupby(keyUnique, sort=False).size()).reset_index().astype(str)
        
        # 指定されたヘッダでグルーピングしサイズを数える        
        newData = source.groupby(headers, sort=False).size().reset_index().astype(str)
        # ヘッダの末尾にcountを追加
        headers.append(HEADER_NAME_COUNT)
        # ヘッダを設定
        newData.columns = headers
        
        #for col in keyColumnNumbers:
        #header = [headerName : result, msg, headerName = csvcol_getHeaderName(source, 0)]
        
        #newData.set_axis(1, range(newData.shape[1]))
        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

        #newData.iloc[0, countColumns-1] = HEADER_NAME_COUNT

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :    columnNumbers (list)で指定した複数列の値を乱数で埋める。
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   乱数で埋める列番号のlist
            int         :   乱数の桁数
            int         :   頭を０パディングするかどうかのフラグ True=する。False=しない。
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   指定列を乱数で埋めたDataFrame
            int         :   csvファイルにした場合のデータの行数
            int         :   csvファイルにした場合のデータの列数  
"""
def csvcol_fillRandomNumber(source, columnNumbers, digit, paddingFlg):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # count結果をDataFrame形式にしたデータ
    countRows = 0                       # csvファイルにした場合のデータの行数
    countColumns = 0                    # csvファイルにした場合のデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [columnNumbers]が[list]のデータ型以外の場合
        # columnNumbersがNULL
        if (type(columnNumbers) is not list) or (not len(columnNumbers)):
            raise Exception

        keyUnique = np.unique(columnNumbers).tolist()
        # [keyUnique] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in keyUnique):
            raise Exception

        # keyUniqueがsourceの範囲を超えていた
        if (source.shape[1] < max(keyUnique) or min(keyUnique) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBERS, columnNumbers)
            return
            
        # 列番号をindexに変換するため-1。
        columnNumbers[:] = [x - 1 for x in columnNumbers]

        # 指定された列数分処理を行う
        for col in columnNumbers:
            # 8桁の乱数を生成 (ヘッダを引いた行数分)
            randomIDs = random.sample(range(10**digit-1), k=source.shape[0])
            
            # 0でパディングし8ケタにする。
            if paddingFlg == True:
                randomIDs = [str(i).zfill(8) for i in randomIDs]
            else:
                randomIDs = [str(i) for i in randomIDs]

            # 乱数で置き換える
            source.iloc[:,col] = randomIDs

        newData = source
        countRows = source.shape[0]+1
        countColumns = source.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns        
        

"""
機能   :    columnNumbers (list)で指定した複数列の値を連番で埋める。
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   乱数で埋める列番号のlist
            int         :   乱数の桁数
            int         :   頭を０パディングするかどうかのフラグ True=する。False=しない。
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   指定列を乱数で埋めたDataFrame
            int         :   csvファイルにした場合のデータの行数
            int         :   csvファイルにした場合のデータの列数  
"""
def csvcol_fillSequentialNumber(source, columnNumbers, digit, paddingFlg):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # count結果をDataFrame形式にしたデータ
    countRows = 0                       # csvファイルにした場合のデータの行数
    countColumns = 0                    # csvファイルにした場合のデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [columnNumbers]が[list]のデータ型以外の場合
        # columnNumbersがNULL
        if (type(columnNumbers) is not list) or (not len(columnNumbers)):
            raise Exception

        keyUnique = np.unique(columnNumbers).tolist()
        # [keyUnique] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in keyUnique):
            raise Exception

        # keyUniqueがsourceの範囲を超えていた
        if (source.shape[1] < max(keyUnique) or min(keyUnique) < 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBERS, columnNumbers)
            return
            
        # 列番号をindexに変換するため-1。
        columnNumbers[:] = [x - 1 for x in columnNumbers]
        
        # 8桁の乱数を生成 (ヘッダを引いた行数分)
        # arangeの第２引数に、例えば10を指定すると9までの配列しかできないので0.1足している。
        sequentialIDs = np.arange(1, source.shape[0]+1, 1)

        # 0でパディングし8ケタにする。
        if paddingFlg == True: 
            sequentialIDs = [str(i).zfill(8) for i in sequentialIDs]
        else:
            sequentialIDs = [str(i) for i in sequentialIDs]

        # 指定された列数分処理を行う
        for col in columnNumbers:
            source.iloc[:,col] = sequentialIDs
        
        newData = source
        countRows = source.shape[0]+1
        countColumns = source.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns
        
if __name__=='__main__':
    pass
