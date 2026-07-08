from typing import Annotated
from http import HTTPStatus

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


