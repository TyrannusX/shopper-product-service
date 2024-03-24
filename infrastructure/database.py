from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_HOST_NAME = os.getenv("MONGODB_HOST_NAME")

client = MongoClient(MONGODB_HOST_NAME, 27017)
db = client.product
collection: Collection = db.products
