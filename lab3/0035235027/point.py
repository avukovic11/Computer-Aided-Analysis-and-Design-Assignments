import math

class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.dim = len(coordinates)

    def to_matrix(self):
        from matrix import Matrix
        return Matrix(data=[[coord] for coord in self.coordinates])

    def __add__(self, other):
        if isinstance(other, Point):
            return Point([a + b for a, b in zip(self.coordinates, other.coordinates)])
        elif isinstance(other, (int, float)):
            return Point([a + other for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for addition")

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Point):
            for i in range(self.dim):
                self.coordinates[i] += other.coordinates[i]
        elif isinstance(other, (int, float)):
            for i in range(self.dim):
                self.coordinates[i] += other
        else:
            raise TypeError("Unsupported type for in-place addition")
        return self

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point([a - b for a, b in zip(self.coordinates, other.coordinates)])
        elif isinstance(other, (int, float)):
            return Point([a - other for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for subtraction")

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Point([other - a for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for reverse subtraction")

    def __isub__(self, other):
        if isinstance(other, Point):
            for i in range(self.dim):
                self.coordinates[i] -= other.coordinates[i]
        elif isinstance(other, (int, float)):
            for i in range(self.dim):
                self.coordinates[i] -= other
        else:
            raise TypeError("Unsupported type for in-place subtraction")
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point([a * other for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for multiplication")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            for i in range(self.dim):
                self.coordinates[i] *= other
        else:
            raise TypeError("Unsupported type for in-place multiplication")
        return self

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point([a / other for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for division")

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Point([other / a for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for reverse division")

    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            for i in range(self.dim):
                self.coordinates[i] /= other
        else:
            raise TypeError("Unsupported type for in-place division")
        return self

    def __pow__(self, power):
        if isinstance(power, (int, float)):
            return Point([a ** power for a in self.coordinates])
        else:
            raise TypeError("Unsupported type for power")

    def __getitem__(self, index):
        return self.coordinates[index]

    def __setitem__(self, index, value):
        self.coordinates[index] = value

    def copy(self):
        return Point(self.coordinates[:])

    def __repr__(self):
        return f"Point({self.coordinates})"
    
    def euclidean_norm(self):
        return math.sqrt(sum([x_i**2 for x_i in self.coordinates]))