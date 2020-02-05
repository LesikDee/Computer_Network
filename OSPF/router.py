import multiprocessing as mp

class MetaRouter:
    def __init__(self, x: float, y: float, max_range: float, id_r: int):
        self.x = x
        self.y = y
        self.mr = max_range
        self.id = id_r

    def is_in_range(self, x_r2: float, y_r2: float) -> bool:
        return  (self.x - x_r2) ** 2 + (self.y - y_r2) ** 2 < self.mr ** 2


class Router:
    def __init__(self, x: float, y: float, max_range: float, id_r: int):
        self.meta = MetaRouter(x, y, max_range, id_r)
        self.queue = mp.Queue()

        self._process = mp.Process(target=Router.run_process)

    @staticmethod
    def run_process():
        pass

    def start(self):
        self._process.run()

    def terminate(self):
        self._process.terminate()