from collections import UserDict
class AddressBook(UserDict):
    data = list()
    def __init__(self, key, value, name, phone):
        super().__init__()
        self.data.append(Record(key, value, name, phone))
class Record:
    record = dict()
    def __init__(self, key, value, name, phone):
        self.record[f"{key}"] = value
        self.name = Name(name)
        self.phones = Phone(phone)
    def __delete__(self):
        del self.record
        del self.name
        del self.phones
    def reduct(self, key, value, name, phone):
        if key not in self.record:
            self.record[f"{key}"] = value
            self.name = Name(name)
            self.phones = Phone(phone)
class Field:
    def __str__(self):
        print(f"{self.__dict__}")
class Name(Field):
    def __init__(self, name):
        self.name = name
class Phone(Field):
    phones = list()
    def __init__(self, phone):
        if type(phone) == 'str':
            self.phones.append(phone)
        elif type(phone) == 'list':
            self.phones = phone
