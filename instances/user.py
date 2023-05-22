from instances.base import Base, BaseList


class User(Base):
    _attributes = 'real_name status last_activity email is_admin'.split()

    def update(self, api):
        json = api.get_json(['users', self.yougile_id])
        self.update_by_json(json)


class UserList(BaseList):
	_base_class = User
