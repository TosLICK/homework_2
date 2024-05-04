from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime, timedelta


class Output(ABC):
    @abstractmethod
    def send_to_user(self, message: str) -> None:
        pass


class TerminalOutput(Output):
    def send_to_user(self, message: str) -> None:
        print(message)


class WebOutput(Output):
    def send_to_user(self, message: str) -> None:
        print(f"*'{message}' was sent to user in web*")


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError()
        self.value = value
    
    def is_valid(self, value):
        return True

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


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

    def add_phone(self, number):
        phone = Phone(number)
        for contact in self.phones:
            if phone.value == contact.value:
                return # "Number already exists"
        self.phones.append(phone)
        return phone

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
            
    def remove_phone(self, number):
        phone = self.find_phone(number)
        if not phone:
            raise ValueError()
        self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if not phone:
            raise ValueError()
        self.add_phone(new_number)
        self.remove_phone(old_number)

    def add_birthday(self, birthday_date):
        birthday = Birthday(birthday_date)
        self.birthday = birthday
        return birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, "\
               f"birthday: {str(self.birthday)}"
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name)

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date() # визначаємо поточну дату
        congratulations = []
        result = ''
        for name in self.data:
            congratulation_date = current_date
            birthday_this_year = self.data[name].birthday.value.replace(year=2024)
            # Беремо дати в найближчі 7 днів з сьогоднішнього
            if current_date <= birthday_this_year <= current_date + timedelta(days=6):
                # якщо день народження (д.н.) припадає на суботу, вітання переносимо на ПН
                if birthday_this_year.weekday() == 5:
                    congratulation_date = birthday_this_year.replace(day=birthday_this_year.day + 2)
                # якщо д.н. припадає на неділю, вітання переносимо на ПН
                elif birthday_this_year.weekday() == 6:
                    congratulation_date = birthday_this_year.replace(day=birthday_this_year.day + 1)
                # якщо д.н. припадає на інший день тижня, вітаємо в д.н.
                else:
                    congratulation_date = birthday_this_year
                result += f"{name}: {congratulation_date.strftime("%d.%m.%Y")}\n"
        return result

    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values)


if __name__ == "__main__":
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("07.04.2020")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("08.04.2020")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    # book.delete("Jane")

    john.remove_phone("5555555555")

    for name, record in book.data.items():
        print(record)

    print(book.get_upcoming_birthdays())
