from langchain_core.tools import tool
from core.sw_state import state

@tool
def save_drawing() -> dict:
    """Save the currently open 2D drawing to disk."""
    try:
        if state.draw_doc is None:
            if state.sw_app is not None:
                active_doc = state.sw_app.ActiveDoc
                if active_doc is not None and active_doc.GetType == 3:
                    state.draw_doc = active_doc
                    
            if state.draw_doc is None:
                return {"error": "No drawing document is currently active to save."}
                
        import win32com.client
        import pythoncom
        errors = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        state.draw_doc.Save3(1, errors, warnings)
        return {"status": "saved"}
    except Exception as e:
        return {"error": f"Failed to save drawing: {str(e)}"}