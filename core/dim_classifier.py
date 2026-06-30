import math

SKIP_TYPES = [
    "RefPlane", "RefAxis", "RefPoint",
    "OriginProfileFeature", "SolidBodyFolder",
    "Equations", "material", "CoordSys", "BodyFolder",
]

DIM_TYPES = {
    0: "linear",
    1: "angular",
    2: "integer"
}

def classify_dimension(raw_type: int, system_value: float, raw_value):
    """Convert raw SolidWorks dimension data into clean values"""
    dim_type = DIM_TYPES.get(raw_type, "unknown")

    if raw_type == 1:    # angular
        val  = round(system_value * 180.0 / math.pi, 3)
        unit = "deg"
    elif raw_type == 0:  # linear
        val  = round(system_value * 1000.0, 3)
        unit = "mm"
    else:                # integer
        val  = raw_value
        unit = ""

    return dim_type, val, unit