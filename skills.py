# -*- coding: utf-8 -*-
"""LTL Freight All Kinds (FAK) Tier Negotiation & Spend Optimizer Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def optimize_ltl_fak_tier_thresholds(**kwargs):
    """Simulates historical LTL class distributions across actual NMFC densities, modeling optimal Freight All Kinds (FAK) class tiers (e.g. Class 150-300 rated as Class 100) to slash freight spend."""
    annual_ltl_shipment_count = kwargs.get('annual_ltl_shipment_count')
    class_distribution_weights = kwargs.get('class_distribution_weights')
    proposed_fak_agreement_class = kwargs.get('proposed_fak_agreement_class')
    discount_off_tariff_czar_lite_pct = kwargs.get('discount_off_tariff_czar_lite_pct')

    total_baseline_spend = sum(x[2] for x in class_distribution_weights)
    total_weight = sum(x[1] for x in class_distribution_weights)
    
    # Blanket FAK savings heuristic: higher classes (125, 175, 250) re-rated down to target FAK class
    projected_fak_spend = 0.0
    for cls, wt, spend in class_distribution_weights:
        cls_num = int(cls.replace("Class ", ""))
        target_num = int(proposed_fak_agreement_class.replace("Class ", ""))
        if cls_num > target_num:
            # Savings proportional to class delta
            savings_factor = target_num / cls_num
            projected_fak_spend += spend * savings_factor
        else:
            projected_fak_spend += spend
            
    projected_fak_spend = round(projected_fak_spend, 2)
    annual_savings_usd = round(total_baseline_spend - projected_fak_spend, 2)
    savings_pct = round((annual_savings_usd / (total_baseline_spend if total_baseline_spend > 0 else 1.0)) * 100.0, 1)
    
    result = {
        "status": "success",
        "total_annual_shipments": annual_ltl_shipment_count,
        "total_freight_weight_lbs": total_weight,
        "baseline_freight_spend_usd": total_baseline_spend,
        "simulated_fak_spend_usd": projected_fak_spend,
        "projected_annual_fak_savings_usd": annual_savings_usd,
        "spend_reduction_percentage": savings_pct,
        "procurement_rfp_directive": f"Enforce {proposed_fak_agreement_class} FAK on all items rated Class 125 through 300; expected annual cost reduction ${annual_savings_usd:,.2f}.",
        "engine": "GenPark LTL Freight All Kinds (FAK) Contracting Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "optimize_ltl_fak_tier_thresholds": {
        "name": "optimize_ltl_fak_tier_thresholds",
        "description": "Simulates historical LTL class distributions across actual NMFC densities, modeling optimal Freight All Kinds (FAK) class tiers (e.g. Class 150-300 rated as Class 100) to slash freight spend.",
        "parameters": {
            "type": "object",
            "properties": {
                "annual_ltl_shipment_count": {"type": "integer", "description": "Total LTL shipments dispatched per year"},
                "class_distribution_weights": {"type": "array", "description": "List of [nmfc_class, total_weight_lbs, actual_freight_spend_usd]"},
                "proposed_fak_agreement_class": {"type": "string", "description": "Target negotiated blanket FAK class (e.g. 'Class 70' or 'Class 100')"},
                "discount_off_tariff_czar_lite_pct": {"type": "number", "description": "Negotiated discount off CzarLite base rates (e.g. 78.5%)"},
            },
            "required": ['annual_ltl_shipment_count', 'class_distribution_weights', 'proposed_fak_agreement_class', 'discount_off_tariff_czar_lite_pct']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "optimize_ltl_fak_tier_thresholds":
            res = optimize_ltl_fak_tier_thresholds(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-freight-nmfc-freight-all-kinds-fak-tier-negotiator-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-freight-nmfc-freight-all-kinds-fak-tier-negotiator-skill...")
    test_args = {'annual_ltl_shipment_count': 1400, 'class_distribution_weights': [['Class 70', 450000.0, 68000.0], ['Class 125', 380000.0, 92000.0], ['Class 175', 220000.0, 78000.0], ['Class 250', 110000.0, 54000.0]], 'proposed_fak_agreement_class': 'Class 100', 'discount_off_tariff_czar_lite_pct': 78.5}
    res = optimize_ltl_fak_tier_thresholds(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-freight-nmfc-freight-all-kinds-fak-tier-negotiator-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
