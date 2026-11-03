from dataclasses import dataclass


def _check_int(value, what):
    # bool is a subclass of int; reject it explicitly.
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f'{what} must be an int, got {type(value).__name__}')
    return value


@dataclass(frozen=True, slots=True)
class Vector2D:
    """An immutable two-dimensional vector with integer Cartesian coordinates.

    Being frozen with value equality, instances are hashable and can be used
    in sets and as dict keys.
    """

    x: int
    y: int

    def __post_init__(self):
        _check_int(self.x, 'x')
        _check_int(self.y, 'y')

    def __str__(self):
        """Human-readable string representation of the vector."""
        return f'{self.x}i + {self.y}j'

    def dot(self, other):
        """The scalar (dot) product of self and other."""
        if not isinstance(other, Vector2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y
    # Alias so a @ b works as well as a.dot(b).
    __matmul__ = dot

    def __add__(self, other):
        """Vector addition."""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Vector subtraction."""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by an integer scalar."""
        if not isinstance(scalar, int) or isinstance(scalar, bool):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __neg__(self):
        """Negation of the vector (invert through origin)."""
        return Vector2D(-self.x, -self.y)

    def __floordiv__(self, scalar):
        """Floor division of each component by an integer scalar."""
        if not isinstance(scalar, int) or isinstance(scalar, bool):
            return NotImplemented
        return Vector2D(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar):
        """Modulus of each component by an integer scalar."""
        if not isinstance(scalar, int) or isinstance(scalar, bool):
            return NotImplemented
        return Vector2D(self.x % scalar, self.y % scalar)

    def length_squared(self):
        """Squared magnitude of the vector (exact, stays an integer)."""
        return self.x * self.x + self.y * self.y

    def distance_squared_to(self, other):
        """Squared distance between vectors self and other."""
        return (self - other).length_squared()


if __name__ == '__main__':
    v1 = Vector2D(2, 5)
    v2 = Vector2D(3, -4)
    print('v1 =', v1)
    print('repr(v2) =', repr(v2))
    print('v1 + v2 =', v1 + v2)
    print('v1 - v2 =', v1 - v2)
    print('-v2 =', -v2)
    print('v1 * 3 =', v1 * 3)
    print('7 * v2 =', 7 * v2)
    print('v2 // 2 =', v2 // 2)
    print('v1 % 3 =', v1 % 3)
    print('v1 @ v2 =', v1 @ v2)
    print('v1.distance_squared_to(v2) =', v1.distance_squared_to(v2))
    print('hash-equal:', Vector2D(1, 2) == Vector2D(1, 2), len({Vector2D(1, 2), Vector2D(1, 2)}))
    try:
        Vector2D(1.5, 2)
    except TypeError as e:
        print('rejected:', e)
