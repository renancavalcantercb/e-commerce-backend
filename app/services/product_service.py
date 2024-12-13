from app.core.database import products_collection

async def get_products_paginated(page: int, limit: int) -> list:
    skip = (page - 1) * limit
    cursor = products_collection.find().skip(skip).limit(limit)
    
    products = []
    async for product in cursor:
        product["_id"] = str(product["_id"])  # Converte ObjectId para string
        products.append(product)
    
    return products
