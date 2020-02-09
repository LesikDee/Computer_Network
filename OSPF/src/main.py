# import pygame
import time
from src.ospf_net import Net


ORANGE = (255, 150, 100)

ws = 480  # window size
WHITE = (255, 255, 255)


# def display(net: Net):
#     pygame.init()
#     sc = pygame.display.set_mode((ws, ws))
#     sc.fill(WHITE)
#
#     while True:
#
#         for i in pygame.event.get():
#             if i.type == pygame.QUIT:
#                 return
#
#         for router in net.routers.values():
#             pygame.draw.circle(sc, ORANGE, (int(router.meta.x * ws), int(router.meta.y * ws)), 20)
#
#         pygame.display.update()
#         time.sleep(0.2)


if __name__ == "__main__":
    net = Net()
    net.add_router(0.5, 0.5)
    net.add_router(0.5, 0.75)
    # display(net)
