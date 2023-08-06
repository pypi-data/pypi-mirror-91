import os
from revdb import exceptions


class SettingsDesc:
    def __init__(self, default):
        self._value = default

    def __get__(self, instance, cls):
        return self._value

    def __set__(self, instance, value):
        self._value = value
        instance.refresh = True


class StageDesc(SettingsDesc):
    def __set__(self, instance, value):
        if value not in ['stg', 'prod']:
            raise exceptions.SettingsError(
                'stage should be one of [stg, prod]')
        super().__set__(instance, value)


class HostDesc(SettingsDesc):
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

        instance.refresh = True

    def set_stg(self, value):
        self._stg_value = value

    def set_prod(self, value):
        self._value = value


class Settings:
    env = StageDesc(os.environ.get('REVDB_STAGE', 'stg'))
    jstorage_host = HostDesc(
        'https://jstorage.revtel-api.com/v1', 'https://jstorage-stg.revtel-api.com/v1')
    api_key = SettingsDesc(os.environ.get('REVDB_API_KEY', None))
    refresh = False


db_settings = Settings()
