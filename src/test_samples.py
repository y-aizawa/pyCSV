# -*- coding: utf-8 -*-
"""
Unit test suite by using "discover" method.
"""
import unittest

#--------------------------------------------
# テストスイートを作成
def suite():
    # TestSuiteから空っぽのテストスイートを作成します
    test_suite = unittest.TestSuite()
    
    # discoverメソッドを用いて、testディレクトリ以下からテストクラスを見つける
    all_test_suite = unittest.defaultTestLoader.discover("test", pattern="test_*.py")
    
    # 見つけたテストクラスをテストスイートに追加します
    for ts in all_test_suite:
        test_suite.addTest(ts)
        
    return test_suite

#--------------------------------------------
if __name__ == "__main__":
    print("Start --- Unit Test Suite ---")
    # テストスイートを呼び出して実行します
    uts = suite()
    unittest.TextTestRunner().run(uts)
    print("Finish --- Unit Test Suite ---")