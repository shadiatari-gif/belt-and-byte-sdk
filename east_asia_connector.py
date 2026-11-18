import json
from typing import Dict, Any

class EastAsiaSupplierConnector:
    """
    Open-Source Connector Interface for East Asian Manufacturers.
    Formats standardized RFQ payloads for B2B portals or automated email dispatch.
    """
    def __init__(self, region_hub: str = "Shenzhen/Shanghai"):
        self.region_hub = region_hub

    def format_supplier_dispatch(self, rfq_payload: Dict[str, Any]) -> str:
        specs = rfq_payload.get("item_specifications", {})
        logistics = rfq_payload.get("logistics_preferences", {})
        
        dispatch_packet = {
            "header": f"STANDARD_RFQ_DISPATCH::{rfq_payload.get('rfq_id')}",
            "target_hub": self.region_hub,
            "technical_requirements": {
                "component": specs.get("part_name"),
                "material": specs.get("material_grade"),
                "seal": specs.get("sealing_material", "N/A"),
                "max_temp_c": specs.get("max_operating_temp_celsius"),
                "qty": specs.get("quantity")
            },
            "shipping_terms": {
                "incoterms": logistics.get("incoterms"),
                "destination": logistics.get("destination_hub")
            },
            "response_format_required": "JSON_SAA_V1"
        }
        return json.dumps(dispatch_packet, indent=2)

    def parse_supplier_quote(self, raw_quote_json: str) -> Dict[str, Any]:
        """
        Validates incoming supplier quote structure before passing to the Private Core.
        """
        data = json.loads(raw_quote_json)
        required_keys = ["rfq_id", "supplier_id", "unit_price_usd", "lead_time_days", "material_cert_available"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Non-compliant supplier quote: Missing '{key}'")
        return data
