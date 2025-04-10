# app/todo_routes.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List

from model.db.todo_db import get_todos_from_db, add_todo_to_db, clear_todos_from_db # Import todo functions
from model.db.auth import get_authenticated_user # For auth check


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/todos", tags=["Todos"])

async def get_current_user_id(request: Request) -> str:
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_info = get_authenticated_user(token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = user_info if isinstance(user_info, str) else user_info.get('id')
    if not user_id:
         logger.error("Auth successful but failed to extract user_id in dependency.")
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication error")
    return user_id

@router.get("/", response_model=List[str])
async def get_user_todos(user_id: str = Depends(get_current_user_id)):
    """Fetches all todo items for the authenticated user."""
    logger.info(f"Fetching todos for user: {user_id}")
    try:
        todos_response = get_todos_from_db(user_id=user_id)

        if isinstance(todos_response, str):
            if todos_response == "Your to-do list is empty.":
                return []
            elif todos_response.startswith("Here"):
                 lines = todos_response.split('\n')[1:]
                 todos = [line.lstrip("- ").strip() for line in lines]
                 return todos
            else:
                 logger.warning(f"Unexpected string response from get_todos_from_db for user {user_id}: {todos_response}")
                 return []
        elif isinstance(todos_response, list):
             return todos_response
        else:
            logger.error(f"Unexpected response type from get_todos_from_db for user {user_id}: {type(todos_response)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve todos due to internal error.")

    except Exception as e:
        logger.error(f"Error fetching todos for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve todos.")

# @router.post("/")
# async def add_user_todo(task: str, user_id: str = Depends(get_current_user_id)):
#     return add_todo_to_db(task, user_id)
#
# @router.delete("/")
# async def clear_user_todos(user_id: str = Depends(get_current_user_id)):
#     return clear_todos_from_db(user_id) 