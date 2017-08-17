#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import hashlib

cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
)

def md5sum(t):
    return hashlib.md5(t).hexdigest()

con = lite.connect('test.db')

cur = con.cursor()
cur.execute
con.create_function("md5", 1, md5sum)

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Cars")

    cur.execute("CREATE TABLE IF NOT EXISTS Cars(Id INT, Name TEXT, Price INT)")
    cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
    cur.execute("INSERT INTO Cars VALUES(9, 'Bmw', 220000)")
