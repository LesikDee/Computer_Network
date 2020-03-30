from geometry import Point3d, Ray, Triangle, Vector
from target import Target
from mirror import Mirror

ORANGE = (255, 150, 100)
WHITE = (255, 255, 255)
BLUE = (5, 180, 255)
GREEN = (0, 240, 10)
BLACK = (0, 0, 0)
ws = 480  # window size

CONFIGURE = {
    'start_laser_location': Point3d(0.8, 0.3, 0),
    'start_laser_direction': Vector(Point3d(-1, 0, 0)),
    'down_triangle': [
        Point3d(0.6, 0.2, 0),
        Point3d(0.4, 0.4, 0.2),
        Point3d(0.4, 0.4, -0.2),
    ],
    'up_triangle': [
        Point3d(0.6, 0.6, 0),
        Point3d(0.8, 0.4, 1),
        Point3d(0.8, 0.4, -1),
    ],
}

if __name__ == '__main__':

    import pygame
    pygame.init()
    sc = pygame.display.set_mode((ws, ws))
    sc.fill(WHITE)
    radius_size = 20

    laser: Ray = Ray(CONFIGURE['start_laser_location'], CONFIGURE['start_laser_direction'])
    points3 = CONFIGURE['down_triangle']
    mirror_down = Mirror(Triangle(points3[0], points3[1], points3[2]))
    points3 = CONFIGURE['up_triangle']
    mirror_up = Mirror(Triangle(points3[0], points3[1], points3[2]))

    Ray_to_target = laser.reflect_plane(mirror_down.triangle).reflect_plane(mirror_up.triangle)
    #tee = Target()

