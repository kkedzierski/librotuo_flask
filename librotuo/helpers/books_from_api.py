import json
from urllib.request import urlopen
from librotuo.models import Book

url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'


def length_of_books_in_api(url):
    response = urlopen(url)

    books_string = response.read().decode('utf-8')
    books_json = json.loads(books_string)
    books_json_items = books_json['items']

    all_books = [books['volumeInfo'] for books in books_json_items]
    return len([book['title'] for book in all_books])


def create_new_book_from_api(url, new_book, new_book_number):
    response = urlopen(url)

    books_string = response.read().decode('utf-8')
    books_json = json.loads(books_string)
    books_json_items = books_json['items']

    all_books = [books['volumeInfo'] for books in books_json_items]
    all_books_len = length_of_books_in_api(url)
    i = 0
    while i <= all_books_len:
        for book in all_books:
            i = i+1
            new_book.title = book['title']
            new_book.published_date = book['publishedDate']
            new_book.authors = ''.join([author for author in book['authors']])
            new_book.ISBN_number = ''.join([book['identifier']
                                            for book in book['industryIdentifiers']
                                            ])
            try:
                new_book.page_number = book['pageCount']
            except KeyError:
                new_book.page_number = None
            try:
                new_book.cover_url = book['imageLinks']['thumbnail']
            except KeyError:
                new_book.cover_url = None
            new_book.publication_language = book['language']
            if i == new_book_number:
                return new_book


def create_books_from_api(url, book_obj_num=length_of_books_in_api(url)):
    book_obj_list = [Book() for i in range(book_obj_num)]
    for book_num in range(book_obj_num):
        create_new_book_from_api(url, book_obj_list[book_num], book_num)
    return book_obj_list


# book_obj_list = create_books_from_api(url)
# for book in book_obj_list:
#     print(f"""title: {book.title}, published_date: {book.published_date},"
#            "Authors: {book.authors}, ISBN_number: {book.ISBN_number},"
#            "page_number:{book.page_number}, cover_url: {book.cover_url},"
#            "publication_language = {book.publication_language}""")
