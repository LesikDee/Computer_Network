import time
from src.ospf_net import Net


ORANGE = (255, 150, 100)
WHITE = (255, 255, 255)
ws = 480  # window size


def display(net: Net):
    import pygame
    pygame.init()
    sc = pygame.display.set_mode((ws, ws))
    sc.fill(WHITE)

    font = pygame.font.Font(None, 36)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return

        for router in net.routers.values():
            pygame.draw.circle(sc, ORANGE, (int(router.meta.x * ws), int(router.meta.y * ws)), 20)
            text = font.render(str(router.meta.id), 1, (180, 0, 0))
            sc.blit(text, (int(router.meta.x * ws), int(router.meta.y * ws)))

        pygame.display.update()
        time.sleep(0.2)


if __name__ == "__main__":
    net = Net()
    net.add_router(0.5, 0.5)
    time.sleep(0.2)
    net.add_router(0.5, 0.75)
    net.add_router(0.6, 0.6)
    display(net)
    net.terminate()


