from router import Router, MetaRouter
import multiprocessing as mp
from typing import Dict

class Server:
    class RoutersBase:
        def __init__(self, router_meta, router_queue):
            self.rm: MetaRouter = router_meta
            self.queue: mp.Queue = router_queue

    def __init__(self):
        self.routers_info: Dict [int, Server.RoutersBase] = {}

    def turn_on_router(self, router: Router):
        for machine in self.routers_info.values():
            curr_router: Server.RoutersBase = machine
            if router.meta.is_in_range(curr_router.rm.x, curr_router.rm.y):
                curr_router.queue.put(router)
            else:
                curr_router.queue.put(router.meta)

        new_router_info = Server.RoutersBase(router.meta, router.queue)
        self.routers_info[router.meta.id] = new_router_info

    def turn_out_router(self):
        pass