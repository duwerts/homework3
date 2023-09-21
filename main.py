import sqlite3
import random

from faker import Faker
from flask import Flask

app = Flask(__name__)
fake = Faker()


@app.route("/")
def hello():
    return("hello")


def customers_table():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT
        )
        
    ''')
    for i in range(100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        cursor.execute('INSERT INTO customers (first_name, last_name) VALUES (?, ?)',
                       (first_name, last_name))
    conn.commit()


def tracks_table():
    conn = sqlite3.connect("tracks.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        Length INTEGER,
        date DATE
    )
    ''')


    for i in range(100):
        title = fake.catch_phrase()
        artist = fake.name()
        length = random.randint(120, 600)
        release_date = fake.date_between(start_date='-5y', end_date='today')
        cursor.execute('INSERT INTO tracks (title, artist, length, release_date) VALUES (?, ?, ?, ?)',
                       (title, artist, length, release_date))
    conn.commit()


@app.route('/names/')
def get_names():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(DISTINCT first_name) FROM customers')
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@app.route("/tracks")
def get_tracks():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tracks')
    count = cursor.fetchone()[0]
    return str(count)

@app.route('/tracks-sec/')
def get_length():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, length FROM tracks')
    tracks = cursor.fetchall()
    out = [{'title': track[0], 'length_seconds': track[1]} for track in tracks]
    return str(out)


if __name__ == '__main__':
    customers_table()
    tracks_table()
    app.run()

