from collections.abc import Callable
from assistant_bot_classes import AddressBook, Record
from assistant_bot_serialization import load_data, save_data


def input_error(func: Callable) -> Callable:
    def inner(*args: list, **kwargs: dict) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact not exist, choose another one'
        except TypeError:
            return 'Be sure you provide correct amount of arguments'
        except ValueError as e:
            if 'values to unpack' in str(e):
                return (
                    'Please provide correct amount of arguments. '
                    'Try help command.'
                )
            return e
        except IndexError:
            return 'Please give me name you looking for'
        except Exception as e:
            return f'Something went wrong, please try again: {e}'
    return inner


@input_error
def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    name, birthday = args[:2]
    record: Record = book.find(name)
    if record is None:
        return f'Contact "{name}" not found.'
    record.add_birthday(birthday)
    return 'Contact updated.'


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    name = args[0]
    record: Record = book.find(name)
    if record is None:
        return 'Contact not found.'
    return f'Birthday of "{record.name}": {record.birthday}'


@input_error
def birthdays(book: AddressBook) -> str:
    return book.get_upcoming_birthdays()


@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone = args[:2]
    record = book.find(name)
    is_new_record = record is None
    message = 'added' if is_new_record else 'updated'
    record = Record(name) if is_new_record else record
    record.add_phone(phone)
    if is_new_record:
        book.add_record(record)
    return f'Contact {message}.'


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    name, old_phone, new_phone = args[:3]
    record: Record = book.find(name)
    if record is None:
        return f'Contact "{name}" not found. If you want to add a new contact, use the "add" command.'
    record.edit_phone(old_phone, new_phone)
    return 'Contact updated.'


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    name = args[0]
    record: Record = book.find(name)
    if record is None:
        return f'Contact "{name}" not found.'
    return ', '.join(str(p) for p in record.phones)


@input_error
def show_all(book: AddressBook) -> str:
    return '\n'.join([f'{record}' for record in book.values()])


def help():
    commands = [
        'help','hello',
        'add {name} {phone}',
        'change {name} {old_phone} {new_phone}',
        'phone {name}',
        'show {name}', # alias for 'phone'
        'add-birthday {name} {birthday}',
        'show-birthday {name}',
        'birthdays',
        'all', 'close', 'exit',
    ]
    return 'Available commands:\n  ' + '\n  '.join(commands)


def main():
    book = load_data()

    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        match command:
            case 'close' | 'exit':
                save_data(book)
                print('Good bye!')
                break
            case 'hello':
                print('How can I help you?')
            case 'add':
                print(add_contact(args, book))
            case 'change':
                print(change_contact(args, book))
            case 'show' | 'phone':
                print(show_phone(args, book))
            case 'all':
                print(show_all(book))
            case 'add-birthday':
                print(add_birthday(args, book))
            case 'show-birthday':
                print(show_birthday(args, book))
            case 'birthdays':
                print(birthdays(book))
            case 'help':
                print(help())
            case _:
                print(
                f'Іnvalid command.'
                'Type "help" to see the list of available commands.'
            )


if __name__ == '__main__':
    main()
