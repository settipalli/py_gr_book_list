from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData)

engine = create_engine('sqlite://:memory:', echo=True)
meta = MetaData()

category = Table('category', meta,
                 Column('id', Integer, autoincrement=True, primary_key=True),
                 Column('name', String),
                 Column('url', String),
                 Column('page_count', Integer),
                 Column('books_count', Integer)
                 )

author = Table('author', meta,
               Column('id', Integer, autoincrement=True, primary_key=True),
               Column('name', String),
               Column('url', String),
               )

book = Table('book', meta,
             Column('id', Integer, autoincrement=True, primary_key=True),
             Column('name', String),

             )