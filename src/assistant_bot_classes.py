from collections import UserDict
from datetime import date, datetime, timedelta
from functools import wraps


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value:
            raise ValueError('Name must be a non-empty string.')
        super().__init__(value)
        self.value = value
    
    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must be 10 digits.')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            value = date.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone: str):
        finded_phones = [p for p in self.phones if p.value == phone]
        return finded_phones[0].value if finded_phones else None

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        return f'Contact "{self.name.value}", phones: {phones}'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict]:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
            next_birthday = record.birthday.value.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            
            days_difference = next_birthday.toordinal() - today.toordinal()
            birthday_week_day = next_birthday.isoweekday()

            if days_difference < 7:
                if birthday_week_day < 6:
                    congratulation_date = next_birthday
                else:
                    days_to_next_monday = 7 - birthday_week_day + 1
                    congratulation_date = next_birthday + timedelta(days=days_to_next_monday)

                upcoming_birthdays.append({
                    'name': record.name.value,
                    'congratulation_date': congratulation_date.strftime('%d.%m.%Y')
                })

        return upcoming_birthdays
