from datetime import datetime 
from sqlalchemy import func
from sqlalchemy.orm import (registry, Mapped, mapped_column)
from sqlalchemy import create_engine

table_registry = registry()


#tabela que gerencia o registro de usuarios num banco de dados
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
 
    id: Mapped[int] = mapped_column(init= False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


