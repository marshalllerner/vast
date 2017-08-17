#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import socket
import hashlib
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1023

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        filename='mytext.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break


def sha256sum(t):
    return hashlib.sha256(t).hexdigest()

con = lite.connect('testaccounts.db')

cur = con.cursor()
cur.execute
con.create_function("sha256", 1, sha256sum)

while True:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Accounts")

    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(Id TEXT PRIMARY KEY NOT NULL, Password TEXT, Name TEXT NOT NULL, Created NOT NULL, Batches, Results)")
    print("Welcome to VAST. ")
    x = sha256sum('chuck')

    #examples for creating an account
    cur.execute("INSERT INTO Accounts (Id, Password, Name, Created)" +
                "VALUES('HIII', sha256('jerry'), 'chucky berry', 220000)")
    cur.execute("INSERT INTO Accounts (Id, Password, Name, Created) VALUES('HII', sha256('hi'), 'chky berry', 2200)")

    con.commit()
    break
con.close()
