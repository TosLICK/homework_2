import pickle
from my_classes import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return no_contact()

    return inner


def hello(args, book: AddressBook):
    return "How can I help you?"


def help(args, book: AddressBook):
    return usage()


@input_error
def parse_input(user_input):  # парсимо ввод користувача
    cmd, *args = user_input.split()  # розбиваємо ввод на команду (перший аргумент) і інші аргументи
    cmd = cmd.strip().lower()  # команду приводимо до нижнього регістру
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def delete_contact(args, book: AddressBook):
    name, *_ = args
    book.delete(name)
    return "Contact deleted"


# @input_error
# змінюємо номер телефону, якщо контакт присутній у словнику
def change_contact(args, book: AddressBook):
    name, old_number, new_number, *_ = args
    record = book.find(name)
    if record is None:
        return no_contact()
    record.edit_phone(old_number, new_number)
    return "Number changed"


@input_error
def show_phone(args, book: AddressBook): # виводимо номер телефону за заданим ім'ям контакту
    name, *_ = args
    return f"{book[name].phones}"


@input_error
def show_all(args, book: AddressBook): # виводимо усі контакти з номерами телефонів
    if not book:
        return "There are no contacts." # якщо контактів немає, виводимо відповідне повідомлення
    string = ''
    for _, record in book.items():
        string += f"{record}\n"
    return string


# @input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    if book[name].birthday:
        book[name].add_birthday(birthday)
        return "Birthday updated"
    else:
        book[name].add_birthday(birthday)
        return "Birthday added"


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    if not book[name].birthday:
        return "Birthday absent"
    return f"{book[name].birthday}"


@input_error
def birthdays(args, book: AddressBook):
    if book.get_upcoming_birthdays() == '':
        return "There are no upcoming birthdays."
    return book.get_upcoming_birthdays()


def usage():
    return "Usage: 'hello'\n'close'\n'exit'\n'all'\n'add name phone_number'\n"\
            "'phone name'\n'delete name'\n'add-birthday name birthday(dd.mm.yyyy)'\n"\
            "'show-birthday name'\n'birthdays'\n'help'"


def no_contact():
    return "Contact does not exist."


functions = {
    "hello": hello,
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "delete": delete_contact,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "help": help,
}


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


@input_error
def main():
    # book = AddressBook()
    book = load_data()
    print("Welcome to the assistant bot!")

    user_type_output = input("Choose interface: 1 = terminal, 2 = web: ")
    if user_type_output == "1":
        output = TerminalOutput()
    elif user_type_output == "2":
        output = WebOutput()
    else:
        print("Incorrect data")
        output = None
        main()

    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                output.send_to_user("Good bye!")
                break
            elif command in functions:
                output.send_to_user(functions[command](args, book))
            else:
                output.send_to_user(usage())
        except ValueError:
            output.send_to_user(usage())
            
    save_data(book)


if __name__ == "__main__":
    main()
