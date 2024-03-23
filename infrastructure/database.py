from pymongo import MongoClient
from pymongo.collection import Collection


client = MongoClient("mongodb", 27017)
db = client.product
collection: Collection = db.products
