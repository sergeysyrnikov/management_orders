import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.db.confdb import localSession
from app.repositories.user import UserRepo


async def get_session():
    with localSession() as session:
        yield session


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="app/token")),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.strip(), settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_repo = UserRepo(session)
    user = user_repo.get_by_id(user_id)
    if user is None:
        credentials_exception.detail = "Not found user by user_id"
        raise credentials_exception
    return user
