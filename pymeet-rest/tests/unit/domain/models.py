"""Models

Test cases for the domain models.
"""
import datetime

from src.pymeet.app.domain.models import MeetingEvent, MeetingEventOption


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

    def test_can_be_closed_with_most_voted_option(self):
        """
        Tests a Meeting Event can be closed with the most voted option.
        """
        # Given
        option_a = MeetingEventOption(date=datetime.date(2021, 1, 1),
                                      hour=10,
                                      votes=["Me", "You"],
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
        event = MeetingEvent(name="Test Event",
                             options=list(),
                             )
        
        # When
        event.add_attendee("Me")

        # Then
        assert "Me" in event.attendees
