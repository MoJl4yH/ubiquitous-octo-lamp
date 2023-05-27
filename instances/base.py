from config import api, get_from_json
from pprint import pprint


class Base:
    _attributes = {}
    _related_attributes = []
    _path = ''
    _api = api

    def __init__(self, yougile_id):
        self.yougile_id = yougile_id
        for attribute in self._attributes.keys():
            self.__setattr__(attribute, None)

    def fill_by_json(self, json):
        for attribute, cls in self._attributes.items():
            if attribute in self._related_attributes:
                self.reload_related(attribute, get_from_json(json, attribute, self.__class__.__name__), cls)
            else:
                self.__setattr__(attribute, get_from_json(json, attribute, self.__class__.__name__), cls)

    def __setattr__(self, key, value, cls=None):
        if cls:
            instance = None
            if isinstance(cls, tuple):
                initializer, converter = cls
                instance = initializer(converter(value))
            else:
                instance = cls(value)
            if 'reload' in dir(instance):
                instance.reload()
            self.__dict__[key] = instance
        else:
            super().__setattr__(key, value)

    def reload_related(self, related_attr, value, cls):
        if isinstance(value, str):
            self.__setattr__(related_attr, value, cls)
        else:
            instance_list = cls()
            for yougile_id, attributes in value.items():
                instance = cls._base_class(yougile_id)
                instance.reload()
                instance_list.add(instance, attributes)
            self.__setattr__(related_attr, instance_list)

    def reload(self):
        json = self._api.get_json([self._path, self.yougile_id])
        self.fill_by_json(json)
            
    @classmethod
    def from_json(cls, json):
        base = cls('')
        base.fill_by_json(json)
        return base


def to_camel_case(name):
    first, *others = name.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


class BaseList:
    _base_class = Base

    def __init__(self):
        self.instance_and_attributes = {}   # добавить дикт сохраняющий последовательность

    def all(self):
        return list(self.instance_and_attributes.keys())

    def add(self, instance_or_json, attributes=None):
        if isinstance(instance_or_json, self._base_class):
            instance = instance_or_json
        else:
            instance = self._base_class.from_json(instance_or_json)
        self.instance_and_attributes[instance] = attributes

    def get(self, index):
        item_by_index = list(self.instance_and_attributes.keys())[index]
        return self.instance_and_attributes[item_by_index]

    def __getitem__(self, item):
        return self.instance_and_attributes[item]
