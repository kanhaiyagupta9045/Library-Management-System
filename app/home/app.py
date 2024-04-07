import logging
from fastapi import FastAPI
from app.database import connect_to_mongodb, close_mongodb_connection
from app.router.bookRouter import router as BookRouter
from app.router.userRouter import router as UserRouter
from app.router.borrowRouter import router as BorrowerRouter
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()
debug_mode = os.getenv("DEBUG") == "True"
app.include_router(BookRouter, tags=["Books"])
app.include_router(UserRouter, tags=["Users"])
app.include_router(BorrowerRouter, tags=["Borrowers"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    try:
        app.mongodb_client = await connect_to_mongodb()
        logger.info("MongoDB connected successfully!")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    try:
        await close_mongodb_connection(app.mongodb_client)
        logger.info("MongoDB connection closed.")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Library Management System app!"}
