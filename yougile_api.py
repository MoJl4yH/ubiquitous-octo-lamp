import requests


class YougileAPI:
    BASE_URL = r"https://cazi.yougile.com/api-v2"

    def __init__(self, api_key):
        self.header = {"Content-Type": "application/json",
                       "Authorization": "Bearer " + api_key}

    def get_json(self, instance_path, query_params=None):
        if isinstance(instance_path, list):
            url = '/'.join([self.BASE_URL] + instance_path)
        else:
            url = f'{self.BASE_URL}/{instance_path}'
        return requests.get(url, headers=self.header, params=query_params, timeout=5).json()

    def get_users(self):
        return self.get_json('users').get('content')

    def get_projects(self):
        return self.get_json('projects').get('content')

    def get_boards(self):
        return self.get_json('boards').get('content')

    def get_columns(self):
        return self.get_json('columns').get('content')

    def get_tasks(self):
        return self.get_json('tasks').get('content')


if __name__ == '__main__':
    from instances.base import Base

    class User(Base):
        _attributes = 'real_name status last_activity email is_admin'.split()

        def update(self, api):
            json = api.get_json(['users', self.yougile_id])
            self.update_by_json(json)

    api = YougileAPI('api_key_here')

    user = User('cf86057a-88ff-4a6b-9800-8670de247d33')
    user.update(api)
    print('aboba')
