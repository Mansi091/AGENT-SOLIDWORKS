from tools.connection_tools import connect_to_solidworks
from tools.extraction_tools import extract_all_dimensions
from tools.drawing_tools    import create_drawing, get_drawing_views
from tools.placement_tools  import check_overlaps, place_dimensions
from tools.save_tools       import save_drawing

ALL_TOOLS = [
    connect_to_solidworks,
    extract_all_dimensions,
    create_drawing,
    get_drawing_views,
    check_overlaps,
    place_dimensions,
    save_drawing
]