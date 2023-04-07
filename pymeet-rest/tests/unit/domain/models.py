"""Models

Test cases for the domain models.
"""
import datetime

import pytest

from pymeet.domain.errors import IllegalVoteError
from pymeet.domain.models import MeetingEvent, MeetingEventOption, User


class TestMeetingEventDomain:
    """
    Meeting Event Domain Test Suite
    """

    def test_can_be_voted(self):
        """
        Tests a new event can be voted.
        """
        event = MeetingEvent(name="Test Event",
                             options=list(),
                             )

        assert event.open_voting is True

    def test_can_be_set__with_options(self):
        """
        Tests Meeting Options can be set.
        """
        # Given
        option_a = MeetingEventOption(date=datetime.date(2021, 1, 1), hour=10)
        option_b = MeetingEventOption(date=datetime.date(2021, 1, 2), hour=10)

        # When
        event = MeetingEvent(name="Test Event",
                             options=[option_b, option_a])

        # Then
        assert option_b, option_a in event.options

    def test_user_can_vote(self):
        """
        Tests a user can vote.
        """
        # Given
        option = MeetingEventOption(date=datetime.date(2021, 1, 1), hour=10)

        user = User(username="Me", email="me@mail", password="a_fake_password")

        event = MeetingEvent(name="Test Event",
                             options=[option],
                             attendees={user}
                             )
        # When
        event.vote(voter=user, option=option)

        # Then
        assert user in option.votes

    def test_user_cannot_vote_if_not_attendee(self):
        """
        Tests a user cannot vote if not an attendee.
        """
        # Given
        option = MeetingEventOption(date=datetime.date(2021, 1, 1), hour=10)
        user = User(username="Me", email="me@mail", password="a_fake_password")
        event = MeetingEvent(name="Test Event", options=[option])

        # Raises / When
        with pytest.raises(IllegalVoteError):
            event.vote(voter=user, option=option)

    def test_user_cannot_vote_if_voting_closed(self):
        """
        Tests a user cannot vote if voting is closed.
        """
        # Given
        option = MeetingEventOption(date=datetime.date(2021, 1, 1), hour=10)
        user = User(username="Me", email="me@mail", password="a_fake_password")
        event = MeetingEvent(name="Test Event", options=[option], attendees={user})

        event.open_voting = False

        # Raises / When
        with pytest.raises(IllegalVoteError):
            event.vote(voter=user, option=option)

    def test_user_cannot_vote_if_option_not_in_event(self):
        """
        Tests a user cannot vote if option is not in the event.
        """
        # Given
        option = MeetingEventOption(date=datetime.date(2021, 1, 1), hour=10)
        invalid_option = MeetingEventOption(date=datetime.date(2021, 1, 2), hour=10)
        user = User(username="Me", email="me@mail", password="a_fake_password")
        event = MeetingEvent(name="Test Event", options=[option], attendees={user})

        # Raises / When
        with pytest.raises(IllegalVoteError):
            event.vote(voter=user, option=invalid_option)

    def test_can_be_closed_with_most_voted_option(self):
        """
        Tests a Meeting Event can be closed with the most voted option.
        """
        # Given
        user_a = User(username="Me",
                      email="an@email.com",
                      password="a_fake_password")

        user_b = User(username="You",
                      email="another@email.com",
                      password="a_fake_password")

        option_a = MeetingEventOption(date=datetime.date(2021, 1, 1),
                                      hour=10,
                                      votes=[user_a, user_b],
                                      )

        option_b = MeetingEventOption(date=datetime.date(2021, 1, 2), hour=10)

        event = MeetingEvent(name="Test Event",
                             options=[option_b, option_a])

        # When
        voted_date_time = event.close_voting()

        # Then
        assert event.open_voting is False
        assert voted_date_time == datetime.datetime.combine(option_a.date,
                                                            datetime.time(hour=option_a.hour))
        assert event.voted_date == voted_date_time

    def test_can_add_attendees(self):
        """
        Test an attendee can be added.
        """
        # Given
        user = User(username="Me",
                    email="an@email.com",
                    password="a_fake_password")
        event = MeetingEvent(name="Test Event",
                             options=list(),
                             )

        # When
        event.add_attendee(user)

        # Then
        assert user in event.attendees
