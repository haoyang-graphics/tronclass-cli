from argparse import ArgumentParser

from tronclass_cli.command.root import RootCommand
from tronclass_cli.command.todo import TodoCommand
from tronclass_cli.command.courses import CoursesCommand, CoursesListCommand
from tronclass_cli.command.homework import HomeworkCommand, HomeworkListCommand
from tronclass_cli.command.activities import ActivitiesCommand, ActivitiesListCommand
from tronclass_cli.middleware import Context
from tronclass_cli.utils import interact

parser = ArgumentParser()
root_command = RootCommand(parser, Context())
root_command.add_sub_command('todo', TodoCommand, aliases=['t', 'td'], help='view to-do list')

courses_command = root_command.add_sub_command('courses', CoursesCommand, aliases=['c'])
courses_command.add_sub_command('list', CoursesListCommand, aliases=['l', 'ls'], help='list courses')

activities_command = root_command.add_sub_command('activities', ActivitiesCommand, aliases=['a'])
activities_command.add_sub_command('list', ActivitiesListCommand, aliases=['l', 'ls'], help='list activities')

homework_command = root_command.add_sub_command('homework', HomeworkCommand, aliases=['h', 'hw'])
homework_command.add_sub_command('list', HomeworkListCommand, aliases=['l', 'ls'], help='list homework')


def main():
    args = root_command.parse_args()
    try:
        args.__middleware.exec(args)
        args.__middleware.dispose()
    except Exception as ex:
        interact.error(f'fatal: {ex}')
        raise


if __name__ == '__main__':
    main()
