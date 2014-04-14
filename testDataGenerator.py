#!/usr/bin/python3

import unittest

from DataGenerator import \
    InMemoryDataSource, \
    Person
import locale

# View all available locales
# locale -a
#
# View current locale settings
# locale
#
# Add locale to system
# sudo locale-gen de_DE.utf8


# class TestDataSource(unittest.TestCase):
    # pass
# 
# 



class TestInMemoryDataSource(unittest.TestCase):
    
    def testStuff(self):
        dataSource = InMemoryDataSource()
        
        values = ['John', 'Robert', 'William', 'Andrew']
        dataSource.loadDataItem('maleNames','en_us', values=values)
        
        values = ['Elizabeth', 'Jennifer', 'Mary', 'Ann']
        dataSource.loadDataItem('femaleNames', 'en_us', values=values)
        
        values = ['Smith', 'Jones', 'Thomas', 'Davis']
        dataSource.loadDataItem('lastNames', 'en_us', values=values)
        
        person = Person(dataSource)
        
        
        print(str(person))
        
        # dataSource.loadDataItems(
            # './locales',
            # ['maleFirstNames'])
            # 
        # personGenerator = dg.PersonGenerator(dataSource)
        # for i in range(10):
           # print(personGenerator.next(sex='M'))

# class TestSqliteDataSource(unittest.TestCase):
    # 
    # def testStuff(self):
        # dataSource = dg.SqliteDataSource()
        # dataSource.open('./test.sqlite3')
        # dataSource.loadDataItems(
            # './locales',
            # ['maleFirstNames'])
            # 
        # personGenerator = dg.PersonGenerator(dataSource)
        # for i in range(10):
           # print(personGenerator.next(sex='M'))
            # 
        # dataSource.close()



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

