import multiprocessing as mp
from typing import Dict, List
from src.ospf_graph import Graph
from src.messages import *


class MetaRouter:
    def __init__(self, x: float, y: float, max_range: float, id_r: int):
        self.x = x
        self.y = y
        self.max_range = max_range
        self.id = id_r

    def range(self, x_r2: float, y_r2: float) -> float:
        return ((self.x - x_r2) ** 2 + (self.y - y_r2) ** 2) ** 0.5


class Router:
    def __init__(self, x: float, y: float, max_range: float, id_r: int, queue_list: []):
        self.meta = MetaRouter(x, y, max_range, id_r)

        self._process = mp.Process(target=self.run_process, args=(self.meta, queue_list))

    @staticmethod
    def add_new_node(
            nodes: Dict[int, MetaRouter],
            new_node: MetaRouter,
            new_node_queue: mp.Queue,
            this_router_meta: MetaRouter,
            neighbor_node_queues: Dict[int, mp.Queue],
            graph: Graph
    ):
        vertex_list: Dict[int, float] = {}
        for node in nodes.values():
            dist = new_node.range(node.x, node.y)
            if dist <= new_node.max_range:
                vertex_list[node.id] = dist

        if new_node.range(this_router_meta.x, this_router_meta.y) <= this_router_meta.max_range:
            neighbor_node_queues[new_node.id] = new_node_queue

        nodes[new_node.id] = new_node
        graph.add_vertex(new_node.id, vertex_list)

    @staticmethod
    def run_process(this_router_meta: MetaRouter, queue_list: List[mp.Queue]):
        # initialization
        this_router_queue = queue_list[this_router_meta.id]
        graph = Graph(this_router_meta.id)
        nodes: Dict[int, MetaRouter] = {this_router_meta.id: this_router_meta}
        neighbor_node_queues: Dict[int, mp.Queue] = {}
        print('router ' + str(this_router_meta.id) + ' runs')
        while True:
            message: Message = this_router_queue.get()

            if message.type == MessageType.ACK:
                transit_info: ACKMessage = message

                if transit_info.finish_node == this_router_meta.id:  # this node is final destination node
                    if nodes.get(transit_info.start_node) is None:
                        Router.add_new_node(nodes, transit_info.router_info, queue_list[transit_info.router_info.id],
                                            this_router_meta, neighbor_node_queues, graph)

                else:  # this node is just a transit node
                    transit_info.mark(this_router_meta.id)
                    print(transit_info.finish_node)
                    queue_list[graph.destination_list[transit_info.finish_node]].put(transit_info)

            elif message.type == MessageType.Add:
                new_node: AddRouterMessage = message

                Router.add_new_node(nodes, new_node.router_info, queue_list[new_node.router_info.id],
                                    this_router_meta, neighbor_node_queues, graph)

                ack = ACKMessage(this_router_meta.id, new_node.router_info.id, this_router_meta)
                queue_list[graph.destination_list[new_node.router_info.id]].put(ack)

    def start(self):
        self._process.start()

    def terminate(self):
        self._process.terminate()


if __name__ == "__main__":
    d = [mp.Queue(), mp.Queue(), mp.Queue()]
    r0 = Router(0.5, 0.5, 0.4, 0, d)
    r0.start()
    import time
    time.sleep(0.2)
    r1 = Router(0.5, 0.8, 0.4, 1, d)
    r1.start()
    mes = AddRouterMessage(r1.meta)
    d[r0.meta.id].put(mes)

    r2 = Router(0.6, 0.6, 0.4, 2, d)
    r2.start()
    mes = AddRouterMessage(r2.meta)
    d[r0.meta.id].put(mes)
    d[r1.meta.id].put(mes)
