from datetime import datetime 
from sqlalchemy import func
from sqlalchemy.orm import (registry, Mapped, mapped_column)

table_registry = registry()


#Table that manages user registration in a database
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
    updadate_at: Mapped[datetime] = mapped_column(init=False,
                                                  server_default=func.now(),
                                                  onupdate=func.now)
