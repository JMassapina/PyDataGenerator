#!/usr/bin/python3

from random import random, choice, randint
from locale import getlocale
from os.path import exists, join

import sqlite3


class DataSource:
    
    ALL_DATA_ITEMS = ['maleFirstNames']
    
    def __init__(self):
        """Creates a new DataSource with no data.  Subclasses may also create
        a new DataSource object from an existing file or database."""
        self.localesDir = None
        self.sourceFilePath = None

        
    def loadDataItems(self, localesDir, dataItems=None, locales=None):
        
        if localesDir == None or len(localesDir.strip()) == 0:
            raise Exception('localesDir not specified')
            
        if not exists(localesDir):
            raise Exception("%s not found" % localesDir)
            
        self.localesDir = localesDir
        
        if dataItems == None or len(dataItems) == 0:
            dataItems = DataSource.ALL_DATA_ITEMS
            
        if locales == None or len(locales) == 0:
            locales = [getlocale()[0]]
        
        for dataItem in dataItems:
            if dataItem not in DataSource.ALL_DATA_ITEMS:
                raise Exception('unrecognized data item %s' % dataItem)
            for locale in locales:
                self.loadDataItem(dataItem, locale)
        
    def loadDataItem(self, dataItem, locale):
        """DataSource.loadDataItem will validate that the directory and 
        data file exist"""
        if self.localesDir == None:
            raise Exception('localesDir not set')
        
        self.sourceFilePath = join(self.localesDir, locale, dataItem + '.txt')
        if not exists(self.sourceFilePath):
            raise Exception('source file %s not found' % self.sourceFilePath)
        
        
class InMemoryDataSource(DataSource):
    pass
    
    
class SqliteDataSource(DataSource):
    
    def __init__(self):
        self.conn = None
        
        
    def open(self, dbFile):
        '''Opens an existing sqllite file if file exists.  Will create one if 
        it does not exist'''
        
        self.conn = sqlite3.connect(dbFile)
        
    def loadDataItem(self, dataItem, locale):
        # Call base class method to validate that source files exist
        DataSource.loadDataItem(self, dataItem, locale)
        print('loadDataItem')
        
        cursor = self.conn.cursor()
        
        if self.hasTable(dataItem):
            cursor.execute('delete maleFirstNames')
        else:
            sql = "create table if not exists maleFirstNames (name text, rand_sort integer)"
            cursor.execute(sql)
        
        sourceFile = open(self.sourceFilePath, 'r')
        
        print(dir(sourceFile))
        
        sourceFile.close()
        
        
    def hasTable(self, tableName):
        cursor = self.conn.cursor()
        cursor.execute("select * from sqlite_master where tbl_name = ?", (tableName,))
        for row in cursor:
            return True
        return False
        
        
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





class Person:
    
    def __init__(self):
        self.sex = None
        self.firstName = None
        self.middleName = None
        self.lastName = None
        self.age = None
    
    def __str__(self):
        array = {
            'sex': self.sex,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'lastName': self.lastName,
            'age':self.age}
        return str(array)
    
        
class PersonGenerator:
    
    def __init__(self, dataSource):
        self.dataSource = dataSource
        
    def next(self, **keywords):
        
        person = Person()        
        
        if 'sex' in keywords.keys():
            person.sex = keywords['sex']
            if person.sex not in ('M','F','H','U'):
                raise(ValueError())
        else:
            person.sex = PersonGenerator.randomSex()
            
            
        if 'firstName' in keywords.keys():
            person.firstName = keywords['firstName']
        elif person.sex == 'M':
            person.firstName = self.dataSource.randomMaleName()
        elif person.sex == 'F':
            person.firstName = self.dataSource.randomFemaleName()
        elif random() < 0.5:
            person.firstName = self.dataSource.randomMaleName()
        else:
            person.firstName = self.dataSource.randomFemaleName()
            
        return person
        
        
    def randomSex():
        x = random()
        if x <= 0.495:
            return 'M'    
        if x > 0.495 and x < 0.99:
            return 'F'    
        if x >= 0.99 and x < 0.995:
            return 'H'
        return 'U'

        
def randomMiddleName(sex):
    return randomFirstName(sex)

def randomLastName(firstPart='', divider=' '):
    return choice(LAST_NAMES)

class RandomPerson():
    def __init__(self, **keywords):

            

        
        if 'middleName' in keywords.keys():
            self.middleName = keywords['middleName']
        else:
            self.middleName = randomMiddleName(self.sex)
            
        if 'lastName' in keywords.keys():
            self.lastName = keywords['lastName']
        self.lastName = randomLastName(self.sex)
        
        if 'minAge' in keywords.keys():
            minAge = keywords['minAge']
            # add check to ensure minAge is numeric
        else:
            minAge = 0
            
        if 'maxAge' in keywords.keys():
            maxAge = keywords['maxAge']
            # add check to ensure maxAge is numeric
        else:
            maxAge = 110
            
        self.age = randint(minAge*100, maxAge*100)/100.0
            


def randomCouple(**keywords):
    """Will generate two random people who may or may not have the last name.
    This function will override values for the sex and lastName keywords"""
    if random() < 0.05:
        # same - sex couple
        keywords['sex'] = randomSex()
        if random() < 0.33:
            # share last_name
            keywords['lastName'] = randomLastName()
            return RandomPerson(**keywords), RandomPerson(**keywords)
        return RandomPerson(**keywords), RandomPerson(**keywords)

    if random() < 0.70 and 'lastName' not in keywords.keys():
        keywords['lastName'] = randomLastName()
        
    keywords['sex'] = 'M'
    person1 = RandomPerson(**keywords)
    
    keywords['sex'] = 'F'
    person2 = RandomPerson(**keywords)
    return person1, person2
        

        

if __name__ == '__main__':
    for i in range(5):
        name = RandomPerson()
        print(name)
    
    for i in range(10):
        person1, person2 = randomCouple()
    
    print('finished')
