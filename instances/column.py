from instances.base import Base
from instances.board import Board


class Column(Base):
    _attributes = {
        'board': Board,
        'color': int,
        'title': str
    }
    _path = 'columns'

    def __str__(self):
        return f'<Column: {self.title}>'

    def __repr__(self):
        return f'<Column: {self.title}>'
