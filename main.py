import pickle


from address_book import address_book
from phone_bot import PhoneBot


def main():
    def save_data(book, filename="storage/addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

    def load_data(filename="storage/addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return address_book()

    book = load_data()
    phone_bot = PhoneBot(book)

    try:
        phone_bot.start_bot()
    finally:
        save_data(book)


if __name__ == "__main__":
    print("Hello")
    main()
