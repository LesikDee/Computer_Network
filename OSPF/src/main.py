import time
import src.cmd_parser as parser
import multiprocessing as mp
from queue import Empty
from src.actions import *

ORANGE = (255, 150, 100)
WHITE = (255, 255, 255)
ws = 480  # window size


def display(display_queue: mp.Queue):
    import pygame
    pygame.init()
    sc = pygame.display.set_mode((ws, ws))
    sc.fill(WHITE)
    radius_size = 20
    font = pygame.font.Font(None, 36)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return

        try:
            routers_meta_list: list = display_queue.get(timeout=0.25)
            print(len(routers_meta_list))
            for meta in routers_meta_list:
                pygame.draw.circle(sc, ORANGE, (int(meta.x * ws), int(meta.y * ws)), radius_size)
                text = font.render(str(meta.id), 1, (180, 0, 0))
                sc.blit(text, (int(meta.x * (ws -  radius_size // 2)), int(meta.y * (ws -  radius_size // 2))))
        except Empty:
            pass

        pygame.display.update()


if __name__ == "__main__":
    net = Net()
    display_queue = mp.Queue()  # for update display
    display_process = mp.Process(target=display, args=(display_queue,))
    display_process.start()
    time.sleep(2)
    while True:
        action: Action = parser.cmd_parse()
        if action.actionType == ActionType.Exit:
            break

        print('aaaaa')
        action.start(net)
        print('bbbbb')
        routers_meta_list = []
        for router in net.routers.values():
            routers_meta_list.append(router.meta)

        print(action.actionType, routers_meta_list)

        display_queue.put(routers_meta_list)

    display_process.terminate()
    net.terminate()

