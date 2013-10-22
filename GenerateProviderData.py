
from DataGenerator import RandomPerson, randomCouple
from random import random

def formatName(person):
    return "%s, %s %s." % \
        (person.lastName, person.firstName, person.middleName[0])

class RandomProvider:
    def __init__(self, **keywords):
        if random() < 0.70:
            # provider is a couple
            while True:
                person1, person2 = randomCouple(minAge=21)
                if person1.sex != person2.sex:
                    self.name = "%s & %s" % \
                        (formatName(person1), formatName(person2))
                    break
        else:
            # provider is a single person
            person = RandomPerson(minAge=21)
            self.name = formatName(person)
        
    def __str__(self):
        array = {
            'name':self.name}
        return str(array)

if __name__ == '__main__':
    for i in range(5):
        provider = RandomProvider()
        print(str(provider))
