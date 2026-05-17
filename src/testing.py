from assistant_bot_classes import AddressBook, Record
from assistant_bot_serialization import load_data, save_data
from assistant_bot import (
    add_contact,
    add_birthday,
    change_contact,
    show_phone,
    show_all,
    show_birthday,
    birthdays,
)


def testing_address_book():
    print('\n[*] Some tests for AddressBook:')

    try:
        # Створення адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record('John')
        john_record.add_phone('1234567890')
        john_record.add_phone('5555555555')

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record('Jane')
        jane_record.add_phone('9876543210')
        book.add_record(jane_record)

        # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(record)

        # Знаходження та редагування телефону для John
        john = book.find('John')
        john.edit_phone('1234567890', '1112223333')
        # john.edit_phone('1234567890', '11122RT333')

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону в записі John
        found_phone = john.find_phone('5555555555')
        print(f'{john.name}: {found_phone}')  # Виведення: 5555555555

        # Видалення запису Jane
        book.delete('Jane')
    # Виведення помилок
    except Exception as e:
        print(f'! Виникла помилка. Перевірте вхідні дані: {e}')


def positive_test_for_assistance_bot():
    print('\n[*] Some positive print tests for assistance bot:')
    book = load_data()
    print(add_contact(['John', '1234567890'], book))
    print(add_contact(['John', '5555555555'], book))
    print(add_contact(['Jane', '9876543210'], book))
    print(change_contact(['Jane', '9876543210','0000003210'], book))
    print(show_phone(['John'], book))
    print(show_all(book))
    print(add_birthday(['John', '08.05.2005'], book))
    print(show_birthday(['John'], book))
    print(birthdays(book))
    save_data(book)


def negative_test_for_assistance_bot():
    print('\n[*] Some negative print tests for assistance bot:')
    book = AddressBook()
    print(add_contact(['John'], book))
    print(add_contact(['John', 'TTTT', 'PPPPP'], book))
    print(change_contact(['TOM', '9876543210', '0000003210'], book))
    print(show_phone(['JACK'], book))
    print(add_birthday(['John', '128.05.2005'], book))
    add_contact(['Tom', '9876543210'], book)
    print(add_birthday(['Tom', '128.05.2005'], book))
    print(show_birthday(['Tom'], book))


if __name__ == '__main__':
    # testing_address_book()
    positive_test_for_assistance_bot()
    # negative_test_for_assistance_bot()
