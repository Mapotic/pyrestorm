from pydantic import BaseModel

from .http import Http


class BaseRESTManager(object):

    def __init__(self, base_url, debug=False):
        self.debug = debug
        self.base_url = base_url
        self.http = Http(debug=debug)

    ###################################
    # C
    ###################################

    def create_url(self):
        return f'{self.base_url}'

    def create(self, obj: BaseModel, url: str = None, expected=(201,), **kwargs):
        url = url or self.create_url()
        return self.http.post(url, json=obj.json(), expected=expected, **kwargs)

    ###################################
    # R
    ###################################

    def get_url(self, id):
        return f'{self.base_url}{id}/'

    def get(self, id, expected=(200,), **kwargs):
        return self.http.get(self.get_url(id), expected=expected, **kwargs)

    def list_url(self):
        return f'{self.base_url}'

    def list(self, expected=(200,), **kwargs):
        # TODO: filtering
        return self.http.get(self.list_url(), expected=expected, **kwargs)

    ###################################
    # U
    ###################################

    def patch_url(self, id):
        return self.get_url(id)

    def patch(self, obj: BaseModel, id=None, url: str = None, expected=(200,), **kwargs):
        url = url or self.patch_url(id)
        return self.http.patch(url, json=obj.json(), expected=expected, **kwargs)

    def put_url(self, id):
        return self.get_url(id)

    def put(self, obj: BaseModel, id=None, url: str = None, expected=(200,), **kwargs):
        url = url or self.put_url(id)
        return self.http.put(url, json=obj.json(), expected=expected, **kwargs)

    ###################################
    # D
    ###################################

    def delete_url(self, id):
        return self.get_url(id)

    def delete(self, id=None, url: str = None, expected=(204,), **kwargs):
        url = url or self.delete_url(id)
        return self.http.delete(url, expected=expected, **kwargs)

    ###################################
    ###################################

    @property
    def model(self):
        raise NotImplementedError()
