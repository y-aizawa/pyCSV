# -*- coding: utf-8 -*-
"""
Data anonymization
"""
import datetime

from sample_csv_file import csvfl_csvToList
from sample_csv_file import csvfl_listToCsv
from sample_csv_row import csvrec_sampling
from sample_csv_row import csvrec_matchRowNumbers
from sample_csv_row import csvrec_deleteRows
from sample_csv_column import csvcol_deleteCollumns
from sample_csv_column import csvcol_countEvery
from sample_csv_column import csvcol_countEvery_TowColumns



# 都道府県名、学校名を削除
def do_delCol():
 
    csvFullPath = r'C:\work\pyCSV\data\2_都道府県、教委なし。学校あり_sampling_大小なし\_JH_公立のみ_2_都道府県、教委なし。学校あり_sampling001-1_大小なし.csv'
    newData=[]
 
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))

    #都道府県名、学校名フィールド削除
    result, newData, countRows, countColumns = csvcol_deleteCollumns(newData, [10,11])        
    print("Number of row after deletion of columns is -> " + str(countRows))
    print("Number of column after deletion of columns is -> " + str(countColumns))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "JH_公立のみ_2_都道府県、教委なし。学校あり_sampling001-1_大小なし_学校削除.csv")
    print("The name of new file is -> " + newName)
    print("Number of rows in the new file is -> " + str(countRows))


# 公立校、私立校を削除
def do_delRow():
 
    csvFullPath = r'C:\work\pyCSV\data\H27_児童.csv'
    newData=[]
 
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))

    #国立人数カウント
    result, rowNumbersKOKU = csvrec_matchRowNumbers(newData, 6, "1")
    print("KOKURITSU -> " + str(len(rowNumbersKOKU)))

    #国立のデータを削除
    result, newData, countRows, countFields = csvrec_deleteRows(newData, rowNumbersKOKU)        
    print("Number of rows after deletion of KOKURITSU -> " + str(countRows))

    #私立人数カウント
    result, rowNumbersSHI = csvrec_matchRowNumbers(newData, 6, "3")
    print("SHIRITSU -> " + str(len(rowNumbersSHI)))

    #私立のデータを削除
    result, newData, countRows, countFields = csvrec_deleteRows(newData, rowNumbersSHI)        
    print("Number of rows after deletion of SHIRITSU -> " + str(countRows))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "EL_KouritsuOnly")
    print("The name of new file is -> " + newName)
    print("Number of rows in the new file is -> " + str(countRows))


#国公私をカウント
def do_count():
 
    csvFullPath = r'C:\work\pyCSV\data\H27_生徒.csv'
    newData=[]
 
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))

    #国立人数カウント
    result, rowNumbers = csvrec_matchRowNumbers(newData, 6, "1")
    print("KOKURITSU -> " + str(len(rowNumbers)))

    #公立人数カウント
    result, rowNumbers = csvrec_matchRowNumbers(newData, 6, "2")
    print("KOURITSU -> " + str(len(rowNumbers)))

    #私立人数カウント
    result, rowNumbers = csvrec_matchRowNumbers(newData, 6, "3")
    print("SHIRITSU -> " + str(len(rowNumbers)))


#サンプリング
def do_sampling():
 
    csvFullPath = r'C:\work\pyCSV\data\_EL_公立のみ_2_都道府県、教委なし。学校あり_大小なし_学校削除.csv'
    newData=[]
    countRows = 0
    countColumns = 0
    
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))
    
    #サンプリング
    result, newData, countRows, countColumns = csvrec_sampling(newData, 0.1)
    print("Number of sampled row is -> " + str(countRows))
    print("Number of column after sampling is -> " + str(countColumns))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "EL_公立のみ_2_都道府県、教委なし。学校あり_大小なし_学校削除_sampling010")
    print("The name of new file is -> " + newName)


#大規模校リスト作成
def do_createLargeSchoolList():
 
    csvFullPath = r'C:\work\pyCSV\data\_EL_公立のみ.csv'
    newData=[]
    countRows = 0
    countColumns = 0
    
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))
    
    #学校ごとの生徒数取得 学校名は15列　コードは14列
    result, listCountStudents = csvcol_countEvery(newData, 14)
    print("The total number of school is -> " + str(len(listCountStudents)))
    
    #大規模校のみ抽出
    newList = []
    for row in listCountStudents:
        if row[1] >= 241:
            newList.append(row)
    print("The number of schools which has 241 students or more is -> " + str(len(newList)))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newList, True, directory, "EL_公立のみ_0_大規模校(241名以上)コード")
    print("The name of new file is -> " + newName)

#小規模校リスト作成
def do_createSmallSchoolList():
 
    csvFullPath = r'C:\work\pyCSV\data\_JH_公立のみ.csv'
    newData=[]
    countRows = 0
    countColumns = 0
    
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))
    
    #学校ごとの生徒数取得 学校名は15列　コードは14列
    result, listCountStudents = csvcol_countEvery(newData, 14)
    print("The total number of school is -> " + str(len(listCountStudents)))
    
    #大規模校のみ抽出
    newList = []
    for row in listCountStudents:
        if row[1] <= 10:
            newList.append(row)
    print("The number of schools which has 10 students or less is -> " + str(len(newList)))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newList, True, directory, "_JH_公立のみ_0_小規模校(10名以下)コード")
    print("The name of new file is -> " + newName)

#小規模校、大規模校データ削除
def do_deleteLargeAndSmallSchool():
 
    # 元データ読み込み   
    csvFullPath = r'C:\work\pyCSV\data\_EL_公立のみ_2_都道府県、教委なし。学校あり.csv'
    newData=[]
    countRows = 0
    countColumns = 0
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))

    # 大規模校データ読み込み-------------------------------------------------------------
    csvLargeShCode =  r'C:\work\pyCSV\data\_EL_公立のみ_0_大規模校(241名以上)コード.csv'
    listL = []
    countRows = 0
    countColumns = 0
    result, listL, countRows, countColumns = csvfl_csvToList (csvLargeShCode)
    print("The number of schools which has 241 students or more is -> " + str(countRows))
    
    #大規模校のレコードを削除
    for row in listL:
        # 削除対処の学校コードを取得
        code = row[0]
        # 削除対象の学校コードが存在する行番号を取得
        result, rowNumbers = csvrec_matchRowNumbers(newData, 10, code)
        # 削除
        result, newData, countRows, countFields = csvrec_deleteRows(newData, rowNumbers)
       
    print("The number of rows after deletion of schools which has 241 students or more is -> " + str(countRows))

    # 小規模校データ読み込み-------------------------------------------------------------
    csvSmallShCode =  r'C:\work\pyCSV\data\_EL_公立のみ_0_小規模校(10名以下)コード.csv'
    listS = []
    countRows = 0
    countColumns = 0
    result, listS, countRows, countColumns = csvfl_csvToList (csvSmallShCode)
    print("The number of schools which has 10 students or less is -> " + str(countRows))
    
    # 小規模校のレコードを削除
    for row in listS:
        # 削除対処の学校コードを取得
        code = row[0]
        # 削除対象の学校コードが存在する行番号を取得
        result, rowNumbers = csvrec_matchRowNumbers(newData, 10, code)
        # 削除
        result, newData, countRows, countFields = csvrec_deleteRows(newData, rowNumbers)
        
    print("The number of rows after deletion of schools which has 10 students or less is -> " + str(countRows))    

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (newData, True, directory, "EL_公立のみ_2_都道府県、教委なし。学校あり_大小なし")
    print("The name of new file is -> " + newName)


#都道府県別受験者数リスト
def do_csvcol_countEvery_TowColumns():
 
    csvFullPath = r'C:\work\pyCSV\data\H27_生徒.csv'
    newData=[]
    countRows = 0
    countColumns = 0
    
    #csv読み込み
    result, newData, countRows, countColumns = csvfl_csvToList (csvFullPath)
    print("Total number of row is -> " + str(countRows))
    print("Total number of column is -> " + str(countColumns))
    
    result, ret = csvcol_countEvery_TowColumns(newData, 2, 3)
    print("The total number of columns -> " + str(len(ret)))

    directory = r'C:\work\pyCSV\data\_'
    result, newName, countRows = csvfl_listToCsv (ret, True, directory, "_JH_全_都道府県別受験者数")
    print("The name of new file is -> " + newName)

#============================ 
if __name__=='__main__':
    d = datetime.datetime.today()
    print("start ::: " +  d.strftime("%x %X"))

    do_csvcol_countEvery_TowColumns()

    print("\007")
    
    d = datetime.datetime.today()
    print("finish ::: " +  d.strftime("%x %X"))
