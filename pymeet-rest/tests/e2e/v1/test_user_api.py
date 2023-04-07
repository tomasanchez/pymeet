"""
Test for User resource API endpoints.
"""
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY

from pymeet.services.dependencies import get_user_repository
from tests.conftest import DependencyOverrider

prefix = "api/v1"
users_endpoint = "users"


class TestUserAPI:
    """
    Test for User resource API endpoints.
    """

    def test_get_all_users(self, test_client, user_repository):
        """
        Test for getting all users.
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "an@email.com", "password1"
        user_repository.add(username=username, password=password, email=email)
        json_data = {
            "username": username,
            "email": email
        }

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.get(f"/{prefix}/{users_endpoint}")

            # then
            assert response.status_code == HTTP_200_OK
            assert response.json() == {
                "data": [
                    json_data
                ]
            }

    def test_can_register_user(self, test_client, user_repository):
        """
        Test for registering a user.
        """
        # given
        override = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "a_valid@email.com", "password1"

        request_body = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": password
        }

        with DependencyOverrider(overrides=override):
            # when
            response = test_client.post(f"/{prefix}/{users_endpoint}", json=request_body)

            # then
            assert response.status_code == HTTP_201_CREATED
            assert response.json() == {
                "data": {
                    "username": username,
                    "email": email
                }
            }

    def test_cannot_register_an_existing_user(self, test_client, user_repository):
        """
        Test for registering an existing user must return conflict.
        """
        # given
        override = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "a_valid@email.com", "password1"
        user_repository.add(username=username, password=password, email=email)
        request_body = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": password
        }

        with DependencyOverrider(overrides=override):
            # when
            response = test_client.post(f"/{prefix}/{users_endpoint}", json=request_body)

            # then
            assert response.status_code == HTTP_409_CONFLICT

    def test_cannot_register_an_user_with_email_in_use(self, test_client, user_repository):
        """
        Test for registering a user which email has already been registered must return conflict.
        """
        # given
        override = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "a_valid@email.com", "password1"
        user_repository.add(username=username, password=password, email=email)
        request_body = {
            "username": "user2",
            "email": email,
            "password1": password,
            "password2": password
        }

        with DependencyOverrider(overrides=override):
            # when
            response = test_client.post(f"/{prefix}/{users_endpoint}", json=request_body)

            # then
            assert response.status_code == HTTP_409_CONFLICT

    def test_cannot_register_user_when_passwords_don_t_match(self, test_client, user_repository):
        """
        Test for registering a user with different passwords must return conflict.
        """
        # given
        override = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "an@email.com", "password1"

        request_body = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": "different_password"
        }

        with DependencyOverrider(overrides=override):
            # when
            response = test_client.post(f"/{prefix}/{users_endpoint}", json=request_body)

            # then
            assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    def test_cannot_register_user_with_invalid_email(self, test_client, user_repository):
        """
        Test for registering a user with invalid email must return conflict.
        """
        # given
        override = {get_user_repository: lambda: user_repository}
        username, email, password = "user1", "invalid_email", "password1"

        request_body = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": password
        }

        with DependencyOverrider(overrides=override):
            # when
            response = test_client.post(f"/{prefix}/{users_endpoint}", json=request_body)

            # then
            assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
