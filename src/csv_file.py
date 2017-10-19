# -*- coding: utf-8 -*-
"""
csvファイルに対して処理を行うmodule
"""

import pandas
import re
import constants as const
from os import path
from csv import QUOTE_ALL
from pandas.io.common import EmptyDataError

"""
機能   :    csvファイルを読み込み、DataFrameに変換する
            csvファイルにヘッダが無い場合、DataFrame(newData)のheaderには、1から始まる列番号を自動的に設定する
引数   :
            string      :   csvファイのfull path
            int         :   csvファイルにheader行が存在するかを表すflag　（0 = header行が無い、　1 = header行が有る）
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   DataFrameに変換したデータ
            int         :   csvファイル内のデータの行数
            int         :   csvファイル内のデータの列数
"""
def csvfl_csvToDataFrame (csvFullPath, existHeaderFlag):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # DataFrameに変換したデータ
    countRows = 0                       # csvファイル内のデータの行数
    countColumns = 0                    # csvファイル内のデータの列数

    try:
        # [csvFullPath]が[string]のデータ型以外の場合
        if type(csvFullPath) is not str:
           raise Exception

        # [existHeaderFlag]が[int]のデータ型以外、または [existHeaderFlag]が[int]のデータ型であり、且つ０、１以外の場合
        if type(existHeaderFlag) is not int or (existHeaderFlag != 0 and existHeaderFlag != 1):
           raise Exception

        csvFullPath = csvFullPath.strip()
        # CSVファイルがない
        if not path.isfile(csvFullPath):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_NOT_EXIST_FILE.format(csvFullPath)
            return

        file_extension = path.splitext(path.basename(csvFullPath))[1]
        # CSVファイルのフォーマットが不正
        if (str.lower(file_extension) != const.CSV_EXTENSION):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_FILE
            return

        # csvファイルにヘッダが無い場合、DataFrame(newData)のheaderには、1から始まる列番号を自動的に設定する
        if existHeaderFlag == 0:
            tp = pandas.read_csv(csvFullPath, sep=const.CSV_SEP, encoding=const.CSV_ENCODING, dtype=str, header=None,
                                 skipinitialspace=True, keep_default_na=False, low_memory=False, chunksize=10000)
            newData = pandas.concat(tp, ignore_index=True)
            newData.set_axis(1, range(1, newData.shape[1] + 1))
        else:
            tp = pandas.read_csv(csvFullPath, sep=const.CSV_SEP, encoding=const.CSV_ENCODING, dtype=str, header=0,
                                 skipinitialspace=True, keep_default_na=False, low_memory=False, chunksize=10000)
            newData = pandas.concat(tp, ignore_index=True)

        countRows = newData.shape[0] + 1
        countColumns = newData.shape[1]

    # CSVファイルがない
    except OSError:
        result = const.RESULT_ERR
        msg = const.MSG_ERR_NOT_OPEN_FILE.format(csvFullPath)

    # CSVファイルのフォーマットの中身がNULL
    except EmptyDataError:
        result = const.RESULT_ERR
        msg = const.MSG_ERR_EMPTY_FILE

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :     DataFrame形式のデータをcsvファイルに出力する
            header行を出力するかどうかを選択することが出来る
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   header行を出力するかを表すflag　（0 = header行を出力しない、　1 = header行を出力する）
            int         :   上書き保存するかどうかのflag
            string      :   csvファイルの出力先
            string      :   出力するcsvファイの名前
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            string      :   出力したcsvファイルの名前
"""
def csvfl_dataFrameToCsv (source, existHeaderFlag, ovwFlag, directory, csvName):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newName = csvName                   # 出力したcsvファイルの名前

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [existHeaderFlag]が[int]のデータ型以外、または [existHeaderFlag]が[int]のデータ型であり、且つ０、１以外の場合
        if type(existHeaderFlag) is not int or (existHeaderFlag != 0 and existHeaderFlag != 1):
            raise Exception

        # [ovwFlag]が[bool]のデータ型以外の場合
        if type(ovwFlag) is not bool:
            # [ovwFlag]が[int]のデータ型以外、または [ovwFlag]が[int]のデータ型であり、且つ０、１以外の場合
            if type(ovwFlag) is not int or (ovwFlag != 0 and ovwFlag != 1):
                raise Exception

        # [directory]が[string]のデータ型以外の場合
        if type(directory) is not str:
           raise Exception

        # [csvName]が[string]のデータ型以外の場合
        if type(csvName) is not str:
           raise Exception

        directory = directory.strip()
        newName = csvName.strip()

        # sourceがNULL
        if not source.shape[0] and not source.shape[1]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # [newName]が空白の場合
        # ファイル名が不正 (¥　/　:　*　?　"　<　>　|が含まれる)
        if newName == "" or re.match(r'.*[\\\¥\/\:\*\?\"\<\>\|].*', newName):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FILE_NAME_CSV.format(newName)
            return

        file_extension = path.splitext(newName)[1]
        # 拡張子がないファイル名の場合
        if (str.lower(file_extension) != const.CSV_EXTENSION):
            newName+=const.CSV_EXTENSION

         # 指定されたdirectoryがない
        if not path.isdir(directory):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_NOT_EXIST_DIRECTORY.format(directory)
            return

        csvFullPath = path.join(directory, newName)
        fileName = path.splitext(newName)[0]
        # ovwFlag(上書き保存flag)=Falseが設定され
        # ovwFlag(上書き保存flag)=0が設定され
        if(ovwFlag == False or ovwFlag == 0):
            i = 1;
            # ファイルが既に存在している場合
            while (path.isfile(csvFullPath)):
                newName = fileName + '(' + str(i) + ')'+ const.CSV_EXTENSION
                csvFullPath = path.join(directory, newName)
                i+=1

        # CSVファイル出力
        if existHeaderFlag == 0: # header行を出力しない
            source.to_csv(csvFullPath, sep=const.CSV_SEP, index=False, header=False, line_terminator=const.CSV_LINE_TERMINATOR,
                          quotechar=const.CSV_QUOTECHAR, quoting=QUOTE_ALL, encoding=const.CSV_ENCODING, chunksize=10000)
        else:
            source.to_csv(csvFullPath, sep=const.CSV_SEP, index=False, header=True, line_terminator=const.CSV_LINE_TERMINATOR,
                          quotechar=const.CSV_QUOTECHAR, quoting=QUOTE_ALL, encoding=const.CSV_ENCODING, chunksize=10000)

    # CSV ファイルが保存できない
    except PermissionError:
        result = const.RESULT_ERR
        msg = const.MSG_ERR_CREATE_FILE.format(csvFullPath)

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newName

if __name__=='__main__':
    pass