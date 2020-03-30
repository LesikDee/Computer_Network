from geometry import Triangle

class Mirror:
    def __init__(self, triangle: Triangle):
        self.static_point = triangle.point_a
        self.triangle = triangle
