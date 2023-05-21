class User:
    _attributes = 'real_name status last_activity email is_admin'.split()

    def update(self, api):
        json = api.get_json(['users', self.id])
        self.update_by_json(json)
