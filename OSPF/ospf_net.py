from server import Server
from router import Router

class Net:
    def __init__(self):
        self._server = Server()
        self.routers = {}
        self._max_id = 0

    def add_router(self, x, y):
        new_router = Router(x, y, 0.2, self._max_id)

        self.routers[self._max_id] = new_router
        self._max_id += 1

        self._server.turn_on_router(new_router)

    def delete_router(self):
        pass
