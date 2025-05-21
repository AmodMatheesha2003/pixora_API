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

    # index for VerificationRequests collection
    # Compound index for user_id and request_date to optimize the query
    await db.client[db.db_name]["VerificationRequests"].create_index([
        ("user_id", 1),  # 1 for ascending order
        ("request_date", -1)  # -1 for descending order
    ])

    # Add index for status field which will be used in queries
    await db.client[db.db_name]["VerificationRequests"].create_index("status")

    # Ensure indexes for better query performance and unique constraints
    await db.client[db.db_name]["users"].create_index("email", unique=True)
    print("Connected to MongoDB!")

async def get_db():
    return db.client[db.db_name]