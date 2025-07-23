from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import UserDB, UserList, Message, UserPublic, UserSchema


app = FastAPI()

database = []