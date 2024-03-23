from domain import models
import logging


def validate_quantity(product: models.Product):
    return product.quantity >= 0


def validate_price(product: models.Product):
    return product.price >= 0.0
