from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['fastapi_app']
users_collection = db['users']
notes_collection = db['notes']
