import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
if not MONGODB_URI or not DB_NAME:
    raise Exception("MONGODB_URI and DB_NAME must be set in the .env file.")

mongo_client = AsyncIOMotorClient(MONGODB_URI)
db = mongo_client[DB_NAME]
nft_collection = db["NFT"]