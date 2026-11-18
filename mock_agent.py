import json
import uuid
import sys
import os
from datetime import datetime, timezone

# Add parent directory to path to import connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connectors.east_asia_connector import EastAsiaSupplierConnector

class BeltAndBytePublicSDK:
    """
    Public SDK & Mock Agent for Belt & Byte AI.
    Validates RFQ payloads against the open schema without exposing private core algorithms.
    """
    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.sdk_version = "1.0.0-public"
        self.connector = EastAsiaSupplierConnector()

    def create_standardized_rfq(self, part_name: str, material: str, sealing: str, temp_c: float, qty: int, dest: str) -> dict:
        rfq_payload = {
            "rfq_id": f"RFQ-{uuid.uuid4().hex[:8].upper()}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "item_specifications": {
                "part_name": part_name,
                "material_grade": material,
                "sealing_material": sealing,
                "max_operating_temp_celsius": temp_c,
                "quantity": qty
            },
            "logistics_preferences": {
                "origin_region": "East Asia",
                "destination_hub": dest,
                "incoterms": "CIF",
                "preferred_corridors": ["Maritime_Direct", "Central_Eurasia_Rail"]
            },
            "commercial_terms": {
                "currency": "USD",
                "benchmark_index": "GLOBAL_COMMODITY_REF",
                "target_lead_time_days": 25
            }
        }
        return rfq_payload

    def simulate_workflow(self, rfq_payload: dict):
        print(f"=== [1] Generated Standardized RFQ: {rfq_payload['rfq_id']} ===")
        dispatch_str = self.connector.format_supplier_dispatch(rfq_payload)
        print("\n=== [2] Formatted Dispatch Packet for East Asia Suppliers ===")
        print(dispatch_str)
        
        print("\n=== [3] Simulating Handshake with Private Offline-First Core ===")
        response = {
            "rfq_id": rfq_payload["rfq_id"],
            "status": "QUEUED_FOR_PRIVATE_CORE",
            "message": "Payload complies with SAA Protocol. Ready for private negotiation engine."
        }
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    sdk = BeltAndBytePublicSDK("Production_Unit_X")
    sample_rfq = sdk.create_standardized_rfq(
        part_name="Production Complement Component X",
        material="SS 316L",
        sealing="Viton",
        temp_c=85.0,
        qty=2500,
        dest="Amman_Hub"
    )
    sdk.simulate_workflow(sample_rfq)
