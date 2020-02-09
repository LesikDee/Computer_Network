import multiprocessing as mp
import copy
from typing import Dict
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

class RoutersBase:
    def __init__(self, router_meta: MetaRouter, router_queue):
        self.meta: MetaRouter = copy.deepcopy(router_meta)
        self.queue: mp.Queue = router_queue

class Router:
    def __init__(self, x: float, y: float, max_range: float, id_r: int):
        self.meta = MetaRouter(x, y, max_range, id_r)
        self.queue = mp.Queue()

        self._process = mp.Process(target=self.run_process, args=RoutersBase(self.meta, self.queue))

    @staticmethod
    def add_new_node(
            nodes: Dict[int, MetaRouter],
            new_node: RoutersBase,
            this_router: RoutersBase,
            neighbor_node_queues: Dict[int, mp.Queue],
            graph: Graph
    ):
        vertex_list: Dict[int, float] = {}
        for node in nodes.values():
            dist = new_node.meta.range(node.x, node.y)
            if dist <= new_node.meta.max_range:
                vertex_list[node.id] = dist

        if new_node.meta.range(this_router.meta.x, this_router.meta.y) <= this_router.meta.max_range:
            neighbor_node_queues[new_node.meta.id] = new_node.queue

        nodes[new_node.meta.id] = new_node.meta
        graph.add_vertex(new_node.meta.id, vertex_list)

    @staticmethod
    def run_process(this_router: RoutersBase):
        # initialization
        graph = Graph(this_router.meta.id)
        nodes: Dict[int, MetaRouter] = {this_router.meta.id: this_router.meta}
        neighbor_node_queues: Dict[int, mp.Queue] = {}
        
        while True :
            message: Message = this_router.queue.get()

            if message.type == MessageType.ACK:
                transit_info: ACKMessage = message

                if transit_info.finish_node == this_router.meta.id: # this node is final destination node
                    if nodes.get(transit_info.start_node) is None:
                        Router.add_new_node(nodes, transit_info.router_info, this_router, neighbor_node_queues, graph)

                else:  # this node is just a transit node
                    transit_info.mark(this_router.meta.id)
                    neighbor_node_queues[graph.destination_list[transit_info.finish_node]].put(transit_info)

            elif message.type == MessageType.Add:
                new_node: AddRouterMessage = message

                Router.add_new_node(nodes, new_node.router, this_router, neighbor_node_queues, graph)

                ack = ACKMessage(this_router.meta.id, new_node.router.meta.id, this_router)
                neighbor_node_queues[graph.destination_list[new_node.router.meta.id]].put(ack)


    def start(self):
        self._process.run()

    def terminate(self):
        self._process.terminate()
