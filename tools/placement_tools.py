from langchain_core.tools import tool
from core.sw_state import state
from config import MIN_DIMENSION_GAP_MM


@tool
def check_overlaps(plan: list) -> dict:
    """
    Check a dimension placement plan for overlapping positions.
    Two dimensions closer than the minimum gap are flagged as 
    conflicts. Returns whether conflicts exist and the conflict list.
    """
    conflicts, placed = [], []

    for item in plan:
        x, y = item["x_mm"], item["y_mm"]
        for prev in placed:
            dist = ((x-prev["x_mm"])**2 + (y-prev["y_mm"])**2) ** 0.5
            if dist < MIN_DIMENSION_GAP_MM:
                conflicts.append({
                    "dim_1": prev["dim_name"], "dim_2": item["dim_name"],
                    "distance_mm": round(dist, 2)
                })
        placed.append(item)

    return {"has_conflicts": len(conflicts) > 0, "conflicts": conflicts}


@tool
def place_dimensions(plan: list) -> dict:
    """
    Place a validated dimension placement plan into the 2D 
    drawing using the SolidWorks API. Each plan item must 
    include dim_name, view_name, x_mm, and y_mm.
    """
    try:
        if state.draw_doc is None:
            if state.sw_app is not None:
                active_doc = state.sw_app.ActiveDoc
                if active_doc is not None and active_doc.GetType == 3:
                    state.draw_doc = active_doc
                    
            if state.draw_doc is None:
                return {"error": "No drawing document is currently active for placing dimensions."}

        import win32com.client
        import pythoncom
        callout = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)

        placed, skipped = 0, 0

        for item in plan:
            try:
                state.draw_doc.ActivateView(item["view_name"])
                state.draw_doc.Extension.SelectByID2(
                    item["dim_name"], "DIMENSION", 0, 0, 0, False, 0, callout, 0
                )
                sel_mgr = state.draw_doc.SelectionManager
                disp_dim = sel_mgr.GetSelectedObject6(1, -1)
                if disp_dim is not None:
                    ann = disp_dim.GetAnnotation
                    ann.SetPosition(item["x_mm"]/1000.0, item["y_mm"]/1000.0, 0.0)
                    placed += 1
                else:
                    skipped += 1
            except Exception:
                skipped += 1

        return {"placed": placed, "skipped": skipped}
    except Exception as e:
        return {"error": f"Failed to place dimensions: {str(e)}"}