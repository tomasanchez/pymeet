"""Models
    This module contains the domain objects and errors used by pymeet.
"""
import datetime


class MeetingEventOption:
    """
    Represents an option for a meeting event.

    Attributes:
        date (datetime.date): A proposal date for the event.
        hour (int): A proposal hour for the event.
        votes (list[str]): Who votes for this option.
    """

    def __init__(self,
                 date: datetime.date = datetime.date.today(),
                 hour: int = 0,
                 votes: list[str] | None = None
                 ):
        self.date = date
        self.hour = hour
        self.votes = votes or []

    def vote(self, attendee: str):
        """
        Vote for the option.

        Args:
            attendee (str): The attendee who votes.
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
                 attendees: set[str] | None = None,
                 voted_date: datetime.datetime | None = None,
                 open_voting: bool = True,
                 ):
        self.name = name
        self.options: set = set(options)
        self.attendees: set = attendees or set()
        self.voted_date = voted_date
        self.open_voting = open_voting

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

    def add_attendee(self, attendee: str):
        """
        Adds an attendee to the event.

        Args:
            attendee (str): The attendee to add.
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
