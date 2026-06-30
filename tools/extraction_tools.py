from langchain_core.tools import tool
from core.sw_state import state
from core.dim_classifier import SKIP_TYPES, classify_dimension


@tool
def extract_all_dimensions(part_path: str) -> dict:
    """
    Open a SolidWorks 3D part and extract every dimension from 
    every feature in the model tree, including linear, angular, 
    and integer dimensions. Skips reference geometry that has no 
    dimensions. Returns total feature count, total dimension 
    count, and a structured breakdown per feature.
    """
    try:
        if state.sw_app is None:
            return {"error": "Not connected. Call connect_to_solidworks first."}

        import win32com.client
        import pythoncom
        errors = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warnings = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)

        # OpenDoc6 parameters: (FileName, Type, Options, Configuration, Errors, Warnings)
        # Type: 1 = swDocPART, Options: 1 = swOpenDocOptions_Silent
        state.part_doc = state.sw_app.OpenDoc6(part_path, 1, 1, "", errors, warnings)
        if state.part_doc is None:
            return {"error": f"Could not open part: {part_path}"}

        features_data = []
        feat = state.part_doc.FirstFeature

        while feat is not None:
            feat_name = feat.Name
            feat_type = feat.GetTypeName2

            if feat_type in SKIP_TYPES:
                feat = feat.GetNextFeature
                continue

            dims = []
            dd = feat.GetFirstDisplayDimension

            while dd is not None:
                try:
                    d = dd.GetDimension
                    raw_type = d.GetType
                    dim_type, val, unit = classify_dimension(
                        raw_type, d.SystemValue, d.Value
                    )
                    dims.append({
                        "name": d.Name, "value": val,
                        "unit": unit, "type": dim_type
                    })
                except Exception as e:
                    print(f"Warning: skipped one dim — {e}")

                dd = feat.GetNextDisplayDimension(dd)

            features_data.append({
                "feature_name": feat_name,
                "feature_type": feat_type,
                "dimensions":   dims,
                "dim_count":    len(dims)
            })

            feat = feat.GetNextFeature

        state.all_dims = [
            {**d, "feature": f["feature_name"]}
            for f in features_data for d in f["dimensions"]
        ]

        return {
            "status":        "success",
            "part_name":     state.part_doc.GetTitle,
            "total_features": len(features_data),
            "total_dims":     len(state.all_dims),
            "features":       features_data
        }
    except Exception as e:
        return {"error": f"Failed to extract dimensions: {str(e)}"}