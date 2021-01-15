import requests
import pprint
import pandas as pd
import csv
import numpy as np


def get_books(author=None, kind="książka", title=None, language="polski"):
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


def return_book():
    print("Which one you want to return?")
    rb = pd.read_csv("RentedBooks.csv", dtype={'Book_ID': 'Int64', 'User_ID': 'Int64'})
    for i in range(len(rb['Book_ID'])):
        if rb['User_ID'][i] == user_id:
            print(f'[{i}] {rb["Title"][i]}\n')
    i = int(input())
    book_id = rb['Book_ID'][i]
    pass
    delete_book("RentedBooks.csv", book_id)


def borrow_book():
    author = input("Type author: ")
    title = input("Type title: ")
    list_of_books = get_books(author=author, title=title)
    rb = pd.read_csv("RentedBooks.csv", dtype={'Book_ID': 'Int64'})
    for i in range(len(list_of_books['id'])):
        for na_id in rb['Book_ID']:
            if list_of_books['id'][i] == na_id:
                list_of_books = list_of_books.drop(index=i)
                break
    if list_of_books.empty:
        print("There are no matching books!")
    else:
        print(list_of_books.to_string())
        i = int(input("Select your book: "))
        book_id = int(list_of_books['id'][i])
        book_title = list_of_books['title'][i]
        append_book("RentedBooks.csv", (user_id, book_id, book_title))


def delete_book(filename, book_id):
    lines = list()
    with open(filename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == str(book_id):
                    lines.remove(row)
        readFile.close()
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
        writeFile.close()


# code from internet, not my own
def append_book(filename, appending):
    with open(filename, 'a+', newline='\n') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(appending)
        write_obj.close()


def login():
    global user_id
    user_id = int(input("Enter Your ID: "))


def menu():
    print("You want to \n[1] Return Book \n[2] Borrow Book \n[3] QUIT\n")
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
    login()
    while True:
        menu()
