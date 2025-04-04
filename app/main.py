import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# ---------------------------------------------------
# Logging Setup
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Will log to logs/app.log
        logging.StreamHandler()               # Logs to terminal
    ]
)
logger = logging.getLogger(__name__)
logger.info("Starting NLP ChatBot API...")

# ---------------------------------------------------
# FastAPI App Setup
# ---------------------------------------------------
app = FastAPI(
    title="NLP ChatBot API",
    version="1.0",
    description="A natural language assistant with FastAPI backend."
)

# ---------------------------------------------------
# CORS Middleware Setup
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Routers
# ---------------------------------------------------
app.include_router(router)

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------
@app.get("/")
def read_root():
    logger.info("GET request to root endpoint.")
    return {"message": "Welcome to the NLP ChatBot API!"}
