from langchain_core.tools import tool
from core.sw_state import state
from config import TEMPLATE_PATH
import os
import win32com.client
import pythoncom


@tool
def create_drawing(part_path: str) -> dict:
    """
    Create a 2D engineering drawing from a 3D SolidWorks part 
    with standard front, top, and right views. Returns the path 
    of the created drawing file. Does NOT add dimensions — 
    that is handled later by the agent's placement plan.
    """
    try:
        if state.sw_app is None:
            return {"error": "Not connected. Call connect_to_solidworks first."}

        base_path, _ = os.path.splitext(part_path)
        drawing_path = base_path + ".SLDDRW"

        # Only close if a document with this path is actually open
        try:
            existing_doc = state.sw_app.GetOpenDocumentByName(drawing_path)
            if existing_doc is not None:
                state.sw_app.CloseDoc(drawing_path)
        except Exception:
            pass  # nothing open with that name, safe to continue

        errors   = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

        if TEMPLATE_PATH.lower().endswith(".slddrw"):
            state.draw_doc = state.sw_app.OpenDoc6(
                TEMPLATE_PATH, 3, 1, "", errors, warnings
            )
        else:
            state.draw_doc = state.sw_app.NewDocument(TEMPLATE_PATH, 0, 0.0, 0.0)

        if state.draw_doc is None:
            return {"error": f"Failed to open drawing document using: {TEMPLATE_PATH}"}

        state.draw_doc.Create3rdAngleViews2(part_path)

        state.draw_doc.ForceRebuild3(True)
        state.draw_doc.SaveAs(drawing_path)

        return {"status": "success", "drawing_path": drawing_path}

    except Exception as e:
        return {"error": f"Failed to create drawing: {str(e)}"}


@tool
def get_drawing_views() -> dict:
    """
    Get bounding box outlines and names of all drawing views on 
    the active drawing sheet. Returns sheet dimensions and views list.
    """
    try:
        if state.draw_doc is None:
            if state.sw_app is not None:
                active_doc = state.sw_app.ActiveDoc
                if active_doc is not None and active_doc.GetType() == 3:
                    state.draw_doc = active_doc

        if state.draw_doc is None:
            return {"error": "No drawing document is currently active. Call create_drawing first."}

        print("get_drawing_views - title:", state.draw_doc.GetTitle())
        print("get_drawing_views - type:", state.draw_doc.GetType())

        views = []
        view = state.draw_doc.GetFirstView()

        while view is not None:
            if "Sheet" not in view.Name:
                o = view.GetOutline()
                if o is not None:
                    views.append({
                        "name": view.Name,
                        "x_min": round(o[0]*1000, 1), "y_min": round(o[1]*1000, 1),
                        "x_max": round(o[2]*1000, 1), "y_max": round(o[3]*1000, 1),
                    })
            view = view.GetNextView()

        sheet = state.draw_doc.GetCurrentSheet()
        if sheet is not None:
            props = sheet.GetProperties2()
            width_mm  = round(props[5] * 1000, 1)
            height_mm = round(props[6] * 1000, 1)
        else:
            width_mm  = 0.0
            height_mm = 0.0

        return {
            "views": views,
            "sheet_width_mm":  width_mm,
            "sheet_height_mm": height_mm
        }
    except Exception as e:
        return {"error": f"Failed to get drawing views: {str(e)}"}