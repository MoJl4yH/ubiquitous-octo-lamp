from config import api


class MetaBase(type):
    def __new__(mcls, name, bases, attrs):
        for name in attrs.get('_attributes', ()):
            attrs[name] = 0
        return type.__new__(mcls, name, bases, attrs)


json_attributes_to_instance_variable = {
    'id': 'yougile_id',
}


class Base(metaclass=MetaBase):
    _attributes = []
    _related_attributes = []
    _path = ''
    _api = api

    def __init__(self, yougile_id):
        self.yougile_id = yougile_id

    def update_by_json(self, json):
        self.yougile_id = json['id']
        for attr in self._attributes:
            if attr in self._related_attributes:
                self.update_related(attr, json[attr])
            else:
                self.__setattr__(attr, json[to_camel_case(attr)])

    def update_related(self, related_attr, value):
        ...
        # cls = attribute2class(related_attr)
        # if isinstance(value, dict):
        #     ...


    def update(self):
        json = self._api.get_json([self._path, self.yougile_id])
        self.update_by_json(json)
            
    @classmethod
    def from_json(cls, json):
        base = cls('')
        base.update_by_json(json)
        return base


def to_camel_case(name):
    first, *others = name.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


class BaseList:
    _base_class = Base

    def __init__(self):
        self.instance_attributes = {}

    def all(self):
        return self.instance_attributes.keys()

    def add(self, instance, attributes=None):
        if not isinstance(instance, self._base_class):
            instance = self._base_class.from_json(instance)
        self.instance_attributes[instance] = attributes
