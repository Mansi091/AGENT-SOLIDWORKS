import win32com.client
import pythoncom

class SolidWorksConnection:

    def __init__(self):
        self.sw_app = None

    def connect(self):
        """
        Connect to SolidWorks.
        SolidWorks must already be open on your laptop.
        """
        pythoncom.CoInitialize()

        try:
            # Try to connect to already running SolidWorks
            self.sw_app = win32com.client.GetActiveObject(
                "SldWorks.Application"
            )
            print("Connected to running SolidWorks instance")

        except Exception:
            # SolidWorks not open — launch it
            self.sw_app = win32com.client.Dispatch(
                "SldWorks.Application"
            )
            self.sw_app.Visible = True##property
            print("Launched SolidWorks")


        return self.sw_app

    def open_part(self, part_path: str):
        """Open a .sldprt file and return the document"""
        errors = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

        doc = self.sw_app.OpenDoc6(
            part_path,
            1,        # 1 = part file
            1,        # 1 = swOpenDocOptions_Silent
            "",       # configuration name
            errors,
            warnings
        )
        ##doc is opened document

        if doc is None:
            raise Exception(f"Could not open file: {part_path}")

        print(f"Opened part: {part_path}")
        return doc