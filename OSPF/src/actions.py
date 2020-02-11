from enum import Enum
from src.ospf_net import Net


class ActionType(Enum):
    None_ = 0
    Add = 1
    Exit = 2


class Action:
    def __init__(self):
        self.actionType: ActionType = ActionType.None_

    def start(self, net: Net):
        pass


class AddAction(Action):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.actionType = ActionType.Add
        self.x = x
        self.y = y

    def start(self, net: Net):
        net.add_router(self.x, self.y)


class ExitAction(Action):
    def __init__(self):
        super().__init__()
        self.actionType = ActionType.Exit
