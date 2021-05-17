import json as _json
from logging import getLogger
from typing import Optional

import httpx
from pprint import pformat
logger = getLogger(__file__)


class HttpExceptionError(Exception):
    pass


class Http(object):
    HTTP_METHODS = ['get', 'post', 'patch', 'put', 'delete']

    def __init__(self, debug=False):
        self.debug = debug

    def request(self,
                url: str,
                method: str,
                headers: Optional[dict] = None,
                data: Optional[dict] = None,
                json: Optional[str] = None,
                expected: list = None,
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

            r = client_method(url, **payload)

            if expected and r.status_code not in expected:
                raise HttpExceptionError(f'Invalid response: {r.status_code}')

            return r

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
