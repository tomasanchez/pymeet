"""
Mocks for testing.
"""
from pymeet.domain.models import User
from src.pymeet.adapters.repository import UserRepository


class FakeUserRepository(UserRepository):

    def __init__(self, users: list[User] | None = None):
        self._users = users or []

    def find_all(self) -> list[User]:
        return self._users

    def find_by(self, **kwargs) -> User | None:
        properties = kwargs.keys()
        return next((x for x in self._users if all(getattr(x, p) == kwargs[p] for p in properties)), None)

    def save(self, entity: User) -> None:
        self._users.append(entity)

    def delete(self, entity) -> None:
        self._users.remove(entity)

    def find_by_username(self, username: str) -> User | None:
        return self.find_by(username=username)

    def add(self, username: str, password: str, email: str):
        """
        Adds a user.

        Args:
            username: The user's username.
            password: The user's password.
            email: The user's email.
        """
        self._users.append(User(username=username, password=password, email=email))
