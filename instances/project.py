from instances.base import Base


class Project(Base):
	_attributes = 'timestamp title users'.split()
	_related_attributes = ['users']

	def update(self, api):
		json = api.get_json(['projects', self.yougile_id])
		self.update_by_json(json)
