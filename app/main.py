from fastapi import FastAPI
from app.routes import user, product, order
from app.core.database import test_connection, test_mongo_connection

app = FastAPI(title="E-commerce API", version="1.0")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(product.router, prefix="/products", tags=["Products"])
# app.include_router(order.router, prefix="/orders", tags=["Orders"])

@app.on_event("startup")
async def startup_event():
    await test_connection()
    await test_mongo_connection()

for route in app.routes:
    print(f"Route: {route.path} | Name: {route.name}")
