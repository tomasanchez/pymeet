"""User Entry Point

This module contains the entry point for the user domain object.
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED

from pymeet.domain.schemas import UserIn, UserResponse, BaseUser
from pymeet.services.dependencies import get_register_service
from pymeet.services.register import IllegalUserException, RegisterService

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

RegisterServiceDependency = Annotated[RegisterService, Depends(get_register_service)]


@router.post("/", status_code=HTTP_201_CREATED)
def register_user(user_form: UserIn, user_repository: RegisterServiceDependency) -> UserResponse:
    """
    Register a new user.
    """

    try:
        user = user_repository.register(username=user_form.username,
                                        email=user_form.email,
                                        password=user_form.password1)
    except IllegalUserException as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e)) from e

    return UserResponse(data=BaseUser(**{"username": user.username, "email": user.email}))
