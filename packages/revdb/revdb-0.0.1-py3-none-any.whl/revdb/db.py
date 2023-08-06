from revdb import db_settings, exceptions, operators
import requests


class JStorageBase:
    def __init__(self, collection, settings=None):
        self.collection = collection
        self.settings = settings or db_settings

    @property
    def api_key(self):
        if not self.settings.api_key:
            raise exceptions.SettingsError
        return self.settings.api_key

    @property
    def db_host(self):
        return self.settings.jstorage_host

    def _build_headers(self, **kwargs):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            **kwargs
        }

    def _requests(self, method, path, data):
        headers = self._build_headers()
        url = f'{self.db_host}/document/{self.collection}/{path}'
        try:
            resp = requests.request(method, url, json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as err:
            response = err.response
            status_code = response.status_code
            if status_code >= 500:
                detail = 'internal server error'
            else:
                detail = response.json()['code']
            raise exceptions.ServiceError(detail)

    def filter(self, query):
        resp = self._requests('post', 'find', {'query': query})
        return resp

    def get(self, query):
        resp = self._requests('post', 'find-one', {'query': query})
        return resp

    def create(self, **kwargs):
        resp = self._requests('post', 'create', {'data': kwargs})
        return resp

    def delete(self, query):
        resp = self._requests('post', 'find-one/delete', {'query': query})
        return resp

    def update(self, query, data):
        resp = self._requests('post', 'update', {'query': query, 'data': data})
        return resp

    def fetch_meta(self):
        headers = self._build_headers()
        url = f'{self.db_host}/collection/{self.collection}/detail'
        resp = requests.get(url, headers=headers)
        return resp.json()


class Compiler:
    def create(self, **kwargs):
        raise NotImplementedError('create() should be implement')

    def filter(self, query):
        raise NotImplementedError('filter() should be implement')

    def update(self, query, data):
        raise NotImplementedError('update() should be implement')

    def delete(self, query):
        raise NotImplementedError('delete() should be implement')

    def fetch_meta(self):
        raise NotImplementedError('fetch_meta() should be implement')


class JStorage(Compiler):
    def __init__(self, collection, settings=None):
        self.db_base = JStorageBase(collection, settings)

    def create(self, **kwargs):
        return self.db_base.create(**kwargs)

    def filter(self, query):
        params = query.to_represent()
        return self.db_base.filter(params)

    def update(self, query, data):
        params = query.to_represent()
        return self.db_base.update(query=params, data=data)

    def delete(self, query):
        params = query.to_represent()
        return self.db_base.delete(params)

    def fetch_meta(self):
        return self.db_base.fetch_meta()

    def all(self):
        return self.db_base.filter({})

    def get(self, query):
        params = query.to_represent()
        return self.db_base.get(params)
