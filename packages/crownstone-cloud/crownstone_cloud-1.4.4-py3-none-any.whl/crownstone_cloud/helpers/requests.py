"""Handler for requests to the Crownstone cloud"""
import logging
from aiohttp import ClientSession, ContentTypeError
from typing import Any, Dict
from crownstone_cloud.helpers.aiohttp_client import create_clientsession
from crownstone_cloud.helpers.conversion import quote_json
from crownstone_cloud.const import (
    BASE_URL, 
    LOGIN_URL
)
from crownstone_cloud.exceptions import (
    CrownstoneAuthenticationError,
    CrownstoneConnectionError,
    CrownstoneUnknownError,
    AuthError
)

_LOGGER = logging.getLogger(__name__)


class RequestHandler:
    """Handles requests to the Crownstone cloud."""

    def __init__(self, cloud, clientsession: ClientSession = None) -> None:
        self.cloud = cloud
        self.client_session = clientsession or create_clientsession()

    async def request_login(self, login_data: Dict[str, str]) -> dict:
        """Request a login to the Crownstone Cloud API."""
        response = await self.request('post', LOGIN_URL, login_data)

        return response

    async def post(
            self,
            model: str,
            endpoint: str,
            model_id: str = None,
            json: Dict[str, Any] = None
    ) -> dict:
        """
        Post request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param json: Dictionary with the data that should be posted.
        :return: Dictionary with the response from the cloud.
        """
        if model_id:
            url = f'{BASE_URL}{model}/{model_id}/{endpoint}?access_token={self.cloud.access_token}'
        else:
            url = f'{BASE_URL}{model}{endpoint}?access_token={self.cloud.access_token}'

        return await self.request('post', url, json)

    async def get(
            self,
            model: str,
            endpoint: str,
            filter: Dict[str, str] = None,
            model_id: str = None
    ) -> dict:
        """
        Get request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param filter: filter output or add extra data to output.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :return: Dictionary with the response from the cloud.
        """
        if filter and model_id:
            url = f'{BASE_URL}{model}/{model_id}/{endpoint}?filter={quote_json(filter)}&access_token=' \
                  f'{self.cloud.access_token}'
        elif model_id and not filter:
            url = f'{BASE_URL}{model}/{model_id}/{endpoint}?access_token={self.cloud.access_token}'
        else:
            url = f'{BASE_URL}{model}{endpoint}?access_token={self.cloud.access_token}'

        return await self.request('get', url)

    async def put(
            self,
            model: str,
            endpoint: str,
            model_id: str,
            command: str,
            value: Any
    ) -> dict:
        """
        Put request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param command: used for command requests. e.g. 'switchState'.
        :param value: the value to be put for the command. e.g 'switchState', 1
        :return: Dictionary with the response from the cloud.
        """
        url = f'{BASE_URL}{model}/{model_id}/{endpoint}?{command}={str(value)}&access_token=' \
              f'{self.cloud.access_token}'

        return await self.request('put', url)

    async def request(self, method: str, url: str, json: Dict[str, Any] = None) -> dict:
        """Make request and check data for errors"""
        async with self.client_session.request(method, url, json=json) as result:
            try:
                data = await result.json()
            except ContentTypeError:
                # when the cloud is unavailable, a payload can be received that can't be converted to a dictionary.
                raise CrownstoneConnectionError("Error connecting to the Crownstone Cloud.")
            refresh = await self.raise_on_error(data)
            if refresh:
                new_url = url.replace(url.split('access_token=', 1)[1], self.cloud.access_token)
                await self.request(method, new_url, json=json)
            return data

    async def raise_on_error(self, data: Dict[str, Any]) -> bool:
        """Check for error message"""
        if isinstance(data, dict) and 'error' in data:
            error = data['error']

            if 'code' in error:
                error_type = error['code']
                try:
                    if error_type == 'INVALID_TOKEN' or error_type == 'AUTHORIZATION_REQUIRED':
                        # Login using existing data
                        response = await self.request_login(self.cloud.login_data)
                        self.cloud.access_token = response['id']
                        return True  # re-run the request
                    else:
                        for type, message in AuthError.items():
                            if type == error_type:
                                raise CrownstoneAuthenticationError(type, message)
                except ValueError:
                    raise CrownstoneUnknownError("Unknown error occurred.")
            else:
                _LOGGER.error(error['message'])

        return False
