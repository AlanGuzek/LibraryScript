import requests


def get_books(url):
    r = requests.get(url)
    return r.json()


def return_book(book="Wiedźmin"):
    pass


def borrow_book(book="Wiedźmin"):
    pass


def menu():
    print("You want to \n[1] Return Book \n[2] Borrow Book? \n[3] QUIT")
    option = int(input("\b"))
    if option == 1:
        return_book()
    elif option == 2:
        borrow_book()
    elif option == 3:
        quit()
    else:
        print("Wrong input!")
        menu()


if __name__ == '__main__':
    while True:
        menu()
