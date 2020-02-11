from src.actions import *


def form_action(args):
    name = args[0]
    if name == 'add':
        return AddAction(float(args[1]), float(args[2]))
    elif name == 'exit':
        return ExitAction()


def parse_args(args: list):
    commands = {
        'add': 2,
        'exit': 0
    }

    command = args[0]
    if command not in commands.keys():
        print('error 1')
        return Action()

    action_info = commands.get(command)
    if len(args) - 1 != action_info:
        print('error 2')
        return Action()

    return form_action(args)


def cmd_parse():

    import sys

    str_action = sys.stdin.readline().strip('\n').split(' ')
    try:
        return parse_args(str_action)
    except SystemExit:
        pass

