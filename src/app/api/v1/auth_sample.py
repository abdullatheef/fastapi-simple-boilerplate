from typing import Annotated, Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException
from ...core.security import get_password_hash, oauth2_scheme
from ...schemas.sample_user import SampleUserRead, SampleUserCreate, SampleUserCreateInternal, LoginRequest
from ...crud.crud_sample_users import crud_sample_user


from fastapi import APIRouter, Depends, Request, Response
from ...core.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from ...core.exceptions.http_exceptions import UnauthorizedException
from datetime import timedelta
from ...core.config import settings

from ...core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_sample_user,
    create_access_token,
    create_refresh_token,
    verify_token,
)


router = APIRouter(tags=["sample"])

@router.post("/my-signup", response_model=SampleUserRead, status_code=201)
async def write_user(
    request: Request, user: SampleUserCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> SampleUserRead:

    email_row = await crud_sample_user.exists(db=db, email=user.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")

    username_row = await crud_sample_user.exists(db=db, username=user.username)
    if username_row:
        raise DuplicateValueException("Username not available")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = SampleUserCreateInternal(**user_internal_dict)
    created_user: SampleUserRead = await crud_sample_user.create(db=db, object=user_internal)
    return created_user


@router.post("/my-login", response_model=Token)
async def login_for_access_token(
    response: Response,
    login_data: LoginRequest,  # Accept JSON instead of form data
    db: AsyncSession = Depends(async_get_db),
) -> dict[str, str]:
    user = await authenticate_sample_user(
        username_or_email=login_data.username,
        password=login_data.password,
        db=db
    )
    if not user:
        raise UnauthorizedException("Wrong username, email, or password.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

    refresh_token = await create_refresh_token(data={"sub": user["username"]})
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Lax", max_age=max_age
    )

    return {"access_token": access_token, "token_type": "bearer"}