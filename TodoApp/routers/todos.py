import sys
sys.path.append('..')

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception


router = APIRouter()

models.Base.metadata.create_all(bind=engine)



def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="priority is between 1-5")
    complete: bool


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(
        models.Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise http_execption()


@router.post("/")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return successful_response(201)


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(
        models.Todos.id == user.get("id")).first()

    if todo_model is None:
        raise http_execption()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, users: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if users is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id) \
        .filter(models.Todos.id == users.get("id")).first()

    if todo_model is None:
        raise http_execption()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'successful'
    }


def http_execption():
    raise HTTPException(status_code=404, detail="Todo no found")
