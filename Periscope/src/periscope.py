from src.geometry import *
from src.mirror import Mirror
import math

from enum import Enum

class MirrorPos(Enum):
    UP = 1
    DOWN = 2

class Angle(Enum):
    YAW = 1
    PITCH = 2

class Periscope:

    EPS_ANGLE_DELTA = 0.005

    def __init__(self, config):
        self.laser: Ray = Ray(config['start_laser_location'], config['start_laser_direction'])
        points3_down_tr = config['down_triangle']
        self.mirror_down = Mirror(Triangle(points3_down_tr[0], points3_down_tr[1], points3_down_tr[2]))
        points3_up_tr = config['up_triangle']
        self.mirror_up = Mirror(Triangle(points3_up_tr[0], points3_up_tr[1], points3_up_tr[2]))

    def ray_to_target(self) -> Ray:
        return self.laser.reflect_plane(self.mirror_down.triangle).reflect_plane(self.mirror_up.triangle)

    @staticmethod
    def final_ray_target_diff(laser: Ray, down_plane: Triangle, up_plane: Triangle, target: Point3d) -> float:
        ray_to_target = laser.reflect_plane(down_plane).reflect_plane(up_plane)
        return target.distance_to_line(ray_to_target.startPos, ray_to_target.startPos + ray_to_target.dir)

    def __define_planes(self, second_m: 'Mirror', upper_plane: Triangle, down_plane: Triangle, ):
        pass

    def __rotate_plane_in_best_angle(self, mirror_pos: MirrorPos, angle_name: Angle, target: Point3d, step: int):
        angle = self.EPS_ANGLE_DELTA /( 2 ** step)

        if mirror_pos == MirrorPos.UP:
            current_plane = self.mirror_up.triangle
        else:
            current_plane = self.mirror_down.triangle

        input_diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target)

        plane_angle_plus: Triangle = current_plane.rotate_plane(angle)
        plane_angle_minus: Triangle = current_plane.rotate_plane(-angle)

        if mirror_pos == MirrorPos.UP:
            diff_angle_plus = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, plane_angle_plus, target)
            diff_angle_minus = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, plane_angle_minus, target)
        else:
            diff_angle_plus = self.final_ray_target_diff(self.laser, plane_angle_plus, self.mirror_up.triangle, target)
            diff_angle_minus = self.final_ray_target_diff(self.laser, plane_angle_minus, self.mirror_up.triangle, target)

        if math.fabs(diff_angle_plus - diff_angle_minus) < 1e-5:
            return

        if diff_angle_plus < diff_angle_minus:
            diff = diff_angle_plus
            angle_sign = 1
            plane_angle_step = plane_angle_plus
        else:
            diff = diff_angle_minus
            angle_sign = -1
            plane_angle_step = plane_angle_minus

        prev_diff = input_diff
        angle_step = 1
        while diff < prev_diff:
            angle_step += 1
            plane_angle_step: Triangle = current_plane.rotate_plane(angle * angle_step * angle_sign)
            prev_diff = diff

            if mirror_pos == MirrorPos.UP:
                diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, plane_angle_step, target)
            else:
                diff = self.final_ray_target_diff(self.laser, plane_angle_step, self.mirror_up.triangle, target)

        if mirror_pos == MirrorPos.UP:
            self.mirror_up.triangle = plane_angle_step
        else:
            self.mirror_down.triangle = plane_angle_step



    def correct_planes(self, target):
        diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target)
        step = 0
        while diff > 1e-2:
            self.__rotate_plane_in_best_angle(MirrorPos.UP, Angle.PITCH, target, step)
            self.__rotate_plane_in_best_angle(MirrorPos.DOWN, Angle.PITCH, target, step)

            diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target)
            step += 1
