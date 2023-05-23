import os
from yougile_api import YougileAPI

api = YougileAPI(os.environ.get('KEY_API_YOUGILE'))

instance_variable_to_json_attributes = {
    'yougile_id': 'id',
    'Board': {
        'project': 'projectId'
    },
    'Column': {
        'board': 'boardId'
    },
    'Task': {
        'column': 'columnId'
    }
}


def get_from_json(json, attr, cls=None):
    translator = instance_variable_to_json_attributes

    if cls and cls in translator.keys():
        translator = translator[cls]

    if attr in translator.keys():
        attr = translator[attr]
    else:
        attr = to_camel_case(attr)

    return json[attr]


def to_camel_case(name):
    first, *others = name.split('_')
    return ''.join([first.lower(), *map(str.title, others)])
