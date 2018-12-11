#!/usr/bin/python3
#
# app.py - Main Python/Flask file
#
# Author: Zalkar Ziiaidin uulu
# Date created: 12/3/2018
#
#

# import files
from flask import Flask, request, render_template, session, url_for, escape, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# basic setup
app = Flask(__name__)

engine = create_engine('postgres://evvuybdksjmxgc:793e1cae388415ba1126d5407211d96e624c402990c436b69b0c562fc91ceed5@ec2-54-163-230-178.compute-1.amazonaws.com:5432/dabk5r98m602n0')
db = scoped_session(sessionmaker(bind=engine))


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('login.html')


# Login
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        result = db.execute("SELECT * FROM users WHERE name = :name AND password = :password",
                            {"name": request.form['name'], "password": request.form['password']}).fetchone()

    if result is None:
        return redirect(url_for('index'))

    session['username'] = request.form['name']
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# Register
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        # check if email is available
        result = db.execute("SELECT * FROM users WHERE name = :name",
                            {"name": request.form['name']}).fetchone()

        if result is None:
            db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                       {"name": request.form['name'], "password": request.form['password']})
            db.commit()
            return redirect(url_for('main'))

    return render_template('register.html')


# Get the list of all books from the database
@app.route("/main")
def main():
    books = db.execute("SELECT * FROM books").fetchall()

    return render_template("main.html", books=books, user = session['username'])


# Get the list of all books from the database
@app.route("/library")
def library():
    books = db.execute("SELECT * FROM books").fetchall()

    return render_template("library.html", books=books, user = session['username'])


# Generates an html page for each book
@app.route("/book/<id>")
def book(id):
    my_book = db.execute("SELECT * FROM books WHERE id = :id",
                         {"id": id}).fetchone()

    import requests
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "xejDlWAAaa4vNLQElPGjHg", "isbns": id})

    reviews = res.json()

    rating_good_reads = reviews['books'][0]['average_rating']
    rating_number_good_reads = reviews['books'][0]['work_ratings_count']

    reviews_bennington = db.execute("SELECT * FROM ratings WHERE id = :id",
                         {"id": id}).fetchall()

    sum = 0
    for review in reviews_bennington:
        sum += review.rating

    if len(reviews_bennington) > 0:
        average = round(sum / len(reviews_bennington), 2)
    else:
        average = 0

    return render_template("book.html", book=my_book, user=session['username'], rating_good_reads=rating_good_reads,
                           rating_number_good_reads=rating_number_good_reads, rating_bennington=average,
                           rating_number_bennington=len(reviews_bennington), reviews_bennington=reviews_bennington)


# Add a review to the database
@app.route("/review/<id>", methods=['POST'])
def review(id):

    db.execute("INSERT INTO ratings (id, rating, review) VALUES (:id, :rating, :review)",
               {"id": id, "rating": int(request.form['rating']), "review": request.form['review']})
    db.commit()
    return book(id)


