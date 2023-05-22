from instances.base import Base, BaseList


class User(Base):
    _attributes = 'real_name status last_activity email is_admin'.split()
    _path = 'users'


class UserList(BaseList):
    _base_class = User
