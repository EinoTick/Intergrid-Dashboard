"""
Deterministic heat consumption data generation.

Generates heat consumption data ensuring energy balance consistency:
Production + Storage Discharge - Storage Charge = Consumption

For different asset types:
- District Heating Networks: Actual consumption (demand)
- Storage Assets: Charge rate (consumption when charging)
- Production Assets: Return 0 (they produce, not consume)
"""

import random
from datetime import datetime, timedelta
from typing import List, Optional

try:
    from .models import HeatConsumption, HeatConsumptionForecast, AssetType
    from .mock_data import get_asset_by_id, get_assets_by_site_id, get_all_sites
    from .heat_production import _generate_production_value
    from .storage_data import generate_storage_charge_discharge, get_storage_state
except ImportError:
    from models import HeatConsumption, HeatConsumptionForecast, AssetType
    from mock_data import get_asset_by_id, get_assets_by_site_id, get_all_sites
    from heat_production import _generate_production_value
    from storage_data import generate_storage_charge_discharge, get_storage_state


# Fixed seed for reproducibility
RANDOM_SEED = 67890


def _get_consumption_base_pattern(hour: int, minute: int) -> float:
    """
    Get base consumption pattern (similar to production but can differ slightly).
    
    Args:
        hour: Hour of day (0-23)
        minute: Minute of hour (0-59)
        
    Returns:
        Consumption multiplier (0.4-1.3)
    """
    time_of_day = hour + minute / 60.0
    
    # Similar pattern to production but with slight variations
    if 0 <= time_of_day < 6:
        return 0.4 + (time_of_day / 6) * 0.2
    elif 6 <= time_of_day < 9:
        peak_factor = abs(time_of_day - 7.5) / 1.5
        return 1.15 + (1 - peak_factor) * 0.25  # Slightly higher peak
    elif 9 <= time_of_day < 17:
        return 0.85 + (time_of_day - 9) / 8 * 0.25
    elif 17 <= time_of_day < 22:
        peak_factor = abs(time_of_day - 19.5) / 2.5
        return 1.15 + (1 - peak_factor) * 0.25
    else:
        return 1.0 - (time_of_day - 20) / 4 * 0.3


def _get_seasonal_consumption_multiplier(date: datetime) -> float:
    """Get seasonal multiplier for consumption (similar to production)."""
    month = date.month
    if month in [12, 1, 2]:
        return 1.2
    elif month in [3, 4, 10, 11]:
        return 0.9
    else:
        return 0.5


def generate_heat_consumption(
    asset_id: str,
    start_time: datetime,
    end_time: datetime,
) -> List[HeatConsumption]:
    """
    Generate heat consumption data for an asset with energy balance consistency.
    
    For District Heating Networks:
    - Consumption = Production + Storage Discharge - Storage Charge
    - This ensures energy balance
    
    For Storage Assets:
    - Consumption = Charge rate (when charging)
    
    For Production Assets:
    - Returns empty list (they produce, not consume)
    
    Args:
        asset_id: Asset identifier
        start_time: Start of the time range
        end_time: End of the time range
        
    Returns:
        List of consumption data points
    """
    asset = get_asset_by_id(asset_id)
    if asset is None:
        return []
    
    # Production assets don't consume
    if asset.type in [AssetType.GAS_BOILER, AssetType.OIL_BOILER, AssetType.ELECTRIC_BOILER]:
        return []
    
    # Find the site this asset belongs to
    sites = get_all_sites()
    site_id = None
    for site in sites:
        if asset_id in site.asset_ids:
            site_id = site.id
            break
    
    if site_id is None:
        return []
    
    # Get all assets in the site
    site_assets = get_assets_by_site_id(site_id)
    
    # Get production assets
    production_assets = [a for a in site_assets if a.type in [
        AssetType.GAS_BOILER, AssetType.OIL_BOILER, AssetType.ELECTRIC_BOILER
    ]]
    
    # Get storage assets
    storage_assets = [a for a in site_assets if a.type == AssetType.HEAT_STORAGE]
    
    data_points = []
    current_time = start_time.replace(minute=(start_time.minute // 15) * 15, second=0, microsecond=0)
    
    if asset.type == AssetType.DISTRICT_HEATING_NETWORK:
        # Consumption = Production + Storage Discharge - Storage Charge
        while current_time <= end_time:
            # Calculate total production
            total_production = 0.0
            for prod_asset in production_assets:
                total_production += _generate_production_value(
                    prod_asset.id, current_time, prod_asset.type, prod_asset.capacity
                )
            
            # Calculate net storage flow (discharge - charge)
            net_storage_flow = 0.0
            for storage_asset in storage_assets:
                # Get charge/discharge for this storage at this time
                storage_data = generate_storage_charge_discharge(
                    storage_asset.id, current_time, current_time, site_id
                )
                if storage_data:
                    net_storage_flow += storage_data[0].net_flow
            
            # Consumption = Production + Storage Discharge - Storage Charge
            consumption = total_production + net_storage_flow
            
            # Ensure non-negative
            consumption = max(0.0, consumption)
            
            data_points.append(HeatConsumption(
                timestamp=current_time,
                value=round(consumption, 2),
            ))
            
            current_time += timedelta(minutes=15)
    
    elif asset.type == AssetType.HEAT_STORAGE:
        # For storage, consumption = charge rate
        storage_data = generate_storage_charge_discharge(
            asset_id, start_time, end_time, site_id
        )
        for data_point in storage_data:
            if data_point.charge > 0:
                data_points.append(HeatConsumption(
                    timestamp=data_point.timestamp,
                    value=data_point.charge,
                ))
    
    return data_points


def generate_heat_consumption_forecast(
    asset_id: str,
    forecast_start: datetime,
    forecast_end: datetime,
) -> List[HeatConsumptionForecast]:
    """
    Generate forecasted heat consumption.
    
    Uses similar logic to historical but with slightly smoother patterns.
    
    Args:
        asset_id: Asset identifier
        forecast_start: Start of forecast period
        forecast_end: End of forecast period
        
    Returns:
        List of forecasted consumption data points
    """
    # Generate consumption data using the same logic as historical
    consumption_data = generate_heat_consumption(asset_id, forecast_start, forecast_end)
    
    # Convert HeatConsumption to HeatConsumptionForecast
    forecast_data = [
        HeatConsumptionForecast(
            timestamp=item.timestamp,
            value=item.value,
        )
        for item in consumption_data
    ]
    
    return forecast_data

