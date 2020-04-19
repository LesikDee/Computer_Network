from src.geometry import Point3d,Triangle
from src.system.periscope import Periscope
import pygame
import src.parser as parser
from src.render import Renderer
from src.target import Target

def run():
    pygame.init()
    config = parser.parse('2d')
    periscope = Periscope(config)
    renderer = Renderer(periscope)

    p_target = periscope.ray_to_target().intersect_plane(
        Triangle(Point3d(0.2, 0.5, 0.2),
                 Point3d(0.2, 0.4, 0.1),
                 Point3d(0.2, 0.3, 0.5)
                 ))
    tee = Target(p_target, config["target_radius"])

    iteration = 0
    while True:
        mirror_down = periscope.mirror_down
        mirror_up = periscope.mirror_up
        p1_intersect = periscope.laser.intersect_plane(mirror_down.triangle)
        p2_intersect = periscope.laser.reflect_plane(mirror_down.triangle).intersect_plane(mirror_up.triangle)
        p_aim = periscope.ray_to_target().intersect_plane(
            Triangle(Point3d(tee.location.x, 0.5, 0.2),
            Point3d(tee.location.x, 0.4, 0.1),
            Point3d(tee.location.x, 0.3, 0.5)
        ))

        renderer.render(p1_intersect, p2_intersect, tee, p_aim)

        pygame.time.delay(10)
        for i in pygame.event.get():
            if i.type == pygame.QUIT: exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    tee.location.y += 0.01
                elif i.key == pygame.K_DOWN:
                    tee.location.y -= 0.01
                elif i.key == pygame.K_RIGHT:
                    tee.location.x += 0.01
                elif i.key == pygame.K_LEFT:
                    tee.location.x -= 0.01
                elif i.key == pygame.K_KP0:
                    tee.location.z -= 0.01
                elif i.key == pygame.K_KP1:
                    tee.location.z += 0.01

                periscope.correct_planes(tee, iteration)
                iteration += 1


if __name__ == '__main__':
    run()


