from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client["e-commerce"]

async def test_connection():
    try:
        await db.command("ping")
        print("Conexão ao MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")

users_collection = db["users"]
products_collection = db["products"]

async def test_mongo_connection():
    count = await products_collection.count_documents({})
    print(f"Total products in collection: {count}")
