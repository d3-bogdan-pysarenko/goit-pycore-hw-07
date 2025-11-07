from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    def __init__(self,value):
        self.__value = value.strip()

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

    def show_birthday(self):
        return self.birthday

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
        
        def get_upcoming_birthdays(self):
            today = date.today()
            upcoming_birthdays = []
            try:
                for name, record in self.data.items():
                    if record.birthday is not None: # if not populated
                        # Replace year with the current year
                        birthday_this_year = record.birthday.value.replace(year=today.year)

                        # If birthday already passed this year, use next year
                        if birthday_this_year < today:
                            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                        # If birthday is on weekend, move to next Monday
                        if birthday_this_year.weekday() == 5:  # Saturday
                            birthday_this_year += timedelta(days=2)
                        elif birthday_this_year.weekday() == 6:  # Sunday
                            birthday_this_year += timedelta(days=1)
                        
                        # Check if the (possibly shifted) date is within the next 7 days
                        if 0 <= (birthday_this_year - today).days <= 7:
                            upcoming_birthdays.append({
                                "name": name,
                                "original_birthday": record.birthday.value.strftime("%d.%m.%Y"),
                                "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                            })
                    
                if len(upcoming_birthdays) == 0:
                    print('There is no one to congratulate in next 7 days')
                else:
                    sorted_upcoming_birthdays = sorted(upcoming_birthdays, key=lambda x: x['congratulation_date'])
                    print("Congratulations list for this week:\n",sorted_upcoming_birthdays)
                    return upcoming_birthdays   
            except ValueError:
                raise ValueError(f"Wrong incoming data, please check your adressbook")




# Checking time ----------------------------------------------------------------------------------------------------------
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

jane= Record("Jane")
jane.add_phone("7777777777")
jane.add_phone("1234567800")

book = AddressBook()
book.add_record(john_record)
book.add_record(jane)

for name, record in book.data.items():
    print(record)

john_for_edit = book.find("John")
print(john_for_edit)

print('------------------------------------------------------------------')

print(john_record.find_phone("5555555555"))
john_record.edit_phone("5555555555", "0000000000")
# john_record.edit_phone("5555555555", "0000000000")
print(john_for_edit)
print(john_record)

print('------------------------------------------------------------------')

john_record.remove_phone("0000000000");
# john_record.remove_phone("0000000000");
print(john_record)

print('------------------------------------------------------------------')

for name, record in book.data.items():
    print(record)

# book.delete('Kevin')
book.delete('Jane')

for name, record in book.data.items():
    print(record)



print('------------------------------------------------------------------')
kevin= Record("Kevin Malone")
jane= Record("Jane Konnor")
book.add_record(jane)
john_record.add_phone("1234567890");
jane.add_phone("5656567788");
john_record.add_birthday('8.11.1991')
# jane.add_birthday('7.11.2000')
kevin.add_birthday('6.11.2002')
book.add_record(kevin)
for name, record in book.data.items():
    print(record)
book.get_upcoming_birthdays()