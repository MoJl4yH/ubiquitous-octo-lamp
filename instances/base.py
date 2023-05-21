class MetaBase(type):
    def __new__(mcls, name, bases, attrs):
        for name in attrs.get('_attributes', ()):
            attrs[name] = 0
        return type.__new__(mcls, name, bases, attrs)


class Base(metaclass=MetaBase):
    _attributes = []

    def __init__(self, yougile_id):
        self.yougile_id = yougile_id

    def update_by_json(self, json):
        self.yougile_id = json['id']
        for attr in self._attributes:
            self.__setattr__(attr, json[to_camel_case(attr)])

    @classmethod
    def from_json(cls, json):
        base = cls('')
        base.update_by_json(json)
        return base


def to_camel_case(name):
    first, *others = name.split('_')
    return ''.join([first.lower(), *map(str.title, others)])
