from instances.base import Base


class Project(Base):
	_attributes = 'timestamp title users'.split()
	_related_attributes = ['users']
	_path = 'projects'
