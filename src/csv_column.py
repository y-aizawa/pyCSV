# -*- coding: utf-8 -*-
"""
csvファイルをlistにconvertしたデータに対して、column（列）を編集するmodule。
"""

import pandas
import constants as const

"""
機能   :  headerNameとheader名が一致する列番号を取得する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ
          header名称
戻り値  :  ステータス
          メッセージ
          headerのcolumnNumber 
"""
def csvcol_getHeaderIndex(source, headerName):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    headerColumnNumber = 0

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

        i = 0
        while (i < (len(source[0]))):
            if(headerName == source[0][i]):
                # 処理が問題なく完了した。
                headerColumnNumber = i + 1
                break
            i = i + 1
        if (headerColumnNumber == 0):
            # headerが見つからない。
            result = const.RESULT_ERR
            msg = const.MSG_ERR_NOT_FOUND_HEADER_NAME.format(headerName)
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, headerColumnNumber

"""
機能   :  headerColumnNumberと一致するheader名を取得する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ
          headerのcolumnNumber
戻り値  :  ステータス
          メッセージ
          header名称
"""
def csvcol_getHeaderName(source, headerColumnNumber):
    result = const.RESULT_COMPLETE
    msg = const.MSG_COMPLETE
    headerName = ""
    
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

        if(headerColumnNumber <= (len(source[0])) and headerColumnNumber > 0):
            # 処理が問題なく完了した。
            headerName = source[0][headerColumnNumber-1]
        else:
            # headerColumnNumberがListの範囲を超えていた。
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_HEADER_COLUMN_NUMBER, headerColumnNumber)
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, headerName

"""
機能   :  指定した列を削除する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ
          削除する列番号
戻り値  :  ステータス
          メッセージ
          列削除後のデータをlistにしたもの
          csvファイルにした場合のデータの行数
          csvファイルにした場合のデータの列数       
"""
def csvcol_deleteColumn(source, columnNumber):
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
        if (columnNumber <= len(source[0]) and columnNumber > 0):
            #2列目を削除したい場合[2]が渡されるので、-1する。
            df.drop(df.columns[columnNumber-1], axis=1, inplace=True)
            newData = df.values.tolist()
            countRows = df.shape[0]
            countColumns = df.shape[1]
        else:
            # columnNumberがListの範囲を超えていた。
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER, columnNumber)
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:       
        return result, msg, newData, countRows, countColumns

"""
機能   :  columnNumbers (list)で指定した複数の列を削除する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ
          削除する列番号のlist
戻り値  :  ステータス
          メッセージ
          列削除後のcsvデータのlist
          csvファイルにしたときのデータの行数
          csvファイルにしたときのデータの列数
"""
def csvcol_deleteColumns(source, columnNumbers):
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

        for i in range(len(columnNumbers)):
            if (columnNumbers[i] > len(source[0]) or columnNumbers[i] < 1):
                # columnNumberがListの範囲を超えていた。
                result = const.RESULT_ERR
                msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_COLUMN_NUMBER, const.NAME_COLUMN_NUMBERS, columnNumbers)
                return

        df = pandas.DataFrame(source)
        # 2列目を削除したい場合[2]が渡されるので、-1する。
        columnNumbers[:] = [x - 1 for x in columnNumbers]
        df.drop(df.columns[columnNumbers], axis=1, inplace=True)
        countColumns = df.shape[1]
        if(countColumns == 0):
            countRows = 0
            newData = []
        else:
            countRows = df.shape[0]
            newData = df.values.tolist()
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  指定した列(colulmnNumber_From)を、指定した列(colulmnNumber_To)に挿入する。処理後の列数は、処理前に比べて1増加する。
引数   :  csv_file.pyのcsvfl_csvToList()で作成したlistデータと同形式のデータ
          複写元の列番号
          複写先の列番号
戻り値  :  ステータス
          メッセージ
          複写後のlist
          csvファイルにしたときのデータの行数
          csvファイルにしたときのデータの列数
"""
def csvcol_duplicateColumn(source, columnNumber_From, columnNumber_To = None):
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

        if (columnNumber_From < 1 or columnNumber_From > len(source[0])):
            # columnNumber_FromがListの範囲を超えていた。
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER_FROM, columnNumber_From)
            return

        if (columnNumber_To is None):
            # colulmnNumber_To = nullの場合、最終列に追加する。
            columnNumber_To = len(source[0]) + 1
        else:
            if (columnNumber_To < 1 or columnNumber_To > len(source[0])):
                # columnNumber_ToがListの範囲を超えていた。
                result = const.RESULT_ERR
                msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_COLUMN_NUMBER_TO, columnNumber_To)
                return

        df = pandas.DataFrame(source)
        df.insert(columnNumber_To - 1, len(source[0]), df[[columnNumber_From - 1]])
        newData = df.values.tolist()
        countRows = df.shape[0]
        countColumns = df.shape[1]
    except Exception:
        # 予期しなかったError。
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED
    finally:
        return result, msg, newData, countRows, countColumns


if __name__=='__main__':
    print("")