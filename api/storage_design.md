# Heat Storage and Consumption Design

## Overview

Heat storage assets are **NOT** production assets. They are bidirectional:
- **Charge (Consumption)**: Storage consumes heat from the system (negative production)
- **Discharge (Production)**: Storage releases heat to the system (positive production)
- **State**: Current stored energy level

## Design Proposal

### 1. Storage-Specific Endpoints

#### Storage Charge/Discharge Data
- **Endpoint**: `GET /assets/{asset_id}/storage/charge-discharge`
  - Returns both charge (negative) and discharge (positive) values
  - Shows net flow: positive = discharging, negative = charging
  - Historical and planned versions

#### Storage State
- **Endpoint**: `GET /assets/{asset_id}/storage/state`
  - Current stored energy (MWh)
  - Capacity (MWh)
  - State of charge percentage (0-100%)

### 2. Heat Consumption Calculation

Heat consumption should be calculated as:

```
Total Heat Available = 
  Sum of all production assets (gas/oil/electric boilers)
  + Storage discharge (if any)
  - Storage charge (if any)

Heat Consumption = 
  Total Heat Available
  - District Heating Network consumption (if applicable)
```

### 3. Proposed Data Models

#### Storage Charge/Discharge
```json
{
  "asset_id": "asset_002",
  "data_points": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "charge": 5.0,      // MW being charged (consumption)
      "discharge": 0.0,   // MW being discharged (production)
      "net_flow": -5.0    // Net: negative = charging, positive = discharging
    }
  ],
  "start_time": "...",
  "end_time": "...",
  "resolution_minutes": 15
}
```

#### Storage State
```json
{
  "asset_id": "asset_002",
  "stored_energy_mwh": 120.5,
  "capacity_mwh": 200.0,
  "state_of_charge_percent": 60.25,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 4. Heat Consumption Endpoint Design

#### Option A: Per Asset (Current Design)
- `GET /assets/{asset_id}/heat-consumption`
- For district heating networks: shows consumption
- For storage: shows charge (consumption)
- For production assets: returns 0 or error

#### Option B: Site-Level Aggregation
- `GET /sites/{site_id}/heat-consumption`
- Aggregates all consumption for a site
- Shows: production, storage charge/discharge, net consumption

#### Option C: Both
- Keep per-asset for detailed view
- Add site-level for aggregated view

### 5. Recommended Approach

**For Heat Consumption Endpoint:**
1. **District Heating Networks**: Show actual consumption (demand)
2. **Storage Assets**: Show charge as consumption (when charging)
3. **Production Assets**: Return 0 or empty (they produce, not consume)

**For Total Available Heat:**
- Create a new endpoint: `GET /sites/{site_id}/heat-balance`
- Shows:
  - Total production (all boilers)
  - Storage discharge
  - Storage charge
  - Net available heat
  - Consumption (district heating)

## Implementation Plan

1. Add storage capacity to Asset model (for storage assets)
2. Create storage charge/discharge data generation
3. Create storage state tracking
4. Update heat consumption to handle:
   - District heating networks (actual consumption)
   - Storage (charge as consumption)
5. Optionally add site-level heat balance endpoint

