from typing import Annotated
from http import HTTPStatus
from fastapi import Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fastapi import APIRouter, Depends, HTTPException
from fast_zero.schemas import TodoFilter, TodoSchema, TodoPublic, TodoList
from fast_zero.security import get_current_user


Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model= TodoPublic)
async def create_task(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session):

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
async def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[TodoFilter, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    )

    return {'todos': todos.all()}
