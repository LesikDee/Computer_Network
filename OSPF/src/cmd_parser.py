from src.actions import *

def form_action(args):
    name = args[0]
    if name == 'add':
        return AddAction(float(args[1]), float(args[2]))
    elif name == 'scenario':
        scenario_names ={
            'circle': ScenarioCircle,
            'polygon': ScenarioPolygon,
            'mill': ScenarioMill
        }

        if args[1] not in scenario_names.keys():
            print('Wrong command, print \"help\" for information')
            return Action()

        return scenario_names[args[1]]()

    if name == 'ping':
        return PingAction(int(args[1]), int(args[2]))
    elif name == 'exit':
        return ExitAction()


def parse_args(args: list):
    commands = {
        'scenario': 1,
        'ping': 2,
        'add': 2,
        'help': 0,
        'exit': 0
    }

    command = args[0]
    if command not in commands.keys():
        print('Wrong command, print \"help\" for information')
        return Action()

    action_info = commands.get(command)
    if len(args) - 1 != action_info:
        print('Wrong parameters number, print \"help\" for information')
        return Action()

    return form_action(args)


def cmd_parse(str_action: str):
    try:
        action = parse_args(str_action.strip('\n').split(' '))
        return action

    except SystemExit:
        pass
