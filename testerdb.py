#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import socket
import hashlib
from threading import Thread
from SocketServer import ThreadingMixIn


def sha256sum(t):
    return hashlib.sha256(t).hexdigest()

con = lite.connect('accounts.db')

cur = con.cursor()
cur.execute
con.create_function("sha256", 1, sha256sum)

while True:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Accounts")

    cur.execute("CREATE TABLE IF NOT EXISTS Accounts(Username TEXT PRIMARY KEY NOT NULL, Password TEXT, Email TEXT NOT NULL, Name TEXT NOT NULL, Created NOT NULL, Batches, Results, BOINCauth)")
    print("Welcome to VAST. ")
    def date(): return cur.execute("SELECT date('now')")
    #examples for creating an account
    cur.execute("INSERT INTO Accounts (Username, Password, Email, Name, Created)" +
               "VALUES('marshalllerner', sha256('marshall'),'marshallhlerner@gmail.com', 'Marshall Lerner', date())")
#    cur.execute("INSERT INTO Accounts (Id, Password, Name, Created) VALUES('HII', sha256('hi'), 'chky berry', 2200)")

    con.commit()
    break
con.close()




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
        f = open("tst.txt",'rb')
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

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
