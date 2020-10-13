from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import sqlite3
import os

if os.path.exists('book.db'):
    os.remove('book.db')

conn = sqlite3.connect('book.db')
conn.execute("CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author TEXT NOT NULL)")
conn.execute("INSERT INTO book (title,author) VALUES ('The Great Gatsby', 'F. Scott Fitzgerald')")
conn.execute("INSERT INTO book (title,author) VALUES ('Moby Dick', 'Herman Melville')")
conn.commit()
conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def find_all():
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def save(titre, author):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO book (title,author) VALUES ('{title}', '{author}')".format(title = titre, author = author))
    conn.commit()
    conn.close()

def delete(bookid):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM book WHERE id={bookid}".format(bookid = bookid))
    conn.commit()
    conn.close()

def update(bookid,title,author):
    conn = sqlite3.connect('book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE book SET title='{title}', author='{author}' WHERE id={bookid}".format(title = title, author = author, bookid = bookid))
    conn.commit()
    conn.close()