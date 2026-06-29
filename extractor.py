#extract every dimension from every feature

class DimensionExtractor:

    # Feature types we skip — they never have dimensions
    SKIP_TYPES = [
        "RefPlane",               # Front/Top/Right Plane
        "RefAxis",                # Reference Axis
        "RefPoint",               # Reference Point
        "OriginProfileFeature",   # Origin
        "SolidBodyFolder",        # Solid Bodies folder
        "Equations",              # Equations
        "material",               # Material
        "CoordSys",               # Coordinate System
        "BodyFolder",             # Body folder
    ]

    # Dimension parameter type mapping (swDimensionParamType_e)
    DIM_TYPES = {
        0: "linear",   # swDimensionParamTypeDoubleLinear
        1: "angular",  # swDimensionParamTypeDoubleAngular
        2: "integer"   # swDimensionParamTypeInteger
    }

    def __init__(self, part_doc):
        self.part = part_doc

    def extract(self) -> dict:
        """
        Walk every feature in model tree.
        Extract every dimension from every feature.
        Return structured dictionary.
        """

        features_data = []
        feat = self.part.FirstFeature

        while feat is not None:

            feat_name = feat.Name
            feat_type = feat.GetTypeName2

            # skip non-dimension features
            if feat_type in self.SKIP_TYPES:
                feat = feat.GetNextFeature
                continue

            # extract dimensions from this feature
            dims = self._extract_dims_from_feature(feat)

            features_data.append({
                "feature_name": feat_name,
                "feature_type": feat_type,
                "dimensions":   dims,
                "dim_count":    len(dims)
            })

            feat = feat.GetNextFeature

        # build final output
        total_dims = sum(f["dim_count"] for f in features_data)

        return {
            "part_name":      self.part.GetTitle,
            "total_features": len(features_data),
            "total_dims":     total_dims,
            "features":       features_data
        }

    def _extract_dims_from_feature(self, feat) -> list:
        """Extract every dimension from one feature"""
        import math
        dims = []
        dd   = feat.GetFirstDisplayDimension

        while dd is not None:
            try:
                d = dd.GetDimension
                raw_type = d.GetType
                dim_type = self.DIM_TYPES.get(raw_type, "unknown")

                if raw_type == 1:  # swDimensionParamTypeDoubleAngular
                    val = round(d.SystemValue * 180.0 / math.pi, 3)
                    unit = "deg"
                elif raw_type == 0:  # swDimensionParamTypeDoubleLinear
                    val = round(d.SystemValue * 1000.0, 3)
                    unit = "mm"
                else:  # swDimensionParamTypeInteger
                    val = d.Value
                    unit = ""

                dims.append({
                    "name":  d.Name,
                    "value": val,
                    "unit":  unit,
                    "type":  dim_type,
                })

            except Exception as e:
                print(f"  Warning: could not read one dimension — {e}")

            dd = feat.GetNextDisplayDimension(dd)

        return dims