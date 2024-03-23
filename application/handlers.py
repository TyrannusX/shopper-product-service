from abc import ABC, abstractmethod
from application import dtos, exceptions
from domain import models, validators
from infrastructure import repositories, brokers
import logging


class Handler(ABC):
    @abstractmethod
    async def handle(self, dto):
        pass


class CreateProductHandler(Handler):
    def __init__(self, product_repository: repositories.CrudRepository, message_broker: brokers.MessageBroker):
        self.product_repository = product_repository
        self.message_broker = message_broker

    async def handle(self, create_product: dtos.CreateProduct):
        product: models.Product = models.Product()

        product.id = None
        product.name = create_product.name
        product.quantity = create_product.starting_quantity
        product.price = create_product.starting_price

        if not validators.validate_quantity(product):
            message = f"Quantity cannot be negative when creating a product!"
            logging.debug(message)
            raise exceptions.BadRequestException(message)

        if not validators.validate_price(product):
            message = f"Price cannot be negative when creating a product!"
            logging.debug(message)
            raise exceptions.BadRequestException(message)

        try:
            new_id = await self.product_repository.create(product)
        except Exception as ex:
            logging.exception("Error occurred while attempting to create product")
            raise
        else:
            product_created = dtos.ProductCreated(created_id=new_id)
            await self.message_broker.publish(product_created, str(dtos.ProductCreated.__name__))
            return product_created


class UpdateProductHandler(Handler):
    def __init__(self, product_repository: repositories.CrudRepository, message_broker: brokers.MessageBroker):
        self.product_repository = product_repository
        self.message_broker = message_broker

    async def handle(self, update_product: dtos.UpdateProduct):
        existing_product: models.Product = await self.product_repository.read(update_product.id)

        if existing_product is None:
            logging.debug("Product with id {id} does not exist!", update_product.id)
            raise exceptions.NotFoundException(f"Product with id {update_product.id} does not exist!")

        existing_product.name = update_product.name
        existing_product.quantity = update_product.new_quantity
        existing_product.price = update_product.new_price

        if not validators.validate_quantity(existing_product):
            logging.debug("Quantity cannot be negative when updating product {product_id}!", existing_product.id)
            raise exceptions.BadRequestException(f"Quantity cannot be negative when updating product {existing_product.id}!")

        if not validators.validate_price(existing_product):
            logging.debug("Price cannot be negative when updating product {product_id}!", existing_product.id)
            raise exceptions.BadRequestException(f"Price cannot be negative when updating product {existing_product.id}!")

        try:
            await self.product_repository.update(existing_product)
        except Exception as ex:
            logging.exception("Error occurred while attempting to update product {product_id}", existing_product.id)
            raise
        else:
            product_updated = dtos.ProductUpdated(updated_id=existing_product.id)
            await self.message_broker.publish(product_updated, str(dtos.ProductUpdated.__name__))
            return product_updated


class GetProductHandler(Handler):
    def __init__(self, product_repository: repositories.CrudRepository):
        self.product_repository = product_repository

    async def handle(self, get_product: dtos.GetProduct):
        found_product: models.Product = await self.product_repository.read(get_product.id)

        if found_product is None:
            logging.debug("Product with id {id} does not exist!", get_product.id)
            raise exceptions.NotFoundException(f"Product with id {get_product.id} does not exist!")

        return dtos.ApplicationProduct(id=found_product.id, name=found_product.name, price=found_product.price, quantity=found_product.quantity)
