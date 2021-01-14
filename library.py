import requests
import pprint
import pandas as pd
import csv


def get_books(author="Andrzej Sapkowski", kind="książka", title="Pani Jeziora", language="polski"):
    url = "http://data.bn.org.pl/api/bibs.json"
    querystring = {
        "kind": kind,
        "author": author,
        "title": title,
        "language": language
    }
    r = requests.request("GET", url, params=querystring)
    books = r.json()
    books = pd.DataFrame(books['bibs'])
    books = books[['id', 'author', 'title', 'language']]
    return books


def return_book(user_id=0, book_id=0):
    pass


def borrow_book(user_id=0):
    list_of_books = get_books()
    rb = pd.read_csv("RentedBooks.csv")
    print(list_of_books.to_string())
    pprint.pprint(rb)
    i = int(input("Select your book: "))
    append_book("RentedBooks.csv", (user_id, list_of_books[i]['id']))


def append_book(filename, appending):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(appending)
        write_obj.close()


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
