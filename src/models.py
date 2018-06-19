from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, Numeric, String, Sequence)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = create_engine('sqlite://books.db', echo=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('category_id_seq'), autoincrement=True, primary_key=True),
    name = Column(String(255)),
    url = Column(String(255)),
    books_count = Column(Integer)

    def __repr__(self):
        return "<Category(id='%d', name='%s', url='%s', books='%d')>" % (
            self.id, self.name, self.url, self.books_count)


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
    img_url = Column(String(255)),
    avgrating = Column(Numeric),
    ratings_count = Column(Integer),
    published_year = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    author_id = Column(Integer, ForeignKey('author.id'))

    # relationships
    category = relationship('Category', back_populates='categories')
    author = relationship('Author', back_populates='authors')

    def __repr__(self):
        return "<Book(id='%d', name='%s', url='%s', avgrating='%f', ratings='%d', published='%d')>" % (
            self.id, self.name, self.url, self.avgrating, self.ratings_count, self.published_year)
