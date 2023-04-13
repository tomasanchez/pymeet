"""Meeting Scheduler Service

Schedules a meeting event.
"""
import datetime
from typing import Any

from pymeet.adapters.repository import MeetingEventRepository, UserRepository
from pymeet.domain.errors import IllegalVoteException
from pymeet.domain.models import MeetingEvent, MeetingEventOption
from pymeet.services.service_exceptions import UserNotFoundException, MeetingNotFoundException, \
    ForbiddenOperationException


class MeetingSchedulerService:

    def __init__(self, meetings: MeetingEventRepository, users: UserRepository):
        self.meetings = meetings
        self.users = users

    def schedule(self,
                 name: str,
                 attendees: set[str],
                 options: list[dict[str, Any]]) -> MeetingEvent:
        """
        Schedules a Meeting Event.

        Args:
            name (str): The name of the meeting.
            attendees (list[str]): The attendees of the meeting.
            options (list[dict[str, str]]): The options of the meeting.

        Raises:
            InvalidMeetingEvent: Raised when the meeting event is invalid.
        """

        users = list()

        if attendees:
            all_users = self.users.find_all()

            users = [user for user in all_users if user.username in attendees]

            usernames = [user.username for user in users]

            users_not_found = [user for user in attendees
                               if user not in
                               usernames]

            if users_not_found:
                raise UserNotFoundException(f"Users not found: {users_not_found}")

        options = [MeetingEventOption(date=option["date"], hour=option["hour"]) for option in options]

        meeting = MeetingEvent(name=name, attendees=set(users), options=options)

        self.meetings.save(meeting)

        return meeting

    def vote(self, meeting_id: str, username: str, date: datetime.date, hour: int):
        """
        Vote for a meeting event.

        Args:
            meeting_id (str): The id of the meeting.
            username (str): The username who votes.
            date (datetime.date): The date of the option.
            hour (int): The hour of the option.
        """
        meeting: MeetingEvent = self.meetings.find_by(id=meeting_id)

        if not meeting:
            raise MeetingNotFoundException(f"Meeting not found: {meeting_id}")

        user = self.users.find_by_username(username=username)

        if not user:
            raise UserNotFoundException(f"User not found: {username}")

        option = MeetingEventOption(date=date, hour=hour)

        try:
            meeting.vote(user, option)
        except IllegalVoteException as e:
            raise ForbiddenOperationException() from e

        self.meetings.save(meeting)

    def toggle_voting(self, meeting_id: str, username: str, voting: bool | None = None):
        """
        Toggle the voting of a meeting event.

        Args:
            meeting_id (str): The id of the meeting.
            username (str): The username who votes.
            voting (bool): The voting status.
        """
        meeting: MeetingEvent = self.meetings.find_by(id=meeting_id)

        if not meeting:
            raise MeetingNotFoundException(f"Meeting not found: {meeting_id}")

        try:
            meeting.toggle_voting(username, voting)
        except IllegalVoteException as e:
            raise ForbiddenOperationException() from e

        self.meetings.save(meeting)
