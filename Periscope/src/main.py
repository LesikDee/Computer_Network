from src.geometry import Point3d, Ray, Triangle, Vector
from src.target import Target
from src.periscope import Periscope, Angle, MirrorPos
import pygame
import math
ORANGE = (255, 150, 100)
WHITE = (255, 255, 255)
BLUE = (5, 180, 255)
GREEN = (0, 240, 10)
BLACK = (0, 0, 0)
ws = 800  # window size

CONFIGURE = {
    'start_laser_location': Point3d(0.8, 0.3, 0),
    'start_laser_direction': Vector(Point3d(-1, 0, 0)),
    'down_triangle': [
        Point3d(0.6, 0.2, 0),
        Point3d(0.5, 0.4, 0.2),
        Point3d(0.5, 0.4, -0.2),
    ],
    'up_triangle': [
        Point3d(0.6, 0.6, 0),
        Point3d(0.7, 0.4, 1),
        Point3d(0.7, 0.4, -1),
    ],
}

def to_window_coords(center: Point3d, length_p: int) -> ():
    return int(center.x * ws) -  length_p // 2, int((1 - center.y) * ws) -  length_p // 2, \
           length_p, length_p

def p_to_window_coords(point: Point3d) -> ():
    return int(point.x * ws) , int((1 - point.y) * ws)

def ps_to_window_coords(points: [Point3d]) -> []:
    points_p = []
    for p_i in range(len(points)):
        points_p.append(p_to_window_coords(points[p_i]))
    return points_p

def render(
    sc,
    mirror_down,
    mirror_up,
    p1_intersect,
    p2_intersect,
    p_target,
    p_aim
):
    sc.fill(WHITE)
    pygame.draw.rect(sc, BLACK, to_window_coords(CONFIGURE['start_laser_location'], 40), 6)
    pygame.draw.aalines(sc, BLACK, True, ps_to_window_coords(mirror_down.get_points_list()))
    pygame.draw.aalines(sc, BLACK, True, ps_to_window_coords(mirror_up.get_points_list()))
    pygame.draw.aalines(sc, ORANGE, False,
                        ps_to_window_coords([CONFIGURE['start_laser_location'], p1_intersect, p2_intersect, p_aim]))
    pygame.draw.circle(sc, GREEN, p_to_window_coords(p_target), 15)
    pygame.display.update()

def run():
    pygame.init()
    sc = pygame.display.set_mode((ws, ws))

    periscope = Periscope(CONFIGURE)
    #tee = Target()
    p_target = periscope.ray_to_target().intersect_plane(
        Triangle(Point3d(0.2, 0.5, 0.2),
                 Point3d(0.2, 0.4, 0.1),
                 Point3d(0.2, 0.3, 0.5)
                 ))

    while True:
        mirror_down = periscope.mirror_down
        mirror_up = periscope.mirror_up
        p1_intersect = periscope.laser.intersect_plane(mirror_down.triangle)
        p2_intersect = periscope.laser.reflect_plane(mirror_down.triangle).intersect_plane(mirror_up.triangle)
        p_aim = periscope.ray_to_target().intersect_plane(
        Triangle(Point3d(0.2, 0.5, 0.2),
                 Point3d(0.2, 0.4, 0.1),
                 Point3d(0.2, 0.3, 0.5)
                 ))
        render(sc,  mirror_down,  mirror_up, p1_intersect, p2_intersect, p_target, p_aim)

        pygame.time.delay(100)
        for i in pygame.event.get():
            if i.type == pygame.QUIT: exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    p_target.y += 0.005
                elif i.key == pygame.K_DOWN:
                    p_target.y -= 0.005

                periscope.correct_planes(p_target)


if __name__ == '__main__':
    run()


