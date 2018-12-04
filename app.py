#!/usr/bin/python3
#
# app.py - Main Python/Flask file
#
# Author: Zalkar Ziiaidin uulu
# Date created: 12/3/2018
#
#

# import files
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# basic setup
app = Flask(__name__)

engine = create_engine('postgres://evvuybdksjmxgc:793e1cae388415ba1126d5407211d96e624c402990c436b69b0c562fc91ceed5@ec2-54-163-230-178.compute-1.amazonaws.com:5432/dabk5r98m602n0')
db = scoped_session(sessionmaker(bind=engine))

# Login
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                   {"name": request.form['name'], "password": request.form['password']})
        db.commit()

    return "Success"
