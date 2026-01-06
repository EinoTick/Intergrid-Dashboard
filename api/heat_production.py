"""
Deterministic heat production data generation.

Generates realistic heat production data for different asset types:
- Gas boilers: Variable production based on demand patterns
- Oil boilers: Similar to gas but with different characteristics
- Electric boilers: Can respond quickly to price signals
- Heat storage: Can charge/discharge
- District heating networks: Aggregate consumption patterns

All data is deterministic using fixed seeds for reproducibility.
"""

import random
from datetime import datetime, timedelta
from typing import List, Optional

try:
    from .models import HeatProductionDataPoint, AssetType
    from .mock_data import get_asset_by_id
except ImportError:
    from models import HeatProductionDataPoint, AssetType
    from mock_data import get_asset_by_id


# Fixed seed for reproducibility
RANDOM_SEED = 12345


def _get_daily_demand_pattern(hour: int, minute: int) -> float:
    """
    Get daily demand pattern multiplier.
    
    Heat demand typically:
    - Higher in morning (06:00-09:00) and evening (17:00-22:00)
    - Lower during night (00:00-06:00)
    - Medium during day (09:00-17:00)
    
    Args:
        hour: Hour of day (0-23)
        minute: Minute of hour (0-59)
        
    Returns:
        Demand multiplier (0.4-1.3)
    """
    time_of_day = hour + minute / 60.0
    
    # Night hours (00:00-06:00): Low demand
    if 0 <= time_of_day < 6:
        return 0.4 + (time_of_day / 6) * 0.2  # 0.4 to 0.6
    
    # Morning peak (06:00-09:00): High demand
    elif 6 <= time_of_day < 9:
        peak_factor = abs(time_of_day - 7.5) / 1.5  # Peak at 7:30
        return 1.1 + (1 - peak_factor) * 0.2  # 1.1 to 1.3
    
    # Daytime (09:00-17:00): Medium demand
    elif 9 <= time_of_day < 17:
        return 0.8 + (time_of_day - 9) / 8 * 0.2  # 0.8 to 1.0
    
    # Evening peak (17:00-22:00): High demand
    elif 17 <= time_of_day < 22:
        peak_factor = abs(time_of_day - 19.5) / 2.5  # Peak at 19:30
        return 1.1 + (1 - peak_factor) * 0.2  # 1.1 to 1.3
    
    # Late evening/night (22:00-24:00): Decreasing demand
    else:
        return 1.0 - (time_of_day - 22) / 2 * 0.4  # 1.0 to 0.6


def _get_seasonal_multiplier(date: datetime) -> float:
    """
    Get seasonal multiplier for heat demand.
    
    Winter months have higher demand than summer.
    
    Args:
        date: Date to check
        
    Returns:
        Seasonal multiplier (0.5-1.2)
    """
    month = date.month
    
    # Winter months (Dec, Jan, Feb): High demand
    if month in [12, 1, 2]:
        return 1.2
    # Spring/Autumn (Mar, Apr, Oct, Nov): Medium demand
    elif month in [3, 4, 10, 11]:
        return 0.9
    # Summer (May-Sep): Lower demand
    else:
        return 0.5


def _get_asset_production_base(asset_id: str, capacity: Optional[float]) -> float:
    """
    Get base production level for an asset.
    
    Uses deterministic seed based on asset_id to create
    consistent base production levels per asset.
    
    Args:
        asset_id: Asset identifier
        capacity: Asset capacity in MW
        
    Returns:
        Base production multiplier (0.3-0.9 of capacity)
    """
    if capacity is None:
        return 0.0
    
    # Use asset_id hash for deterministic base level
    random.seed(RANDOM_SEED + hash(asset_id))
    base_factor = random.uniform(0.3, 0.9)
    return capacity * base_factor


def _generate_production_value(
    asset_id: str,
    timestamp: datetime,
    asset_type: AssetType,
    capacity: Optional[float],
) -> float:
    """
    Generate a single production value for an asset.
    
    Args:
        asset_id: Asset identifier
        timestamp: Timestamp for the value
        asset_type: Type of asset
        capacity: Asset capacity in MW
        
    Returns:
        Production value in MW
    """
    if capacity is None:
        return 0.0
    
    # Get base production level for this asset
    base_production = _get_asset_production_base(asset_id, capacity)
    
    # Get daily pattern
    daily_multiplier = _get_daily_demand_pattern(timestamp.hour, timestamp.minute)
    
    # Get seasonal pattern
    seasonal_multiplier = _get_seasonal_multiplier(timestamp)
    
    # Asset type specific adjustments
    if asset_type == AssetType.ELECTRIC_BOILER:
        # Electric boilers can respond quickly, more variation
        type_variation = random.uniform(0.9, 1.1)
    elif asset_type in [AssetType.GAS_BOILER, AssetType.OIL_BOILER]:
        # Gas/oil boilers have moderate variation
        type_variation = random.uniform(0.95, 1.05)
    else:
        # Other types (storage, network) - different logic
        type_variation = 1.0
    
    # Calculate production
    production = base_production * daily_multiplier * seasonal_multiplier * type_variation
    
    # Ensure production doesn't exceed capacity
    production = min(production, capacity)
    
    # Ensure production is non-negative
    production = max(0.0, production)
    
    return round(production, 2)


def generate_historical_heat_production(
    asset_id: str,
    start_time: datetime,
    end_time: datetime,
) -> List[HeatProductionDataPoint]:
    """
    Generate historical heat production data for an asset.
    
    Args:
        asset_id: Asset identifier
        start_time: Start of the time range
        end_time: End of the time range
        
    Returns:
        List of heat production data points with 15-minute resolution
    """
    asset = get_asset_by_id(asset_id)
    if asset is None:
        return []
    
    # Only generate data for production assets
    if asset.type not in [AssetType.GAS_BOILER, AssetType.OIL_BOILER, AssetType.ELECTRIC_BOILER]:
        return []
    
    data_points = []
    current_time = start_time.replace(minute=(start_time.minute // 15) * 15, second=0, microsecond=0)
    
    # Initialize random with fixed seed for this asset
    random.seed(RANDOM_SEED + hash(asset_id))
    
    while current_time <= end_time:
        # Generate production value
        value = _generate_production_value(
            asset_id=asset_id,
            timestamp=current_time,
            asset_type=asset.type,
            capacity=asset.capacity,
        )
        
        data_points.append(HeatProductionDataPoint(
            timestamp=current_time,
            value=value,
        ))
        
        # Move to next 15-minute interval
        current_time += timedelta(minutes=15)
    
    return data_points


def generate_planned_heat_production(
    asset_id: str,
    start_time: datetime,
    end_time: datetime,
) -> List[HeatProductionDataPoint]:
    """
    Generate planned heat production data for an asset.
    
    Planned production is similar to historical but may have:
    - Slightly smoother curves (less variation)
    - More predictable patterns
    - Can be slightly different from actual (to show planning vs reality)
    
    Args:
        asset_id: Asset identifier
        start_time: Start of the planned period
        end_time: End of the planned period
        
    Returns:
        List of planned heat production data points with 15-minute resolution
    """
    asset = get_asset_by_id(asset_id)
    if asset is None:
        return []
    
    # Only generate data for production assets
    if asset.type not in [AssetType.GAS_BOILER, AssetType.OIL_BOILER, AssetType.ELECTRIC_BOILER]:
        return []
    
    data_points = []
    current_time = start_time.replace(minute=(start_time.minute // 15) * 15, second=0, microsecond=0)
    
    # Use different seed for planned vs historical (to show they can differ)
    planned_seed = RANDOM_SEED + hash(asset_id) + 1000
    random.seed(planned_seed)
    
    while current_time <= end_time:
        # Generate planned production value (slightly smoother)
        base_production = _get_asset_production_base(asset_id, asset.capacity)
        daily_multiplier = _get_daily_demand_pattern(current_time.hour, current_time.minute)
        seasonal_multiplier = _get_seasonal_multiplier(current_time)
        
        # Planned production has less variation (more predictable)
        if asset.type == AssetType.ELECTRIC_BOILER:
            type_variation = random.uniform(0.95, 1.05)  # Less variation
        elif asset.type in [AssetType.GAS_BOILER, AssetType.OIL_BOILER]:
            type_variation = random.uniform(0.97, 1.03)  # Even less variation
        else:
            type_variation = 1.0
        
        production = base_production * daily_multiplier * seasonal_multiplier * type_variation
        production = min(production, asset.capacity or 0.0)
        production = max(0.0, production)
        
        data_points.append(HeatProductionDataPoint(
            timestamp=current_time,
            value=round(production, 2),
        ))
        
        # Move to next 15-minute interval
        current_time += timedelta(minutes=15)
    
    return data_points


def get_current_heat_production(asset_id: str) -> float:
    """
    Get current (latest) heat production value for an asset.
    
    This is essentially the most recent value from historical data.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Current production value in MW
    """
    asset = get_asset_by_id(asset_id)
    if asset is None:
        return 0.0
    
    # Only generate data for production assets
    if asset.type not in [AssetType.GAS_BOILER, AssetType.OIL_BOILER, AssetType.ELECTRIC_BOILER]:
        return 0.0
    
    # Generate value for current time
    now = datetime.now()
    value = _generate_production_value(
        asset_id=asset_id,
        timestamp=now,
        asset_type=asset.type,
        capacity=asset.capacity,
    )
    
    return value

