"""Dependencies

This module contains the dependencies for the application.
"""
from typing import Annotated

from fastapi import Depends

from pymeet.adapters.repository import UserRepository, ListUserRepository
from pymeet.services.password_encoder import PasswordEncoder, BcryptPasswordEncoder
from pymeet.services.register import RegisterService


def get_password_encoder() -> PasswordEncoder:
    """
    Returns the password encoder.
    """
    return BcryptPasswordEncoder()


PasswordEncoderDependency = Annotated[PasswordEncoder, Depends(get_password_encoder)]


def get_user_repository() -> UserRepository:
    """
    Returns the user repository.
    """
    return ListUserRepository()


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]


def get_register_service(repository: UserRepositoryDependency,
                         encoder: PasswordEncoderDependency) -> RegisterService:
    """
    Returns the register service.
    """
    return RegisterService(user_repository=repository, password_encoder=encoder)
