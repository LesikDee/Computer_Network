from src.server import Server
from src.router import Router
import multiprocessing as mp


class Net:
    MAX_ROUTERS_COUNT = 15
    ROUTERS_RANGE = 0.35

    def __init__(self):

        self.routers = {}
        self._max_id = 0
        self.id_free_list = [True] * self.MAX_ROUTERS_COUNT
        self.queue_list = [mp.Queue()] * self.MAX_ROUTERS_COUNT
        self._server = Server(self.queue_list)

    def add_router(self, x, y):
        new_router = Router(x, y, self.ROUTERS_RANGE, self._max_id, self.queue_list)

        self.routers[self._max_id] = new_router
        self._max_id += 1

        self._server.turn_on_router(new_router)

    def delete_router(self):
        pass
