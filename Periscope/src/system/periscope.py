from src.geometry import *
from src.system.mirror import Mirror
from src.target import Target
import math

class MirrorPos(Enum):
    UP = 1
    DOWN = 2

class Periscope:

    EPS_ANGLE_DELTA = 0.008

    def __init__(self, config):
        self.laser: Ray = Ray(config['start_laser_location'], config['start_laser_direction'])
        points3_down_tr = config['down_triangle']
        self.mirror_down = Mirror(Triangle(points3_down_tr[0], points3_down_tr[1], points3_down_tr[2]))
        points3_up_tr = config['up_triangle']
        self.mirror_up = Mirror(Triangle(points3_up_tr[0], points3_up_tr[1], points3_up_tr[2]))

        self.tee = Target

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
        input_ray = self.laser.reflect_plane(self.mirror_down.triangle)

        if mirror_pos == MirrorPos.UP:
            current_plane = self.mirror_up.triangle
        else:
            current_plane = self.mirror_down.triangle

        input_diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target)

        plane_angle_plus: Triangle = current_plane.rotate_plane(angle, angle_name)
        plane_angle_minus: Triangle = current_plane.rotate_plane(-angle, angle_name)

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

        if mirror_pos == MirrorPos.UP:
            if not self.__check_rotate_relevant(input_ray, plane_angle_step):
                return
        else:
            ray = self.laser.reflect_plane(plane_angle_step)
            if not self.__check_rotate_relevant(ray, self.mirror_up.triangle):
                return
            if not self.__check_rotate_relevant(self.laser, plane_angle_step):
                return

        prev_diff = input_diff
        angle_step = 1
        while diff < prev_diff:
            angle_step += 1
            new_plane_angle_step: Triangle = current_plane.rotate_plane(angle * angle_step * angle_sign, angle_name)
            prev_diff = diff

            if mirror_pos == MirrorPos.UP:
                if not self.__check_rotate_relevant(input_ray, plane_angle_step):
                    return
            else:
                ray = self.laser.reflect_plane(plane_angle_step)
                if not self.__check_rotate_relevant(ray, self.mirror_up.triangle):
                    return
                if not self.__check_rotate_relevant(self.laser, plane_angle_step):
                    return


            plane_angle_step = new_plane_angle_step

            if mirror_pos == MirrorPos.UP:
                diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, plane_angle_step, target)
            else:
                diff = self.final_ray_target_diff(self.laser, plane_angle_step, self.mirror_up.triangle, target)

        if mirror_pos == MirrorPos.UP:
            self.mirror_up.triangle = plane_angle_step
        else:
            self.mirror_down.triangle = plane_angle_step

    # if point (on ray and plane) is in triangle
    @staticmethod
    def __check_rotate_relevant(ray: Ray, plane: Triangle) -> bool:
        point_plane_intersect: Point3d = ray.intersect_plane(plane)
        xz_a = Point2d(plane.point_a.x, plane.point_a.z)
        xz_b = Point2d(plane.point_b.x, plane.point_b.z)
        xz_c = Point2d(plane.point_c.x, plane.point_c.z)
        xz_k = Point2d(point_plane_intersect.x, point_plane_intersect.z)

        is_relevant = True
        is_relevant *= Periscope.__on_one_side_of_the_plane(Vector2d(xz_b, xz_a), Vector2d(xz_c, xz_a), Vector2d(xz_k, xz_a))
        is_relevant *= Periscope.__on_one_side_of_the_plane(Vector2d(xz_c, xz_a), Vector2d(xz_b, xz_a),
                                                            Vector2d(xz_k, xz_a))
        is_relevant *= Periscope.__on_one_side_of_the_plane(Vector2d(xz_b, xz_c), Vector2d(xz_a, xz_c),
                                                            Vector2d(xz_k, xz_c))
        return is_relevant

    @staticmethod
    def __on_one_side_of_the_plane(v_plane: Vector2d, v2: Vector2d, vk: Vector2d) -> bool:
        pseudo_scalar_v_plane_vk = v_plane.pseudo_scalar_prod(vk)
        pseudo_scalar_v_plane_v2 = v_plane.pseudo_scalar_prod(v2)

        if pseudo_scalar_v_plane_vk * pseudo_scalar_v_plane_v2 > 0:
            return True

        return False

    def correct_planes(self, target: Target, iteration: int = 0):
        diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target.location)
        step = 0
        first_type_plane = MirrorPos.UP
        second_type_plane = MirrorPos.DOWN
        if iteration % 2 == 0:
            first_type_plane = MirrorPos.DOWN
            second_type_plane = MirrorPos.UP

        while diff > target.radius and step < 10:
            self.__rotate_plane_in_best_angle(first_type_plane, Angle.ROLL, target.location, step)
            self.__rotate_plane_in_best_angle(first_type_plane, Angle.PITCH, target.location, step)

            self.__rotate_plane_in_best_angle(second_type_plane, Angle.ROLL, target.location, step)
            self.__rotate_plane_in_best_angle(second_type_plane, Angle.PITCH, target.location, step)

            diff = self.final_ray_target_diff(self.laser, self.mirror_down.triangle, self.mirror_up.triangle, target.location)
            step += 1
