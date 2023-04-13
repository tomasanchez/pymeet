"""Meeting Event  

Entry point for the Meeting Event API.
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY

from pymeet.domain.models import MeetingEvent, MeetingEventOption
from pymeet.domain.schemas import MeetingEventOut, BaseUser, MeetingOptionOut, MeetingResponse, MeetingEventIn
from pymeet.services.dependencies import MeetingRepositoryDependency, get_meeting_scheduler_service
from pymeet.services.meeting_scheduler import MeetingSchedulerService
from pymeet.services.service_exceptions import UserNotFoundException

router = APIRouter(prefix="/meetings", tags=["meetings"])

MeetingSchedulerDependency = Annotated[MeetingSchedulerService, Depends(get_meeting_scheduler_service)]


def meeting_option_to_schema_out(option: MeetingEventOption) -> MeetingOptionOut:
    users = list((BaseUser(**{"username": user.username, "email": user.email}) for user in option.votes))

    data = {"votes": users, "date": option.date, "hour": option.hour}

    return MeetingOptionOut(**data)


def meeting_to_schema_out(meeting: MeetingEvent) -> MeetingEventOut:
    users = list((BaseUser(**{"username": user.username, "email": user.email}) for user in meeting.attendees))
    options = list((meeting_option_to_schema_out(option) for option in meeting.options))

    data = {
        "name": meeting.name,
        "attendees": users,
        "options": options
    }

    return MeetingEventOut(**data)


@router.get("/", status_code=HTTP_200_OK)
def get_meetings(repository: MeetingRepositoryDependency) -> MeetingResponse:
    """
    Retrieves all the meetings.
    """
    meetings = repository.find_all()

    data = [meeting_to_schema_out(meeting) for meeting in meetings]

    return MeetingResponse(data=data)


@router.get("/{meeting_id}", status_code=HTTP_200_OK)
def get_meeting(meeting_id: str, repository: MeetingRepositoryDependency) -> MeetingResponse:
    """
    Obtains information related to a specific meeting.
    """
    meeting = repository.find_by(name=meeting_id)

    if meeting is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Meeting not found")

    data = meeting_to_schema_out(meeting)

    return MeetingResponse(data=data)


@router.post("/", status_code=HTTP_201_CREATED)
def schedule_meeting(meeting_form: MeetingEventIn,
                     scheduler: MeetingSchedulerDependency
                     ) -> MeetingResponse:
    """
    Schedules a meeting.
    """
    options_list = list((option.dict() for option in meeting_form.options))

    attendees = list(meeting_form.organizer) + list(meeting_form.attendees)

    try:
        meeting = scheduler.schedule(name=meeting_form.name,
                                     attendees=set(attendees),
                                     options=options_list)
        return MeetingResponse(data=meeting_to_schema_out(meeting))
    except UserNotFoundException as e:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
