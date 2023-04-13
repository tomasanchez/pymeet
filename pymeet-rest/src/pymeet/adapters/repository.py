"""Repository

This module abstracts the Persistence layer with a Repository pattern.
"""
import abc
from abc import ABC
from typing import TypeVar

from pymeet.domain.models import User

T = TypeVar("T")


class ReadOnlyRepository(abc.ABC):
    """
    Abstract base class for read-only repository implementations.
    """

    @abc.abstractmethod
    def find_all(self) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class WriteOnlyRepository(abc.ABC):
    """
    Abstract base class for write-only repository implementations.
    """

    @abc.abstractmethod
    def save(self, entity) -> None:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class Repository(ReadOnlyRepository, WriteOnlyRepository, ABC):
    """
    Abstract base class for repository implementations.
    """
    pass


class UserRepository(Repository, ABC):
    """
    Abstract base class for user repository implementations.
    """

    @abc.abstractmethod
    def find_by_username(self, username: str) -> User | None:
        """
        Finds a user by its username.

        Args:
            username (str): The username of a user.

        Returns:
            User : A user if exists, otherwise None.

        """
        raise NotImplementedError


class MeetingEventRepository(Repository, abc.ABC):
    """
    Abstract base class for meeting event repository implementations.
    """
    pass


class ListRepository(Repository):
    """
    A list repository implementations.
    """

    def __init__(self):
        self._data = []

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


class ListUserRepository(UserRepository, ListRepository):
    """
    A list user repository implementations.
    """

    def find_by_username(self, username: str) -> User | None:
        """
        Finds a user by its username.

        Args:
            username (str): The username of a user.

        Returns:
            User : A user if exists, otherwise None.

        """
        return self.find_by(username=username)


class ListMeetingEventRepository(MeetingEventRepository, ListRepository):
    """
    A list meeting event repository implementations.
    """
    pass
