from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, Numeric, String, Sequence)

Base = declarative_base()
engine = create_engine('sqlite://books.db', echo=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('category_id_seq'), autoincrement=True, primary_key=True),
    name = Column(String(255)),
    url = Column(String(255)),
    page_count = Column(Integer),
    books_count = Column(Integer)

    def __repr__(self):
        return "<Category(id='%d', name='%s', url='%s', pages='%d', books='%d')>" % (
            self.id, self.name, self.url, self.page_count, self.books_count)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, Sequence('author_id_seq'), autoincrement=True, primary_key=True),
    name = Column(String(255)),
    url = Column(String(255)),

    def __repr__(self):
        return "<Author(id='%d', name='%s', url='%s')>" % (
            self.id, self.name, self.url)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, Sequence('author_id_seq'), autoincrement=True, primary_key=True),
    name = Column(String(255)),
    url = Column(String(255)),
    avgrating = Column(Numeric),
    ratings_count = Column(Integer),
    published_year = Column(Integer)

    def __repr__(self):
        return "<Book(id='%d', name='%s', url='%s', avgrating='%f', ratings='%d', published='%d')>" % (
            self.id, self.name, self.url, self.avgrating, self.ratings_count, self.published_year)
