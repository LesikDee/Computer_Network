import time
import src.cmd_parser as parser
import multiprocessing as mp
from queue import Empty
from src.actions import *

ORANGE = (255, 150, 100)
WHITE = (255, 255, 255)
ws = 480  # window size


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def display(display_queue: mp.Queue):
    import pygame
    pygame.init()
    sc = pygame.display.set_mode((ws, ws))
    sc.fill(WHITE)

    font = pygame.font.Font(None, 36)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return

        try:
            routers_meta_list: list = display_queue.get(timeout=0.25)
            for meta in routers_meta_list:
                pygame.draw.circle(sc, ORANGE, (int(meta.x * ws), int(meta.y * ws)), 20)
                text = font.render(str(meta.id), 1, (180, 0, 0))
                sc.blit(text, (int(meta.x * ws), int(meta.y * ws)))
        except Empty:
            pass

        pygame.display.update()


def run(main_process_queue: mp.Queue):
    net = Net()
    display_queue = mp.Queue()  # for update display
    display_process = mp.Process(target=display, args=(display_queue,))
    display_process.start()

    while True:
        action: Action = main_process_queue.get()
        if action.actionType == ActionType.Exit:
            break

        action.start(net)
        routers_meta_list = []
        for router in net.routers.values():
            routers_meta_list.append(router.meta)

        display_queue.put(routers_meta_list)

    display_process.terminate()
    net.terminate()


if __name__ == "__main__":
    main_process_queue = mp.Queue()
    main_process = mp.Process(target=run, args=(main_process_queue,))
    main_process.start()

    time.sleep(2)

    while True:
        action = parser.cmd_parse()

        if action.actionType != ActionType.None_:
            main_process_queue.put(action)

        if action.actionType == ActionType.Exit:
            break

    main_process.join()




