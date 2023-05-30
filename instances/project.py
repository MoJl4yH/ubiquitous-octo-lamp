from instances.base import Base
from instances.user import UserList, UsersDict
from datetime import datetime


class Project(Base):
    _attributes = {'timestamp': (datetime.fromtimestamp, lambda militime: militime/1000),
                   'title': 	str,
                   'users': 	UsersDict.from_id_and_attribute}
    _path = 'projects'

    def __str__(self):
        return f'<Project: {self.title}>'

    def __repr__(self):
        return f'<Project: {self.title}>'
