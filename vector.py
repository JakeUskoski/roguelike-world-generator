import math

class Vector:
    def __init__(self, x = None, y = None, z = None):
        self.coordinates = []
        if x is not None:
            self.coordinates.append(x)
        if y is not None:
            self.coordinates.append(y)
        if z is not None:
            self.coordinates.append(z)

    def clone(self):
        if self.get_dimension() == 2:
            return Vector(self.coordinates[0], self.coordinates[1])
        elif self.get_dimension() == 1:
            return Vector(self.coordinates[0])
        elif self.get_dimension() == 0:
            return Vector()
        else:
            return Vector(self.coordinates[0], self.coordinates[1], self.coordinates[2])

    def get_dimension(self):
        return len(self.coordinates)

    def __add__(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        vector = self.clone()
        for i in range(vector.get_dimension()):
            vector.coordinates[i] += other.coordinates[i]
        return vector

    def __sub__(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        vector = self.clone()
        for i in range(vector.get_dimension()):
            vector.coordinates[i] -= other.coordinates[i]
        return vector

    def __neg__(self):
        if self.get_dimension() == 2:
            return Vector(-self.coordinates[0], -self.coordinates[1])
        elif self.get_dimension() == 1:
            return Vector(-self.coordinates[0])
        elif self.get_dimension() == 0:
            return Vector()
        else:
            return Vector(-self.coordinates[0], -self.coordinates[1], -self.coordinates[2])

    def __iadd__(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        for i in range(self.get_dimension()):
            self.coordinates[i] += other.coordinates[i]

    def __isub__(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        for i in range(self.get_dimension()):
            self.coordinates[i] -= other.coordinates[i]

    def magnitude(self):
        total = 0
        for i in range(self.get_dimension()):
            total += self.coordinates[i] * self.coordinates[i]
        return math.sqrt(total)

    def squared_magnitude(self):
        total = 0
        for i in range(self.get_dimension()):
            total += self.coordinates[i] * self.coordinates[i]
        return total

    def multiply(self, x):
        vector = self.clone()
        for i in range(vector.get_dimension()):
            vector.coordinates[i] *= x

    def dot_product(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        total = 0
        for i in range(self.get_dimension()):
            total += self.coordinates[i] * other.coordinates[i]
        return total

    def angle(self, other):
        if self.get_dimension() != other.get_dimension():
            return
        prod = self.dot_product(other)
        if prod == 1:
            return 0
        elif prod == 0.5:
            return math.radians(60)
        elif prod == 0:
            return math.radians(90)
        elif prod == -0.5:
            return math.radians(120)
        elif prod == -1:
            return math.radians(180)
        else:
            return math.acos(prod)


