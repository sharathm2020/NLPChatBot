import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as chat_router
from app.auth_routes import router as auth_router
from app.todo_routes import router as todo_router

# ---------------------------------------------------
# Logging Setup
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
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
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Routers
# ---------------------------------------------------
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(todo_router)

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------
@app.get("/")
def read_root():
    logger.info("GET request to root endpoint.")
    return {"message": "Welcome to the NLP ChatBot API!"}