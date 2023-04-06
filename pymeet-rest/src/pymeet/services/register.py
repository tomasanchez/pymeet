"""
Register Service
"""
from pymeet.adapters.repository import UserRepository
from pymeet.domain.models import User
from pymeet.services.password_encoder import PasswordEncoder


class IllegalUserException(Exception):
    pass


class RegisterService:
    """
    Registration Service
    """

    def __init__(self, user_repository: UserRepository, password_encoder: PasswordEncoder):
        self.user_repository = user_repository
        self.password_encoder = password_encoder

    def _verify_username(self, username: str):
        """
        Verifies if the username is available.

        Args:
            username (str): The username to verify.

        Raises:
            UserAlreadyExistsException: If the username is already in use.
        """
        user = self.user_repository.find_by(username=username)
        if user:
            raise IllegalUserException(f"Username {username} already in use.")

    def _verify_email(self, email: str):
        """
        Verifies if the email is available.

        Args:
            email (str): The email to verify.

        Raises:
            UserAlreadyExistsException: If the email is already in use.
        """
        user = self.user_repository.find_by(email=email)
        if user:
            raise IllegalUserException(f"Email {email} already in use.")

    def register(self, username, email, password):
        """
        Registers a new user.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user.

        Raises:
            UserAlreadyExistsException: If the username or email is already in use.
        """

        self._verify_username(username)
        self._verify_email(email)

        hashed_password = self.password_encoder.encode(password)

        user = User(username=username, email=email, password=hashed_password)

        self.user_repository.save(user)
        return user
