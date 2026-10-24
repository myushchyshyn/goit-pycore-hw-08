from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Ім'я контакту. Обов'язкове поле."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Name is required.")
        super().__init__(value)


class Phone(Field):
    """Номер телефону. Має містити рівно 10 цифр."""

    def __init__(self, value):
        if not (isinstance(value, str) and len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """День народження у форматі DD.MM.YYYY."""

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Запис контакту: ім'я, телефони та (необов'язково) день народження."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        new = Phone(new_phone)
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = new
                return
        raise ValueError(f"Phone {old_phone} not found.")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        if self.birthday is not None:
            raise ValueError("Birthday already set.")
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"


class AddressBook(UserDict):
    """Адресна книга: записи за іменем, пошук і видалення, список привітань."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    def get_upcoming_birthdays(self, today=None) -> list[dict]:
        """Контакти, яких треба привітати протягом наступних 7 днів (включно з сьогодні).

        Дні народження на суботу або неділю переносяться на понеділок.
        """
        today = today or datetime.today().date()
        result = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday = record.birthday.value.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            if not 0 <= (birthday - today).days <= 7:
                continue
            if birthday.weekday() == 5:
                birthday += timedelta(days=2)
            elif birthday.weekday() == 6:
                birthday += timedelta(days=1)
            result.append({"name": record.name.value, "congratulation_date": birthday.strftime("%Y.%m.%d")})
        return result
