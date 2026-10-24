import pickle

from address_book import AddressBook

DEFAULT_FILE = "addressbook.pkl"


def save_data(book: AddressBook, filename: str = DEFAULT_FILE) -> None:
    """Зберігає адресну книгу у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = DEFAULT_FILE) -> AddressBook:
    """Відновлює адресну книгу з файлу. Якщо файлу немає — повертає нову книгу."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
