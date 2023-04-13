"""Scheduler

Test Scheduler Service.
"""
import pytest

from src.pymeet.services.meeting_scheduler import MeetingSchedulerService
from src.pymeet.services.service_exceptions import UserNotFoundException
from tests.mocks import FakeUserRepository, FakeMeetingRepository


class TestScheduler:

    def test_a_meeting_can_be_scheduled(self):
        """
        Tests a meeting can be scheduled.
        """
        # Given
        users = FakeUserRepository()
        users.add(username="user1", password="a_password", email="an@email.com")
        meetings = FakeMeetingRepository()

        service = MeetingSchedulerService(users=users, meetings=meetings)

        # When
        name, attendees, options = "A Meeting", {"user1"}, [{"date": "2021-01-01", "hour": 10}]
        meeting_event = service.schedule(name=name, attendees=attendees, options=options)

        # Then
        assert meeting_event in meetings.find_all()
        assert meeting_event.name == name
        assert users.find_by_username("user1") in meeting_event.attendees

    def test_a_meeting_cannot_be_scheduled_with_invalid_attendees(self):
        """
        Tests a meeting cannot be scheduled with invalid attendees.
        """
        # Given
        users = FakeUserRepository()
        users.add(username="user1", password="a_password", email="an@email.com")

        service = MeetingSchedulerService(users=users, meetings=FakeMeetingRepository())
        name, attendees, options = "A Meeting", {"user2"}, [{"date": "2021-01-01", "hour": 10}]

        # Exception
        with pytest.raises(UserNotFoundException):
            # When
            service.schedule(name=name, attendees=attendees, options=options)

    def test_a_meeting_can_be_voted_for_scheduling(self):
        """
        Tests a meeting can be voted for scheduling.
        """
        # Given
        users = FakeUserRepository()
        users.add(username="user1", password="a_password", email="an@email.com")
        users.add(username="user2", password="a_password", email="another@email.com")

        meetings = FakeMeetingRepository()

        service = MeetingSchedulerService(users=users, meetings=meetings)
