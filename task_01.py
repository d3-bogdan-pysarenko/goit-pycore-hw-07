from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    def __init__(self,value):
        self.__value = value.strip() #removing spaces

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        try:
            formatted_string = '%d.%m.%Y'
            self.value = datetime.strptime(value,formatted_string).date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY format for real calendar dates")

class Phone(Field):
   def __init__(self,value):

        if isinstance(value, str) and value.isdigit() and len(value) == 10:
            self.value = value
        else:
            raise ValueError("Phone number must be a 10-digit string")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birhday_string):
        self.birthday = Birthday(birhday_string)

    def add_phone(self,phone_number):
        phone_num_act = Phone(phone_number)
        self.phones.append(phone_num_act)
    
    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

    def edit_phone(self, old_phone, new_phone):

        phone_obj_to_edit = self.find_phone(old_phone)
        if phone_obj_to_edit:
            phone_obj_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone number '{old_phone}' not found for editing within '{self.name}' record")
    
    def remove_phone(self, phone_num):
        phone_obj_to_remove = self.find_phone(phone_num)
        if phone_obj_to_remove:
            self.phones.remove(phone_obj_to_remove)
        else:
            raise ValueError(f"Phone number '{phone_num}' not found in record for {self.name}.")


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, bithday: {self.birthday}"
    

class AddressBook(UserDict):
        def add_record(self, record):
            if isinstance(record, Record):
                self.data[record.name.value] = record
            else:
                raise TypeError("Only Record objects can be added to AddressBook.")
            
        def find(self,name):
            return self.data.get(name)
        
        def delete(self, name):
            if name in self.data:
                del self.data[name]
            else:
                raise KeyError(f"Contact '{name}' not found in the address book.")




# # Checking time ----------------------------------------------------------------------------------------------------------
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# jane= Record("Jane")
# jane.add_phone("7777777777")
# jane.add_phone("1234567800")

# book = AddressBook()
# book.add_record(john_record)
# book.add_record(jane)

# for name, record in book.data.items():
#     print(record)

# john_for_edit = book.find("John")
# print(john_for_edit)

# print('------------------------------------------------------------------')

# print(john_record.find_phone("5555555555"))
# john_record.edit_phone("5555555555", "0000000000")
# # john_record.edit_phone("5555555555", "0000000000")
# print(john_for_edit)
# print(john_record)

# print('------------------------------------------------------------------')

# john_record.remove_phone("0000000000");
# # john_record.remove_phone("0000000000");
# print(john_record)

# print('------------------------------------------------------------------')

# for name, record in book.data.items():
#     print(record)

# # book.delete('Kevin')
# book.delete('Jane')

# for name, record in book.data.items():
#     print(record)






# my_birthday = Birthday('14.10.1991');
# print(my_birthday.__str__())
# wrong_birthday= Birthday('28.02.1991')
# print(wrong_birthday.__str__())

john_record = Record("John Bay")
john_record.add_phone("1234567890");
john_record.add_phone("5656567788");
john_record.add_birthday('14.10.1991')
print(john_record.__str__())
john_record.add_birthday('1.1.2002')
print(john_record.__str__())