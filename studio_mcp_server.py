"""
CineSync: Real Model Context Protocol (MCP) Server
Powered by the official MCP Python SDK (FastMCP over Stdio Transport)
"""

import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CineSync Studio MCP Server")
INVENTORY_DB = "studio_inventory.json"

def _load_db():
    if not os.path.exists(INVENTORY_DB):
        default_data = {
            "flashlight": {"status": "Available in Prop Locker B", "cost_per_day": 15, "requires_permit": False},
            "gun": {"status": "RESTRICTED: Armorer Clearance Pending", "cost_per_day": 150, "requires_permit": True},
            "camera": {"status": "RED V-Raptor 8K Ready in Studio Vault", "cost_per_day": 1200, "requires_permit": False},
            "vehicle": {"status": "UNAVAILABLE: Unit 4 in Maintenance", "cost_per_day": 2500, "requires_permit": True}
        }
        with open(INVENTORY_DB, "w") as f:
            json.dump(default_data, f, indent=4)
    with open(INVENTORY_DB, "r") as f:
        return json.load(f)

@mcp.tool()
def query_studio_asset_database(item_query: str) -> dict:
    """Securely query the real disk-backed enterprise inventory file for props, equipment, and gear."""
    data = _load_db()
    q = item_query.lower()
    for k, v in data.items():
        if k in q:
            return {
                "protocol": "Model Context Protocol (MCP)",
                "transport": "JSON-RPC 2.0 over Stdio Subprocess",
                "item": k,
                "result": v,
                "server": "CineSync Dyno Studio MCP Server"
            }
    
    new_v = {"status": "Custom Procurement Required from External Vendor", "cost_per_day": 250, "requires_permit": False}
    data[q] = new_v
    with open(INVENTORY_DB, "w") as f:
        json.dump(data, f, indent=4)
        
    return {
        "protocol": "Model Context Protocol (MCP)",
        "transport": "JSON-RPC 2.0 over Stdio Subprocess",
        "item": q,
        "result": new_v,
        "server": "CineSync Dyno Studio MCP Server"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
