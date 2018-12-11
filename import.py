#!/usr/bin/python3
#
# import.py - imports books.csv to the database
#
# Author: Zalkar Ziiaidin uulu
# Date created: 12/5/2018
#
#

# import files
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv


engine = create_engine('postgres://evvuybdksjmxgc:793e1cae388415ba1126d5407211d96e624c402990c436b69b0c562fc91ceed5@ec2-54-163-230-178.compute-1.amazonaws.com:5432/dabk5r98m602n0')
db = scoped_session(sessionmaker(bind=engine))


def main():
    file = open("books.csv")
    reader = csv.reader(file)

    for id, title, author, year in reader:
        db.execute("INSERT INTO books (id, title, author, year) VALUES (:id, :title, :author, :year)",
                   {"id": id, "title": title, "author": author, "year": year})
        print({id}, " ", {title})
        db.commit()


if __name__ == "__main__":
    main()
