import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return bool(re.fullmatch(r'\d{10}', value))

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone_to_remove = next((p for p in self.phones if p.value == phone), None)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = next((p for p in self.phones if p.value == old_phone), None)
        if old_phone_obj:
            if not Phone.validate(new_phone):
                raise ValueError("Invalid new phone number")
            old_phone_obj.value = new_phone
        else:
            raise ValueError("Old phone number not found")

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of Record")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found")

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                delta_days = (record.birthday.value - today).days
                if 0 <= delta_days <= 6:
                    greeting_date = record.birthday.value
                    # Adjust if birthday falls on a weekend
                    while greeting_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                        greeting_date += timedelta(days=1)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": greeting_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays
def save(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

@staticmethod
def load(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
def __str__(self):
    return '\n'.join(str(record) for record in self.data.values())

# Function decorators
def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones for {name}: {'; '.join(p.value for p in record.phones)}"
    return "Contact not found."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Contact or birthday not found."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return '\n'.join(f"{entry['name']}: {entry['birthday']}" for entry in upcoming)
    return "No upcoming birthdays."

def parse_input(user_input):
    return user_input.strip().split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
