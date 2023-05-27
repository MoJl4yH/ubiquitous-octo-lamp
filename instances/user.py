from instances.base import Base, BaseList


class User(Base):
    _attributes = {'real_name':     str,
                   'status':        str,
                   'last_activity': str,
                   'email':         str,
                   'is_admin':      bool}
    _path = 'users'

    def __str__(self):
        return f"<User: {self.email}>"

    def __repr__(self):
        return f"<User: {self.email}>"


class UserList(BaseList):
    _base_class = User
