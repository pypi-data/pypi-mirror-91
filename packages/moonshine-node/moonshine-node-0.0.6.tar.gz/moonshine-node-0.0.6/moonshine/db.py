from pymongo import MongoClient
import os

db = MongoClient(
    os.environ.get('MONGODB_IP', 'mongodb'),
    int(os.environ.get('MONGODB_PORT', '27017'))
)
