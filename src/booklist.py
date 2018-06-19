import argparse
import requests
from bs4 import BeautifulSoup as bsoup
from fake_useragent import UserAgent
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import locale
# import models

# Set default locale - required while parsing string to float (later)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# =================================================================================
# Database setup
# =================================================================================

# Base class for the rest of the models
Base = declarative_base()
Session = sessionmaker()


def setup_database(reset=False):
    """
    Performs initial setup of the database
    :param reset: if true, deletes the records and starts from scratch
    :return: nothing
    """
    engine = create_engine('sqlite://book.db', echo=True)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)


# =================================================================================
# Download URLs
# =================================================================================

@lru_cache(maxsize=128)
def get_request_headers():
    headers = {
        'User-Agent': str(UserAgent().chrome)
    }
    return headers


def download_url_html(url):
    headers = get_request_headers()
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text
    return html


def parse_html_and_add_record(html):
    s = bsoup(html, 'lxml')
    container = s.find('div', class_='leftContainer')
    category_books_count = locale.atoi(container.find('span', class_='smallText').text.strip().rstrip(')').split()[-1])
    books_list = container.find_all('div', class_='elementList')
    f = open('out/books.csv', 'a')
    for book in books_list:
        left = book.find('div', class_='left')
        book_img_url = left.find('img')['src']
        book_url = 'www.goodreads.com/{}'.format(left.find('a', class_='bookTitle')['href'])
        book_title = left.find('a', class_='bookTitle').text
        book_title = " ".join(book_title.split()).replace(',','_')
        author_name = left.find('a', class_='authorName').span.text
        author_url = left.find('a', class_='authorName')['href']
        grey_text = left.find('span', class_='greyText smallText').text.strip().split('\n')
        book_avg_rating = locale.atof(grey_text[0].rstrip('—').strip().split()[2])
        book_ratings_count = locale.atoi(grey_text[1].strip().split()[0])
        book_published_year = locale.atoi(grey_text[2].strip().split()[1])
        category_name = s.find('div', class_='breadcrumbs').find_all('a')[-1]['href'].split('/')[-1]

        # add the record to the database
        book_details = "{},{},{},{},{},{},{}\n".format(book_title, author_name, book_avg_rating,
                                                  book_ratings_count, book_published_year, category_name, book_url)
        f.write(book_details)
    f.close()


def parse_args():
    """
    Parse command line parameters and return them as a list.
    """
    parser = argparse.ArgumentParser(
        prog="Books List",
        description="Scan goodreads to generate a list of books for various genres."
    )

    parser.add_argument('-l', '--list', action='store_true',
                        default=False, help='list all genres')

    args = parser.parse_args()
    return args


def main():
    """
    Entry point of the program.
    """
    args = parse_args()
    with open('src/category.urls', 'r') as f:
        category_data = f.read().split('\n')
    for category in category_data:
        data = category.split(',')
        print ("Downloading books in the '{}' category ...".format(data[0]))
        html = download_url_html(data[1])
        parse_html_and_add_record(html)
        print ("Done.")


# =================================================================================
# Trigger main if this is not an import
# =================================================================================
if __name__ == '__main__':
    main()
