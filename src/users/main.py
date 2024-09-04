from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from models import User, get_db
from schemas import UserModel

app = FastAPI()

