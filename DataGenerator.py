#!/usr/bin/python3

from random import random, choice, randint
from locale import getlocale
from os.path import exists, join
from datetime import datetime

import sqlite3

MALE_FIRST_NAMES = 'maleFirstNames'

class DataSource:
    
    MALE_NAMES = 'maleNames'
    FEMALE_NAMES = 'femaleNames'
    LAST_NAMES = 'lastNames'
    
    def __init__(self, dataSource):
        self.dataSource = dataSource

        
    def loadDataItems(self, localesDir, dataItems=None, locales=None):
        pass
        # if localesDir == None or len(localesDir.strip()) == 0:
            # raise Exception('localesDir not specified')
            # 
        # if not exists(localesDir):
            # raise Exception("%s not found" % localesDir)
            # 
        # self.localesDir = localesDir
        # 
        # if dataItems == None or len(dataItems) == 0:
            # dataItems = DataSource.ALL_DATA_ITEMS
            # 
        # if locales == None or len(locales) == 0:
            # locales = [getlocale()[0]]
        # 
        # for dataItem in dataItems:
            # if dataItem not in DataSource.ALL_DATA_ITEMS:
                # raise Exception('unrecognized data item %s' % dataItem)
            # for locale in locales:
                # self.loadDataItem(dataItem, locale)
        
    def loadDataItem(self, dataItem, locale, *posArgs, **keywords):
        raise Exception('implement this method in subclass')
        
    def randomMaleName(self):
        return self.randomChoice(DataSource.MALE_NAMES)
        
    def randomFemaleName(self):
        return self.randomChoice(DataSource.FEMALE_NAMES)
        
    def randomLastName(self):
        return self.randomChoice(DataSource.LAST_NAMES)
        
class InMemoryDataSource(DataSource):
    
    def __init__(self):
        self.dataItems = {}
    
    def loadDataItem(self, dataItem, locale, *posArgs, **keywords):
        if 'values' not in keywords.keys():
            raise Exception('values not specified')
        
        self.dataItems[dataItem] = keywords['values']
        
    def randomChoice(self, dataItemName):
        if dataItemName not in self.dataItems.keys():
            raise Exception(dataItemName + " not present in data items")
        return choice(self.dataItems[dataItemName])
        
    
class SqliteDataSource(DataSource):
    
    def __init__(self):
        self.conn = None
        
        
    def open(self, dbFile):
        '''Opens an existing sqllite file if file exists.  Will create one if 
        it does not exist'''
        
        self.conn = sqlite3.connect(dbFile)
        
    def loadDataItem(self, dataItem, locale):
        # Call base class method to validate that  files exist
        DataSource.loadDataItem(self, dataItem, locale)
        print('loadDataItem')
        
        cursor = self.conn.cursor()
        
        if not self.hasTable('nameControlTable'):
            cursor.execute(
                """create table if not exists maleFirstNames (
                    tableName text)""")
        
        if self.hasTable(dataItem):
            if self.hasRecords(dataItem):
                cursor.execute('delete maleFirstNames')
        else:
            cursor.execute(
                """create table if not exists maleFirstNames (
                    name text, 
                    randSort integer)""")
        
        sourceFile = open(self.sourceFilePath, 'r')
        
        for line in sourceFile:
            line = line.strip()
            print(line)
            cursor.execute(
                "insert into maleFirstNames (name) values (?)", 
                (line,))
            
        
        sourceFile.close()
        
        
    def hasTable(self, tableName):
        cursor = self.conn.cursor()
        cursor.execute(
            "select * from sqlite_master where tbl_name = ?", 
            (tableName,))
        for row in cursor:
            return True
        return False
        
        
    def hasRecords(self, tableName):
        cursor = self.conn.cursor()
        cursor.execute(
            "select count(*) from %s" % tableName)
        for row in cursor:
            if row[0] == 0:
                return False
        return True
        
        
    def randomMaleName(self):
        pass
        
    def randomFemaleName(self):
        pass
            
    def close(self):
        if self.conn != None:
            self.conn.close()
    
    
    # def __init__(self):
        # self.conn = None
        # 
    # def reLoad(self):
        # """opens an existing sqlite database"""
        # pass
        # 
    # def load(self, localesDir, databaseFile, locales=None, dataItems=None):
        # """clears database and loads data into sqlite database from file."""
        # # check if localesDirectory exists
        # 
        # 
        # 
        # if locales == None or len(locales) == 0:
            # locales = [getlocale()[0]]
        # 
        # for locale in locales:
            # # do this in a cross platform way
            # localeDir = localesDir + '/' + locale
            # print(localeDir)
            # 
    # def close(self):
        # self.conn.close()

def defaultGenerateAge():
   return 90 * random()
   
def defaultGenerateSex():
    x = random()
    if x <= 0.495:
        return 'male'
    if x > 0.495 and x < 0.99:
        return 'female'
    return 'unknown'


class DefaultContext:

    def __init__(self):
        self.currentDateTime = datetime(2001, 1, 1)
        self.currentDateTime = self.currentDateTime.now()
        
        self.generateAgeRule = defaultGenerateAge
        self.generateSexRule = defaultGenerateSex

class Person:
    
    SEXES = ['male', 'female', 'unknown']
    
    def __init__(self, dataSource, context=None, **keywords):
        self.dataSource = dataSource
        
        self.context = context
        if self.context == None:
            self.context = DefaultContext()
            
        
        if 'sex' in keywords.keys():
            self.sex = keywords['sex']
            if self.sex not in Person.SEXES:
                raise(ValueError())
        else:
            self.sex = self.context.generateSexRule()
            
        self.age = self.context.generateAgeRule()
        
        self.dateOfBirth = self.context.defaultSexRule()
            
        self.firstName, tempSex = self.firstOrMiddleName(
            self.sex, 
            'firstName', 
            **keywords)
            
        self.middleName, tempSex = self.firstOrMiddleName(
            tempSex,
            'middleName',
            **keywords)
        
        self.lastName = self.dataSource.randomLastName()
        
        
        
    def firstOrMiddleName(self, sex, nameType, **keywords):
        if nameType in keywords.keys():
            return keywords[nameType]
        if sex == 'male' or (sex == 'unknown' and random() < 0.5):
            return self.dataSource.randomMaleName(), 'male'
        return self.dataSource.randomFemaleName(), 'female'
        
        

        
        
    def __str__(self):
        array = {
            'sex': self.sex,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'lastName': self.lastName,
            'age':self.age}
        return str(array)
        
        
# def randomMiddleName(sex):
    # return randomFirstName(sex)
# 
# def randomLastName(firstPart='', divider=' '):
    # return choice(LAST_NAMES)

# class RandomPerson():
    # def __init__(self, **keywords):
# 
            # 
# 
        # 
        # if 'middleName' in keywords.keys():
            # self.middleName = keywords['middleName']
        # else:
            # self.middleName = randomMiddleName(self.sex)
            # 
        # if 'lastName' in keywords.keys():
            # self.lastName = keywords['lastName']
        # self.lastName = randomLastName(self.sex)
        # 
        # if 'minAge' in keywords.keys():
            # minAge = keywords['minAge']
            # # add check to ensure minAge is numeric
        # else:
            # minAge = 0
            # 
        # if 'maxAge' in keywords.keys():
            # maxAge = keywords['maxAge']
            # # add check to ensure maxAge is numeric
        # else:
            # maxAge = 110
            # 
        # self.age = randint(minAge*100, maxAge*100)/100.0
            


# def randomCouple(**keywords):
    # """Will generate two random people who may or may not have the last name.
    # This function will override values for the sex and lastName keywords"""
    # if random() < 0.05:
        # # same - sex couple
        # keywords['sex'] = randomSex()
        # if random() < 0.33:
            # # share last_name
            # keywords['lastName'] = randomLastName()
            # return RandomPerson(**keywords), RandomPerson(**keywords)
        # return RandomPerson(**keywords), RandomPerson(**keywords)
# 
    # if random() < 0.70 and 'lastName' not in keywords.keys():
        # keywords['lastName'] = randomLastName()
        # 
    # keywords['sex'] = 'M'
    # person1 = RandomPerson(**keywords)
    # 
    # keywords['sex'] = 'F'
    # person2 = RandomPerson(**keywords)
    # return person1, person2
        

        

if __name__ == '__main__':
    pass

