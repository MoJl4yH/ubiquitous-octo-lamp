from instances.base import Base
from instances.project import Project


class Board(Base):
    _attributes = {
        'project':  Project,
        'title':    str
    }
    _path = 'boards'

    def __str__(self):
        return f'<Board: {self.title}>'

    def __repr__(self):
        return f'<Board: {self.title}>'
