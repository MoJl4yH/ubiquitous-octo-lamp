from instances.base import Base
from instances.column import Column
from instances.user import User
from datetime import datetime


class Task(Base):
    _attributes = {
        'archived': bool,
        'column': Column,
        'completed': bool,
        'created_by': User,
        'timestamp': (datetime.fromtimestamp, lambda miliseconds: miliseconds / 1000),
        'title': str
    }
    _path = 'tasks'

    def __str__(self):
        return f'<Task: {self.title}>'

    def __repr__(self):
        return f'<Task: {self.title}>'
