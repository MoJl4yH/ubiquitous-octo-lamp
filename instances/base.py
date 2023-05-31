
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

    def fill_by_json(self, json, reload_related=True):
        for attribute, class_creator in self._attributes.items():
            value = get_from_json(json, attribute, self.__class__.__name__)
            instance = self.related_instance_initializer(class_creator, value)
            
            if reload_related and 'reload' in dir(instance):
                instance.reload()
            
            self.__setattr__(attribute, instance)

    @staticmethod
    def related_instance_initializer(class_creator, value):
        instance = None
        if isinstance(class_creator, tuple):
            initializer, converter = class_creator
            instance = initializer(converter(value))
        else:
            instance = class_creator(value)
        return instance

    def reload(self, reload_related=True):
        json = self._api.get_json([self._path, self.yougile_id])
        self.fill_by_json(json, reload_related)
            
    @classmethod
    def from_json(cls, json, reload_related=True):
        yougile_id = get_from_json(json, 'yougile_id')
        base = cls(yougile_id)
        base.fill_by_json(json, reload_related=True)
        return base


class BaseList:
    _base_class = Base

    def __init__(self, instances):
        self.instances = instances[:]

    def append(self, instance):
        if isinstance(instance, self._base_class):
            raise TypeError
        self.instances.append(instance)

    def __getitem__(self, item):
        return self.instances[item]

    def all(self):
        return self.instances

    @classmethod
    def from_id_list(cls, id_list):
        instance_list = []
        for yougile_id in id_list:
            instance = cls._base_class(yougile_id)
            instance.reload()
            instance_list.append(instance)
        return cls(instance_list)


class BaseDict:
    _base_class = Base

    def __init__(self, instance_list, value_list):
        if len(instance_list) == len(value_list):
            self.instance2value = {instance: value for instance, value in zip(instance_list, value_list)}

    def __setitem__(self, key, value):
        self.instance2value[key] = value

    def __getitem__(self, item):
        return self.instance2value[item]

    def all(self):
        return self.instance2value

    def get(self, index):
        item_by_index = list(self.instance2value.keys())[index]
        return self.instance2value[item_by_index]

    @classmethod
    def from_id_and_attribute(cls, id_and_attribute):
        instance_list = [cls._base_class(yougile_id) for yougile_id in id_and_attribute.keys()]
        [instance.reload() for instance in instance_list]
        value_list = id_and_attribute.values()
        return cls(instance_list, value_list)


