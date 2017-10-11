# -*- coding: utf-8 -*-
"""
Unit test suite by using "discover" method.
"""
import unittest
import datetime

#--------------------------------------------
# テストスイートを作成
def suite():
    # TestSuiteから空っぽのテストスイートを作成します
    test_suite = unittest.TestSuite()
    
    # discoverメソッドを用いて、testディレクトリ以下からテストクラスを見つける
    all_test_suite = unittest.defaultTestLoader.discover("test", pattern="testCsv_*.py")
    
    # 見つけたテストクラスをテストスイートに追加します
    for ts in all_test_suite:
        test_suite.addTest(ts)
        
    return test_suite

#--------------------------------------------
if __name__ == "__main__":
    d = datetime.datetime.today()
    print("start ::: " +  d.strftime("%x %X"))
    
    # テストスイートを呼び出して実行します
    uts = suite()
    unittest.TextTestRunner().run(uts)
    
    d = datetime.datetime.today()
    print("finish ::: " +  d.strftime("%x %X"))
