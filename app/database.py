from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
import os 
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("CONNECTION_STRING")
async def connect_to_mongodb():
    try:
        client = AsyncIOMotorClient(DATABASE_URL)
        return client
    except OperationFailure as e:
        print(f"Could not connect to MongoDB: {e}")

async def close_mongodb_connection(client: AsyncIOMotorClient):
    client.close()



