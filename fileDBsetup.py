#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('fileMeta.db')

cur = con.cursor()
cur.execute

while True:

    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Files(hashName TEXT PRIMARY KEY NOT NULL, Name TEXT NOT NULL, Owner TEXT NOT NULL, Active TEXT NOT NULL, Created NOT NULL, LastUpdated NOT NULL, Result, System)")
    print("Welcome to VAST. ")
    def date(): return cur.execute("SELECT date('now')")
    #examples for creating an account
#    cur.execute("INSERT INTO Files (Username, Password, Email, Name, Created)" +
#               "VALUES('marshalllerner', sha256('marshall'),'marshallhlerner@gmail.com', 'Marshall Lerner', date())")
    con.commit()
    break
con.close()
