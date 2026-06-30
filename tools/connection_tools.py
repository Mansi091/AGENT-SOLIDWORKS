import win32com.client
import pythoncom
from langchain_core.tools import tool
from core.sw_state import state


@tool
def connect_to_solidworks() -> dict:
    """
    Connect to a running SolidWorks application instance.
    Must be called first before any other SolidWorks tool.
    """
    pythoncom.CoInitialize()
    state.sw_app = win32com.client.Dispatch("SldWorks.Application")
    state.sw_app.Visible = True
    return {"status": "connected"}