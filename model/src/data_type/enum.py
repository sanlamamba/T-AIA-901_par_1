from enum import Enum


class CityType(Enum):
    intermediary = "intermediary"
    arrival = "arrival"
    departure = "departure"
    none = "none"

class IOBTypes(Enum):
    B = "B"
    I = "I"
    O = "O"
