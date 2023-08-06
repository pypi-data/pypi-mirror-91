import requests
from revdb import db_settings, db
from revdb.manager import Manager
from revdb.operators import AND
import copy


class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__

        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        meta_attr = attrs.pop('Meta', None)
        collection = attrs.pop('collection')
        new_class = super_new(cls, name, bases, attrs)

        meta = meta_attr or getattr(new_class, 'Meta', None)
        db_class = meta.db_class
        settings = meta.settings
        new_class.add_to_class('_meta', meta)
        new_class.add_to_class('db', db_class(collection, settings))
        new_class.add_to_class('_collection', collection)
        new_class.add_to_class('_cached_db_meta', None)
        new_class.add_to_class('objects', Manager(new_class))

        return new_class

    def add_to_class(cls, name, attr):
        setattr(cls, name, attr)


class Model(metaclass=ModelBase):
    class Meta:
        db_class = db.JStorage
        settings = db_settings

    def __init__(self, data):
        self._set_db_meta()
        self._data = data

    def __getattr__(self, key):
        return self._data[key]

    def __setattr__(self, name, value):
        _setattr = super().__setattr__
        if name not in self.__dict__ and not name.startswith('_'):
            self._save(name, value)
        else:
            _setattr(name, value)

    @property
    def pk(self):
        self._set_db_meta()
        return self.__class__._cached_db_meta['primary_key']

    def _set_db_meta(self):
        if self.__class__._cached_db_meta is None or self._meta.settings.refresh:
            self.__class__._cached_db_meta = self.db.fetch_meta()

    def _save(self, key, value):
        self._data[key] = value

    def save(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
        return self.db.update(query, self._data)

    def delete(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
        self.db.delete(query)
        del self._data[self.pk]

    def to_json(self):
        return copy.deepcopy(self._data)
