import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db_name: str = None

db = Database()

# Initialize database connection right away, not just during startup event
mongodb_uri = os.getenv("MONGODB_URI")
db.db_name = os.getenv("DB_NAME", "pixora_db")
db.client = AsyncIOMotorClient(mongodb_uri)

async def init_db():
    # Ensure indexes for better query performance and unique constraints
    await db.client[db.db_name]["users"].create_index("email", unique=True)
    print("Connected to MongoDB!")

async def get_db():
    return db.client[db.db_name]