"""
Register Service Test
"""
import pytest

from src.pymeet.services.password_encoder import BcryptPasswordEncoder
from src.pymeet.services.register import RegisterService, IllegalUserException
from tests.mocks import FakeUserRepository


class TestRegisterService:
    """
    Unit test suite for the register in the service layer
    """

    def test_register_with_encoded_password(self):
        """
        Test that the register service registers a user with an encoded password
        """

        # Given
        encoder = BcryptPasswordEncoder()
        repository = FakeUserRepository()
        service = RegisterService(password_encoder=encoder,
                                  user_repository=repository
                                  )
        username, email, password = ("user1", "user@mail.com", "password1")

        # When
        registered_user = service.register(username=username, email=email, password=password)

        # Then
        encoder.verify(password, registered_user.password)

        assert registered_user in repository.find_all()

    def test_cannot_register_with_existing_username(self):
        """
        Test that the register service raises an error when an existing username is provided.
        """

        # Given
        encoder = BcryptPasswordEncoder()
        repository = FakeUserRepository()
        repository.add(username="user1", password="password1", email="an@email.com")

        service = RegisterService(password_encoder=encoder,
                                  user_repository=repository
                                  )

        username, email, password = ("user1", "another@email.com", "password1")

        # When / Then
        with pytest.raises(IllegalUserException):
            service.register(username=username, email=email, password=password)

    def test_cannot_register_with_existing_email(self):
        """
        Test that the register service raises an error when an existing email is provided.
        """

        # Given
        encoder = BcryptPasswordEncoder()
        repository = FakeUserRepository()
        username, email, password = ("user2", "user@email.com", "password1")
        repository.add(username="user1", password=password, email=email)
        service = RegisterService(password_encoder=encoder, user_repository=repository)

        # When / Then
        with pytest.raises(IllegalUserException):
            service.register(username=username, email=email, password=password)
