from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    starting_price: float
    starting_quantity: int


class ProductCreated(BaseModel):
    created_id: str


class UpdateProduct(BaseModel):
    id: str
    name: str
    new_price: float
    new_quantity: int


class ProductUpdated(BaseModel):
    updated_id: str


class GetProduct(BaseModel):
    id: str


class ApplicationProduct(BaseModel):
    id: str
    name: str
    price: float
    quantity: int