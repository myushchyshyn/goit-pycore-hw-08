import os
import tempfile
from address_book import AddressBook, Record
from storage import save_data, load_data
from bot import add_contact, add_birthday, show_phone

path = os.path.join(tempfile.mkdtemp(), "addressbook.pkl")

assert isinstance(load_data(path), AddressBook) and len(load_data(path)) == 0

book = AddressBook()
assert add_contact(["Jime", "0501234356"], book) == "Contact added."
assert add_birthday(["Jime", "25.10.1990"], book) == "Birthday added."
save_data(book, path)

restored = load_data(path)
assert show_phone(["Jime"], restored) == "0501234356"
assert str(restored.find("Jime").birthday) == "25.10.1990"
assert add_contact(["Bob", "1234567890"], restored) == "Contact added."
save_data(restored, path)
assert len(load_data(path)) == 2

print("ALL HW8 TESTS PASSED")
