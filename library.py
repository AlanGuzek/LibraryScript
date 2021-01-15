import requests
import pprint
import pandas as pd
import csv
import codecs
import numpy as np


def get_books(author="", kind="książka", title="", language="polski"):
    url = "http://data.bn.org.pl/api/bibs.json"
    querystring = {
        "kind": kind,
        "author": author,
        "title": title,
        "language": language
    }
    if author == "":
        querystring.pop("author")
    if title == "":
        querystring.pop("title")
    r = requests.request("GET", url, params=querystring)
    books = r.json()
    books = pd.DataFrame(books['bibs'])
    books = books[['id', 'author', 'title', 'language']]
    return books


def return_book():
    rb = pd.read_csv("RentedBooks.csv", dtype={'Book_ID': 'Int64', 'User_ID': 'Int64'}, encoding='utf-8')
    empty = True
    for i in range(len(rb['Book_ID'])):
        if rb['User_ID'][i] == user_id:
            print(f'[{i}] {rb["Title"][i]}\n')
            empty = False
    if not empty:
        try:
            i = int(input("Which one you want to return: "))
            book_id = rb['Book_ID'][i]
            delete_book("RentedBooks.csv", book_id)
        except:
            pass
    else:
        print("You have nothing to return")


def borrow_book():
    author = input("Type author: ")
    title = input("Type title: ")
    list_of_books = get_books(author=author, title=title)
    rb = pd.read_csv("RentedBooks.csv", dtype={'Book_ID': 'Int64'}, encoding='utf-8')
    for i in range(len(list_of_books['id'])):
        for na_id in rb['Book_ID'][1:]:
            na_id = int(na_id)
            if list_of_books['id'][i] == na_id:
                list_of_books = list_of_books.drop(index=i)
                break
    if list_of_books.empty:
        print("There are no matching books!")
    else:
        print(list_of_books.to_string())
        try:
            i = int(input("Select your book: "))
            book_id = int(list_of_books['id'][i])
            book_title = list_of_books['title'][i]
            append_book("RentedBooks.csv", (user_id, book_id, book_title))
        except:
            borrow_book()


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
    with codecs.open(filename, 'a+', encoding='utf-8') as write_obj:
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
