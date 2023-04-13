"""
Mocks for testing.
"""

from src.pymeet.adapters.repository import T, Repository
from src.pymeet.adapters.repository import UserRepository, MeetingEventRepository
from src.pymeet.domain.models import User


class InMemoryRepository(Repository):
    """
    A list in memory repository implementations.
    """

    def __init__(self, data: list[T] | None = None):
        self._data = data or list()

    def find_all(self) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        return self._data

    def find_by(self, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        properties = kwargs.keys()
        return next((x for x in self._data if all(getattr(x, p) == kwargs[p] for p in properties)), None)

    def save(self, entity) -> None:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        self._data.append(entity)

    def delete(self, entity) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        self._data.remove(entity)


class FakeUserRepository(UserRepository, InMemoryRepository):

    def __init__(self, users: list[User] | None = None):
        super().__init__(data=users)

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
        self._data.append(User(username=username, password=password, email=email))


class FakeMeetingRepository(MeetingEventRepository, InMemoryRepository):
    pass
