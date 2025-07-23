from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    password: str
    username: str
    email: EmailStr
