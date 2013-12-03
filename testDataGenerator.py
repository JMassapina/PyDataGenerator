#!/usr/bin/python3

import unittest
import DataGenerator as dg
import locale

# View all available locales
# locale -a
#
# View current locale settings
# locale
#
# Add locale to system
# sudo locale-gen de_DE.utf8


class TestSqliteDataSource(unittest.TestCase):
    
    def testStuff(self):
        dataSource = dg.SqliteDataSource()
        dataSource.open(True, dbFile='./test.sqlite3')
        dataSource.loadDataItems(
            './locales',
            ['maleFirstNames'])
        dataSource.close()



# class TestDataSource(unittest.TestCase):
    # 
    # def testload_currentLocale(self):
        # locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
        # 
        # # print(str(locale.localeconv()))
        # # print(str(locale.getdefaultlocale()))
        # #print(str(locale.getlocale()))
        # dg.DATA_SOURCE.load(
            # './locales',
            # './data.sqlite',
            # None,
            # ['maleFirstNames'])
# 
# 
# class TestRandomFirstName(unittest.TestCase):
    # 
    # def setUp(self):
        # pass
    # 
    # def testDefaultLocal(self):
        # print(dg.randomFirstName(sex='M'))

if __name__ == '__main__':
    unittest.main()

