
class Point3d:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other) -> 'Point3d':
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other) -> 'Point3d':
        return Point3d(self.x - other.x, self.y - other.y, self.z - other.z)

class Vector:
    def __init__(self, point_end: Point3d, point_start: Point3d = Point3d(0, 0, 0)):
        self.x = point_end.x - point_start.x
        self.y = point_end.y - point_start.y
        self.z = point_end.z - point_start.z

    def normalize(self):
        norm = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        self.x /= norm
        self.y /= norm
        self.z /= norm

    def scalar_prod(self, b: 'Vector') -> float:
        return self.x * b.x + self.y * b.y + self.z * b.z


    def vector_prod(self, b: 'Vector') -> 'Vector':
        # right triple vectors
        return Vector(Point3d(
                self.y * b.z - self.z * b.y,
                self.z * b.x - self.x * b.z,
                self.x * b.y - self.y * b.x,
            )
        )
        pass

    def get_point(self) -> Point3d:
        return Point3d(self.x, self.y, self.z)

    def __mul__(self, constant: float) -> 'Vector':
        return Vector(Point3d(self.x * constant, self.y * constant, self.z * constant))

    def __truediv__(self, constant: float) -> 'Vector':
        return Vector(Point3d(self.x / constant, self.y / constant, self.z / constant))


class Triangle:
    def __init__(self, point_a, point_b, point_c):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c


class Ray:
    def __init__(self, location: Point3d,  direction: Vector):
        self.startPos: Point3d = location
        direction.normalize()
        self.dir: Vector = direction
        self.unit_length_dist_point = location + direction

    def intersect_plane(self, plane: Triangle) -> Point3d:
        # normal to plane: N = (B - A) x (C - A)
        n = Vector(plane.point_b, plane.point_a).vector_prod(Vector(plane.point_c, plane.point_a))
        n.normalize()
        v = Vector(plane.point_a, self.startPos)  # V = A - X
        # distance from X to plane
        d = n.scalar_prod(v)  # d = N * V
        # dir projection to N
        e = v.scalar_prod(self.dir)  #  e = N * (Y - X)

        if e == 0 or d == 0:
            raise ValueError()

        return self.startPos + (self.dir * d / e)

    def reflect_plane(self, plane: Triangle) -> 'Ray':
        o = self.intersect_plane(plane)
        m = self.startPos + Vector(o, self.startPos)

        n = Vector(plane.point_b, plane.point_a).vector_prod(Vector(plane.point_c, plane.point_a))
        n.normalize()
        v = Vector(plane.point_a, self.startPos)  # V = A - X
        d = n.scalar_prod(v)  # d = N * V

        m_symm = m + n * 2 * d  # symmetrical point TODO: think, maybe minus

        return Ray(o, Vector(m_symm - o))