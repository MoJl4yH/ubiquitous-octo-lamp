
from config import api, get_from_json
from pprint import pprint


class MemorizedInstances:
    def __init__(self):
        self.instances = {}     # {'<Class>': {'<id>': instance}}

    def add(self, instance, yougile_id):
        cls_name = instance.__class__.__name__
        if cls_name not in self.instances:
            self.instances[cls_name] = {}
        self.instances[cls_name][yougile_id] = instance

    def get(self, cls, yougile_id):
        cls_instances = self.instances.get(cls)
        if cls_instances is None:
            return None
        return cls_instances.get(yougile_id)


class Base:
    _attributes = {}            # Base attributes for instance without id (yougile_id)
    _related_attributes = []    # Related attributes is attributes which represents by Instance(Base)
    _path = ''                  # API path without https://yougile.com/api-v2/
    _api = api                  # API instance which can get jsons
    _memorized_instances = MemorizedInstances()     # Struct to contain existed instances

    def __new__(cls, *args, **kwargs):                                  # Create instance or give it from memory
        instance = cls._memorized_instances.get(cls.__name__, args[0])  # Get existed instance or None
        if instance is None:                                            # If instance doesn't exist
            instance = super().__new__(cls)                             # Create new instance by default method
            cls._memorized_instances.add(instance, args[0])             # And add it to existed
            instance.__setattr__('creation', True)                      # Set 'creation' attribute to init
        else:                                                           # If instance exists
            instance.__setattr__('creation', False)                     # Set 'creation' attribute to skip init
        return instance

    def __init__(self, yougile_id):
        if not self.creation:           # 'Creation' is false if we don't need to reinit instance
            return
        self.yougile_id = yougile_id    # Init main attribute to identify instance
        self.init_base_attributes()     # Init base attributes for instance by None

    def init_base_attributes(self):
        for attribute in self._attributes.keys():
            self.__setattr__(attribute, None)

    def fill_by_json(self, json):
        for attribute, cls in self._attributes.items():
            value = get_from_json(json, attribute, self.__class__.__name__)
            if attribute in self._related_attributes:
                self.reload_related(attribute, value, cls)
            else:
                self.__setattr__(attribute, value, cls)

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
        yougile_id = get_from_json(json, 'yougile_id')
        base = cls(yougile_id)
        base.fill_by_json(json)
        return base


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


class BaseList2:
    _base_class = Base

    def __init__(self, instances):
        self.instances = instances[:]

    def __getitem__(self, item):
        return self.instances[item]

    def all(self):
        return self.instances


class BaseDict:
    _base_class = Base

    def __init__(self, instance_list, values_list):
        if len(instance_list) == len(values_list):
            self.instance2value = {instance: value for instance, value in zip(instance_list, values_list)}

    def __setitem__(self, key, value):
        self.instance2value[key] = value

    def __getitem__(self, item):
        return self.instance2value[item]

    def all(self):
        return self.instance2value

    def get(self, index):
        item_by_index = list(self.instance2value.keys())[index]
        return self.instance2value[item_by_index]
