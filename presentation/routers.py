from fastapi import APIRouter
from application import dtos, handlers
from infrastructure import repositories, brokers


# Dependencies
product_router = APIRouter()
product_repository = repositories.ProductRepository()
message_broker = brokers.RabbitMqBroker()
create_product_handler = handlers.CreateProductHandler(product_repository, message_broker)
update_product_handler = handlers.UpdateProductHandler(product_repository, message_broker)
get_product_handler = handlers.GetProductHandler(product_repository)


@product_router.post("/products/")
async def create_product(create_product: dtos.CreateProduct):
    return await create_product_handler.handle(create_product)


@product_router.put("/products/")
async def update_product(update_product: dtos.UpdateProduct):
    return await update_product_handler.handle(update_product)


@product_router.get("/products/{product_id}")
async def get_product(product_id: str):
    return await get_product_handler.handle(dtos.GetProduct(id=product_id))
