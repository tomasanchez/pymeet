"""Service Exceptions

Exceptions related to service operations.

"""


class UserNotFoundException(Exception):
    """
    Raised when a username is not found.
    """
    pass


class MeetingNotFoundException(Exception):
    """
    Raised when a meeting is not found.
    """
    pass


class ForbiddenOperationException(Exception):
    """
    Raised when an operation is forbidden.
    """
    pass
