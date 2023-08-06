from mjango import settings, exceptions
import os
import requests


class APIKeySettings(settings.SettingsDesc):
    def __set__(self, instance, value):
        try:
            resp = requests.get(
                f'{instance.jstorage_host}/settings', headers={'Content-Type': 'application/json', 'x-api-key': value})
            resp.raise_for_status()
        except requests.HTTPError:
            raise exceptions.SettingsError
        resp = resp.json()
        instance.db_host = resp['db_host']
        instance.db_name = resp['client']
        self._value = value


class StageDesc(settings.SettingsDesc):
    def __set__(self, instance, value):
        if value not in ['stg', 'prod']:
            raise exceptions.SettingsError(
                'stage should be one of [stg, prod]')
        super().__set__(instance, value)


class HostDesc(settings.SettingsDesc):
    def __init__(self, default, default_stg):
        self._value = default
        self._stg_value = default_stg

    def __get__(self, instance, cls):
        if instance.env == 'stg':
            return self._stg_value
        return self._value

    def __set__(self, instance, value):
        if instance.env == 'stg':
            self.set_stg(value)
        else:
            self.set_prod(value)

    def set_stg(self, value):
        self._stg_value = value

    def set_prod(self, value):
        self._value = value


class Settings(settings.Settings):
    env = StageDesc(os.environ.get('REVDB_STAGE', 'stg'))
    api_key = APIKeySettings()
    jstorage_host = HostDesc(
        'https://jstorage.revtel-api.com/v1', 'https://jstorage-stg.revtel-api.com/v1')
    db_host = None
    db_name = None


db_settings = Settings()
