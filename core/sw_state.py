class SolidWorksState:
    """Singleton-style state holder for SolidWorks objects"""
    sw_app   = None
    part_doc = None
    draw_doc = None
    all_dims = []

state = SolidWorksState()