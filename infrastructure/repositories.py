from abc import ABC, abstractmethod
from domain import models
from infrastructure import database
from pymongo.collection import ObjectId


class CrudRepository(ABC):
    @abstractmethod
    async def create(self, model):
        pass

    @abstractmethod
    async def read(self, id):
        pass

    @abstractmethod
    async def read_all(self):
        pass

    @abstractmethod
    async def update(self, model):
        pass

    @abstractmethod
    async def delete(self, id):
        pass


class ProductRepository(CrudRepository):
    async def create(self, model: models.Product):
        bson = self.map_to_bson(model)
        inserted_id = database.collection.insert_one(bson).inserted_id
        return str(inserted_id)

    async def read(self, id):
        bson = database.collection.find_one({"_id": ObjectId(id)})
        model = self.map_to_domain(bson)
        return model

    async def read_all(self):
        return database.collection.find()

    async def update(self, model: models.Product):
        bson = self.map_to_bson(model)
        print(bson)
        database.collection.replace_one({"_id": bson["_id"]}, bson)

    async def delete(self, id):
        database.collection.delete_one({"_id": ObjectId(id)})

    def map_to_bson(self, model: models.Product):
        bson = {
            "name": model.name,
            "price": model.price,
            "quantity": model.quantity
        }

        if model.id:
            bson["_id"] = ObjectId(model.id)

        return bson

    def map_to_domain(self, bson):
        model: models.Product = models.Product()
        model.id = str(bson["_id"])
        model.name = bson["name"]
        model.price = bson["price"]
        model.quantity = bson["quantity"]
        return model
