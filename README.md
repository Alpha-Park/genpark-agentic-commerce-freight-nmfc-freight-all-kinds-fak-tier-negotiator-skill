# LTL Freight All Kinds (FAK) Tier Negotiation & Spend Optimizer Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `optimize_ltl_fak_tier_thresholds`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Simulates historical LTL class distributions across actual NMFC densities, modeling optimal Freight All Kinds (FAK) class tiers (e.g. Class 150-300 rated as Class 100) to slash freight spend.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Logistics / Freight Contracting)`

## MCP Tool Specification
### `optimize_ltl_fak_tier_thresholds`
Parameters:
- `annual_ltl_shipment_count` (int): Total LTL shipments dispatched per year
- `class_distribution_weights` (list): List of [nmfc_class, total_weight_lbs, actual_freight_spend_usd]
- `proposed_fak_agreement_class` (str): Target negotiated blanket FAK class (e.g. 'Class 70' or 'Class 100')
- `discount_off_tariff_czar_lite_pct` (float): Negotiated discount off CzarLite base rates (e.g. 78.5%)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-freight-nmfc-freight-all-kinds-fak-tier-negotiator-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-freight-nmfc-freight-all-kinds-fak-tier-negotiator-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
