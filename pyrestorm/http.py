import json as _json
import typing
from datetime import datetime
from logging import getLogger
from pprint import pformat
from typing import Optional

import httpx

if typing.TYPE_CHECKING:
    from .manager import BaseRESTManager

logger = getLogger(__file__)


class HttpExceptionError(Exception):
    pass


class Http(object):
    HTTP_METHODS = ['get', 'post', 'patch', 'put', 'delete']

    def __init__(self, manager: 'BaseRESTManager', debug=False):
        self.manager = manager
        self.debug = debug

    def request(self,
                url: str,
                method: str,
                headers: Optional[dict] = None,
                data: Optional[dict] = None,
                json: Optional[str] = None,
                expected: list = None,
                timeout: int = None,
                **kwargs):

        method = method.lower()
        assert method in self.HTTP_METHODS

        with httpx.Client() as client:
            client_method = getattr(client, method)
            payload = {}

            if headers:
                payload['headers'] = headers
            if data:
                payload['data'] = data
            if json:
                if isinstance(json, str):
                    json = _json.loads(json)
                payload['json'] = json

            if self.debug:
                _payload = pformat(payload)
                logger.info(f'Pyrestorm: call url `{url}` with {_payload}')

            start = datetime.now()
            try:
                response = client_method(url, timeout=timeout, **payload)
            except httpx.TimeoutException as e:
                self.handle_exception(e, duration=(datetime.now() - start).total_seconds())
                raise e

            self.handle_response(response, expected)
            return response

    def handle_exception(self, exception, **kwargs):
        for callback in self.manager.exception_callbacks:
            if callable(callback):
                callback(exception, **kwargs)

    def handle_response(self, response, expected=None):

        for callback in self.manager.response_callbacks:
            if callable(callback):
                callback(response)

        if expected and response.status_code not in expected:
            msg = getattr(response, 'text', '')
            raise HttpExceptionError(f'Invalid response: {response.status_code} {msg}')

    def get(self, url, headers=None, **kwargs):
        return self.request(url, 'get', headers=headers, **kwargs)

    def post(self, url: str, data: dict = None, json: str = None, **kwargs):
        return self.request(url, 'post', data=data, json=json, **kwargs)

    def patch(self, url: str, data: dict = None, json: str = None, **kwargs):
        return self.request(url, 'patch', data=data, json=json, **kwargs)

    def put(self, url: str, data: dict = None, json: str = None, **kwargs):
        return self.request(url, 'put', data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request(url, 'delete', **kwargs)
