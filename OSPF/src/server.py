from src.router import Router, RoutersBase
from typing import Dict
from src.messages import AddRouterMessage, Message

class Server:


    def __init__(self):
        self.routers_info: Dict[int, RoutersBase] = {}

    def turn_on_router(self, router: Router):
        router.start()  # Run the process

        new_router_info = RoutersBase(router.meta, router.queue)

        for machine in self.routers_info.values():
            curr_router: RoutersBase = machine
            message: Message = AddRouterMessage(new_router_info)
            curr_router.queue.put(message)


        self.routers_info[router.meta.id] = new_router_info

    def turn_out_router(self):
        pass
# if router.meta.is_in_range(curr_router.rm.x, curr_router.rm.y):