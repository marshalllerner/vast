#!/usr/bin/python

from pymongo import MongoClient
import datetime
import hashlib
#from flask_bcrypt import Bcrypt
# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
def sha256sum(t):
    return hashlib.sha256(t).hexdigest()


client = MongoClient()
db = client.test
coll = db.dataset
hashpass = bcrypt.hashpw('marshall')
print hashpass

hashpass = bcrypt.hashpw('marshall', bcrypt.genSalt())

coll.remove()
coll.remove()
coll.insert_one({
    "BOINCauth": "",
    "Batches": [],
    "Created": "2017-08-23",
    "Email": "marshallhlerner@gmail.com",
    "Name": "Marshall Lerner",
    "Password": hashpass,
    "Results": [],
    "Username": "marshalllerner"
})
cursor = coll.find()
for doc in cursor:
    pprint(doc)
    print
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)
