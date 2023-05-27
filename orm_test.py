from pprint import pprint as pp
from yougile_api import YougileAPI
from instances.user import User
from instances.project import Project
from instances.task import Task
import os


def main():
	api = YougileAPI(os.environ.get('KEY_API_YOUGILE'))
	# pp(api.get_users()[0])
	# pp(api.get_projects()[0])
	# pp(api.get_boards()[0])
	# pp(api.get_columns()[0])
	# pp(api.get_tasks()[0])

	# u = User('cf86057a-88ff-4a6b-9800-8670de247d33')
	# u.reload()
	# pp(u.__dict__)

	# p = Project('a6729c93-1d30-4fec-b4c4-a0bee00d71c4')
	# p.reload()
	# pp(p.__dict__)

	task = Task('00dbd904-0ba0-4f0b-a1c5-6fca3ea0dd0c')
	task.reload()
	pp(task.__dict__)


if __name__ == '__main__':
	main()
