"""Models
    This module contains the domain objects and errors used by pymeet.
"""
import datetime
import uuid

from pymeet.domain.errors import IllegalVoteException, IllegalUserException


class User:
    """
    Represents a user.

    Attributes:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    """

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User({self.username}, {self.email})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False

        return self.username == other.username

    def __hash__(self):
        return hash(self.username)


class MeetingEventOption:
    """
    Represents an option for a meeting event.

    Attributes:
        date (datetime.date): A proposal date for the event.
        hour (int): A proposal hour for the event.
        votes (list[User]): Who votes for this option.
    """

    def __init__(self,
                 date: datetime.date = datetime.date.today(),
                 hour: int = 0,
                 votes: list[User] | None = None
                 ):
        self.id = str(uuid.uuid4())
        self.date = date
        self.hour = hour
        self.votes = votes or []

    def vote(self, attendee: User):
        """
        Vote for the option.

        Args:
            attendee (User): The attendee who votes.
        """
        self.votes.append(attendee)

    def __repr__(self) -> str:
        return f"Option({self.date}, {self.hour}, {self.votes})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, MeetingEventOption):
            return False

        return self.date == other.date and self.hour == other.hour

    def __hash__(self):
        return hash((self.date, self.hour))


class MeetingEvent:
    """
    Represents a meeting event.

    Attributes:
        name (str): The name of the event.
        attendees (list[str]): The attendees of the event.
        options (list[Option]): The options for the event.
    """

    def __init__(self,
                 name: str,
                 options: list[MeetingEventOption],
                 attendees: set[User] | None = None,
                 voted_date: datetime.datetime | None = None,
                 open_voting: bool = True,
                 ):
        self.name = name
        self.options: set = set(options)
        self.attendees: set = attendees or set()
        self.voted_date = voted_date
        self.open_voting = open_voting

    def toggle_voting(self, user: str, voting: bool | None = None):
        """
        Toggles the voting status of the event.

        Args:
            user (str): The user who toggles the voting.
            voting (Optional[bool]): The new status of the voting. Defaults to None.
        """
        owner = list(self.attendees)[0]

        if owner.username is not user:
            raise IllegalUserException("Only the owner of the event can toggle the voting.")

        self.open_voting = voting if voting is not None else not self.open_voting

    def close_voting(self) -> datetime.datetime:
        """
        Sets the most voted option as the final date for the event.

        Returns:
            datetime.datetime: The date and time which had most votes.
        """
        self.open_voting = False

        most_voted_option: MeetingEventOption = max(self.options, key=lambda option: len(option.votes))

        self.voted_date = datetime.datetime.combine(most_voted_option.date, datetime.time(hour=most_voted_option.hour))

        return self.voted_date

    def vote(self, voter: User, option: MeetingEventOption):
        """
        Vote for an option.

        Args:
            voter (User): The attendee who votes.
            option (MeetingEventOption): The option to vote.

        Raises:
            IllegalVoteError: If the voter is not an attendee of the event or if the voting is closed.
        """
        if voter not in self.attendees:
            raise IllegalVoteException(f"{voter.username} is not an attendee of this event.")

        if not self.open_voting:
            raise IllegalVoteException("Voting is closed.")

        if option not in self.options:
            raise IllegalVoteException(f"{option} is not an option for this event.")

        option.vote(voter)

    def add_attendee(self, attendee: User):
        """
        Adds an attendee to the event.

        Args:
            attendee (User): The attendee to add.
        """
        self.attendees.add(attendee)

    def __repr__(self):
        return f"Event({self.name}, {self.voted_date or 'TBD'}, {self.attendees})"

    def __hash__(self):
        return hash(self.__repr__())

    def __lt__(self, other):
        return self.voted_date < other.voted_date

    def __gt__(self, other):
        return self.voted_date > other.voted_date

    def __le__(self, other):
        return self.voted_date <= other.start

    def __ge__(self, other):
        return self.voted_date >= other.start

    def __ne__(self, other):
        return not self.__eq__(other)
