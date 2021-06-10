################################################################################
#         adress book classes                                                  #
################################################################################

from collections import UserDict
from datetime import datetime
from datetime import date
import math
import re
import json

class AddressBook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 40

    def add_record(self,record):
        self.data [record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        if  self.current_page < int(math.ceil(len(self.data)/self.records_on_the_page)) :
            keys = list(self.data.keys())
            r_list = []  
            for i in range(self.current_page*self.records_on_the_page ,min([(self.current_page+1)*self.records_on_the_page,len(self.data)])):
                a_dict = {}    
                a_dict["Name"] = keys[i]
                a_dict["Phones"]= [x.value for x in self.data[keys[i]].phones]
                if type(self.data[keys[i]].birthday)!=type(""):
                    a_dict["Birthday"]= str(self.data[keys[i]].birthday.value)
                r_list.append(a_dict)
            self.current_page+=1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
            
    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict ={self.name:{}}
            store_records_on_the_page = self.records_on_the_page
            self.records_on_the_page = 1
            id =1
            for page in self:
                dump_dict[self.name]["RecID"+str(id)]= page[0]
                id+=1
            json.dump(dump_dict, write_file)
            self.records_on_the_page = store_records_on_the_page
            print("Data exported to the file")

    def load(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            self.name= list(data.keys())[0]
            for name in list(data[self.name].keys()):
                record = data[self.name][name]
                rec = Record(record["Name"])
                if "Phones" in record.keys():
                    for phone in record["Phones"]:
                        rec.add_phone(Phone(phone))
                if "Birthday" in record.keys():
                    lst = record["Birthday"].split("-")
                    birthday = Birthday(lst[2]+"."+lst[1]+"."+lst[0])
                    rec.add_birthday(birthday)
                self.add_record(rec)
            print ("Data have been loaded from file")        

    def find(self, request):
        result_lst = []
        for name in self.data.keys():
            search_list = [name]
            search_list.extend([phone.value for  phone in self.data[name].phones])
            for field in search_list:
                if request[0]=='+':
                   request = request[1:] 
                if re.search(request.upper(),field.upper())!=None:
                    result_lst.append(name)
                    break
        return result_lst 
               
class Record:
    def __init__(self, name):
        self.phones = list()
        self.birthday = ""
        self.name = Name(name)
      
    def add_phone(self,phone):
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)

    def del_phone(self,phone):
        self.phones = list(filter(lambda x: x.value!=phone, self.phones))

    def edit_phone(self,phone, new_phone):
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(Phone(new_phone))
       
         
    def add_birthday(self,birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        date1 = datetime(datetime.now().timetuple().tm_yday, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
        delta = date1.timetuple().tm_yday - datetime.now().timetuple().tm_yday
        if delta > 0:
            return str(delta)
        else:
            date1 = datetime(datetime.now().timetuple().tm_year+1, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
            date2 = datetime(datetime.now().timetuple().tm_year, datetime.now().timetuple().tm_mon, datetime.now().timetuple().tm_mday)
            delta = date1 - date2
            return str(delta.days)
    
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(f"{self.__dict__}")

    @property
    def value(self):
       return self.__value    

    @value.setter
    def value(self, value_):
       if len(value_) > 0:
          self.__value = value_


class Name(Field):
    def __init__(self, name):
        self.__value = name

    @property
    def value(self):
       return self.__value    

    @value.setter
    def set_value(self, value):
       if len(value) > 0:
          self.__value = value    

class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
       return self.__value


    @value.setter
    def value(self, phone):
       if re.search('\+\d{12}', phone) != None:
          self.__value = phone
       else:
          raise  ValueError("Phone should be in the next format: '+XXXXXXXXXXXX' (12 digits)")
       
class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, birthday):
       if re.search('\d{2}\.\d{2}\.\d{4}', birthday) != None:
          self.__value = datetime.strptime(birthday, '%d.%m.%Y').date()
       else:
          return False 


################################################################################
#         CLI BOT section                                                      #
################################################################################

exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
   def inner(phone):
      result=func(phone)
      if len(result) == 12:
          result='+'+result
      else: result='+38'+result    
      return result
   return inner
            

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

def hello_(data):
    return "How can I help You?"

def add_(data):
    done = False
    while not done:
        print("Type 'C' if you would like to add a new contact or 'P' to add a phone number to existing one")
        choose = input().lower()
        if choose == 'exit':
            print ("Operation cancelled")
            done = True
        elif choose == 'c':
            print("Input the name of new contact")
            name = input()
            phone = choose_phone()
            if phone == 'exit':
                print ("Operation cancelled")
                return "Please choose command"
            r = Record(name)
            p = Phone(phone)
            r.add_phone(p)
            a.add_record(r)
            print ("Contact successfully added to phone_book")
            done = True
        elif choose == 'p':
            name = choose_record()
            if name == 'exit': 
                print ("Operation cancelled")
                return "Please choose command"
            while True:
                phone = choose_phone()
                if phone == 'exit':
                    print ("Operation cancelled")
                    return "Please choose command"
                if phone not in [ph.value for ph in a.data[name].phones]:
                    if a.find(phone)!=[]:
                        print("This number already belonged to contact "+a.find(phone)[0]+", please try again or type 'Exit' to come back to main menu")
                    else:
                        a.data[name].add_phone(Phone(phone))
                        print ("Phone number succesfully added")
                        return "Please choose command"
                else:
                    print("This number already belonged to contact "+name+", please try again or type 'Exit' to come back to main menu")
    return "Please choose command" 

def change_(data):
    name = choose_record()
    if name == 'exit':
        print("Operation canselled")
        return "Please choose command"
    while True:
        print("Type 'N' to edit the name or 'P' to edit a phone number")
        choose = input().lower()
        if choose == 'p':
            while True:
                print("I need the old number to change")
                phone = choose_phone()
                if phone == 'exit':
                    print("Operation canselled")
                    return  "Please choose command" 
                elif phone in [ph.value for ph in a.data[name].phones]:
                    print("I need the new number to save")
                    phone_new = choose_phone()
                    a.data[name].edit_phone(phone, phone_new)
                    print ("Phone changed succesfully")
                    return  "Please choose command" 
                else:
                    print("This number doesn't belong to the "+name)
                    print("List of phone numbers belonged to the "+name)
                    for ph in a.data[name].phones:
                        print(ph.value)
                    print("Please input the correct number or type 'Exit' to come back to main menu")
        elif choose =='n':
            print("Please give me a new name for a contact: "+name)
            name_new = input()
            a.data[name_new] = a.data[name]
            a.data.pop(name)
            print("The name of a contact succesfully changed")
            return "Please choose command" 
        elif choose =='exit':
            print("Operation canselled")
            break
    return  "Please choose command" 

  

def find_(data):
    res_lst =[]
    print("Please input info to search. It could be the name, phone number or even a part of them")
    search_str = input().rstrip()
    search_str = (
        search_str.strip()
            .replace("+","\+")
            .replace("*", "\*")
            .replace("{", "\{")
            .replace("}", "\}")
            .replace("[", "\[")
            .replace("]", "\]")
            .replace("?", "\?")
            .replace("$", "\$")
            .replace("'\'", "\\")
        
    )

    res_lst = a.find(search_str)
    if res_lst == []:
        print("Couldn't find records in the phone book")
    else:
        print("Found next contacts:")
        for contact in res_lst:
            print(contact)
            for ph in a.data[contact].phones:
                print("       "+ph.value)
    return "Please choose command"

def show_all(data):
    adress_book = a    
    for page in adress_book:
        for record in page:
            print("Name:", record["Name"])
            print("      Phone list:")
            for phone in record["Phones"]:
                print("      "+phone)
            if "Birthday" in record.keys():
                print ("      Birthday: ", record["Birthday"])
        input("Press enter to continue")
    return "Please choose command"

def help_(command):
    print("List of available commands: ")
    for key in exec_command.keys():
        print (exec_command[key][1])
    print ("exit:      Exit program ('good by', 'close' also works)")    
    return "Please choose command"

def birthday_(data):
    name = choose_record()
    if name == 'exit':
        print("Operation canselled")
        return "Please choose command"
    birthday = choose_date()
    if birthday == 'exit':
        print("Operation canselled")
    else:
        b=Birthday(birthday)
        a.data[name].add_birthday(b)
        print("Birthday setted successfully")
    return "Please choose command"

def choose_record():
    print("Please enter the name of a contact")
    while True:
        name = input()
        if name in a.data.keys():
            break
        elif name.lower() == 'exit':
            break
        else:
            print("Couldn`t find exactly this name in adress book.")
            print("Here are the list of the contacts with similar spelling:")
            for c in a.find(name):
                print("     "+c)
            print("Please try to choose the name again or type 'Exit' to come back to main menu")    
    return name

def choose_phone():
    print("Please enter the phone number")
    while True:
        phone = input().lower()
        if phone == 'exit':
            break
        is_correct_format= re.search("\+?[\ \d\-\(\)]+$",phone)
        phone= sanitize_phone_number(phone)
        if is_correct_format!=None and len(phone) == 13: 
            break
        else:
            print("Phone number is incorrect format, please try again or type 'Exit' to come back to main menu")
    return phone

def choose_date():
    print("Please enter the date of birthday in format dd.mm.yyyy")
    while True:
        birthday = input().lower()
        is_correct_format= re.search("\d{2}[\/\.\:]\d{2}[\/\.\:]\d{4}",birthday)
        if is_correct_format!=None:
            birthday = birthday.replace("/",".")
            birthday = birthday.replace(":",".")
            b_array = birthday.split(".")
            try:
                datetime.strptime(birthday, '%d.%m.%Y').date()
            except ValueError:
                print("You gave me incorrect date, be carefull nex time")
            else:
                break
        elif birthday == 'exit':
            break
        print("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
    return birthday


def delete_(command):
    choose = ""
    while True:
        print("Type 'C' if you would like to delete a contact or 'P' to delete a phone number")
        choose= input().lower()
        if choose in ['c','p', 'exit']:
           break
        else:
            print("Incorrect input, please choose 'C' or 'P', or 'Exit' to terminate delete operation")
    if choose == 'p':    
        name = choose_record()
        if name == 'exit':
            print("Operation canselled")
            return "Please choose command"
        while True:
            phone = choose_phone()
            if phone == 'exit':
                print("Operation canselled")
                break
            elif phone in [ph.value for ph in a.data[name].phones]:
                a.data[name].del_phone(phone)
                print ("Phone deleted succesfully")
                break
            else:
                print("This number doesn't belong to the "+name)
                print("List of phone numbers belonged to the "+name)
                for ph in a.data[name].phones:
                    print(ph.value)
                print("Please input the correct number or type 'Exit' to come back to main menu")
    elif choose == 'c':
        name = choose_record()
        if name == 'exit':
            print("Operation canselled")
            return "Please choose command"
        while True:
            print ("Find a contact "+name+", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y': 
                a.delete(name)
                print("Contact "+name+" deleted")
                return "Please choose command"
            elif choose_d == 'n':
                print("Operation canselled")
                return "Please choose command"
            else:
                printf("Make a correct choise, please")
    else:
        print("Operation canselled")
        return "Please choose command"
    return  "Please choose command"         
       
    
def save_(data):
    a.dump("Work telephones.json")
    return "Please choose command"
    
exec_command = { 
    "hello": [hello_,      "hello:     Greetings", 0], #
    "add": [add_,          "add:       Add a new contact or a new phone for existing contact", 2], #
    "edit": [change_,      "edit:      Edit the name of contact or phone number for contact", 2], #
    "find": [find_,        "find:      Find the records by phone or name", 1], #
    "show all": [show_all, "show all:  Print all the records of adress book, page by page", 0], #
    "help": [help_,        "help:      Print a list of the available commands",0], 
    "birthday": [birthday_,"birthday:  Add birthday to existed contact",1],#
    "delete": [delete_,    "delete:    Delete contact or phone for specified contact", 2], #
    "save": [save_,        "save:      Save the current state of address book to disk", 0] #
                           
             }


def handler(command, data):
    return exec_command[command][0](data.replace(command+" ",""))
    

def parser(input_str):
    for token in exec_command.keys():
        if token in input_str:
            return handler(token, input_str.replace(token+" ", ""))
    return "Input error, please type 'help' for commands description"
            
def listener():
    command = ""
    communication_str = "CLI phone book bot looking for command"
    while (command) not in exit_command:
        print(communication_str+": ")
        command = input().lower()
        communication_str = parser(command)


a = AddressBook("Work telephones")
try:
    a.load("Work telephones.json")
except:
    print("Couldn't find file, starting with empty adress book")
listener() 
a.dump("Work telephones.json")
