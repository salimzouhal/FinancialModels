from enum import Enum


class PayoffType(Enum):
    CALL = 1
    PUT = -1

    
class InterpolationConvention(Enum):
    LINEAR = 0
    QUADRATIC = 1

