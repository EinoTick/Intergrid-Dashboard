"""
Industrial Automation Dashboard - Mock API

FastAPI application providing simulated data for industrial assets,
heat production, electricity prices, and consumption forecasts.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional

try:
    # Try relative import (when run as a module)
    from .models import (
        Asset,
        AssetListResponse,
        HeatProductionCurrent,
        HeatProductionHistorical,
        HeatProductionPlanned,
        ElectricityPrice,
        ElectricityPriceResponse,
        HeatConsumption,
        HeatConsumptionResponse,
        HeatConsumptionForecast,
        HeatConsumptionForecastResponse,
        Site,
        SiteListResponse,
        SiteDetailResponse,
        StorageChargeDischarge,
        StorageChargeDischargeResponse,
        StorageState,
        StorageStateDataPoint,
        StorageStateHistorical,
        AssetType,
        AssetUpdate,
    )
    from .mock_data import (
        get_all_sites,
        get_site_by_id,
        get_all_assets,
        get_assets_by_site_id,
        get_asset_by_id,
        update_asset,
    )
    from .electricity_prices import generate_electricity_prices
    from .heat_production import (
        get_current_heat_production,
        generate_historical_heat_production,
        generate_planned_heat_production,
    )
    from .storage_data import (
        generate_storage_charge_discharge,
        generate_planned_storage_charge_discharge,
        generate_historical_storage_state,
        get_storage_state,
    )
    from .heat_consumption import (
        generate_heat_consumption,
        generate_heat_consumption_forecast,
    )
except ImportError:
    # Fall back to absolute import (when run directly)
    from models import (
        Asset,
        AssetListResponse,
        HeatProductionCurrent,
        HeatProductionHistorical,
        HeatProductionPlanned,
        ElectricityPrice,
        ElectricityPriceResponse,
        HeatConsumption,
        HeatConsumptionResponse,
        HeatConsumptionForecast,
        HeatConsumptionForecastResponse,
        Site,
        SiteListResponse,
        SiteDetailResponse,
        StorageChargeDischarge,
        StorageChargeDischargeResponse,
        StorageState,
        StorageStateDataPoint,
        StorageStateHistorical,
        AssetType,
        AssetUpdate,
    )
    from mock_data import (
        get_all_sites,
        get_site_by_id,
        get_all_assets,
        get_assets_by_site_id,
        get_asset_by_id,
        update_asset,
    )
    from electricity_prices import generate_electricity_prices
    from heat_production import (
        get_current_heat_production,
        generate_historical_heat_production,
        generate_planned_heat_production,
    )
    from storage_data import (
        generate_storage_charge_discharge,
        generate_planned_storage_charge_discharge,
        generate_historical_storage_state,
        get_storage_state,
    )
    from heat_consumption import (
        generate_heat_consumption,
        generate_heat_consumption_forecast,
    )

app = FastAPI(
    title="Industrial Automation Dashboard API",
    description="Mock API for industrial automation dashboard frontend exercise",
    version="1.0.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Industrial Automation Dashboard API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/sites", response_model=SiteListResponse)
async def get_sites():
    """
    Get a list of all industrial sites.
    
    A site represents a collection of assets at one industrial location.
    This endpoint is used to allow users to select a site in the dashboard
    and view data for all assets belonging to that site.
    
    Returns:
        List of sites with their IDs, names, and associated asset IDs
    """
    sites = get_all_sites()
    return SiteListResponse(sites=sites)


@app.get("/sites/{site_id}", response_model=SiteDetailResponse)
async def get_site_detail(site_id: str):
    """
    Get detailed information about a specific site including all its assets.
    
    Args:
        site_id: Unique identifier of the site
        
    Returns:
        Site information with full details of all associated assets
    """
    site = get_site_by_id(site_id)
    if site is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Site with id '{site_id}' not found")
    
    assets = get_assets_by_site_id(site_id)
    return SiteDetailResponse(site=site, assets=assets)


@app.get("/assets", response_model=AssetListResponse)
async def get_assets(site_id: Optional[str] = None):
    """
    Get a list of industrial assets with their details.
    
    Args:
        site_id: Optional filter to get assets belonging to a specific site
        
    Returns:
        List of assets including:
        - Asset ID, name, and type
        - Capacity (for production assets)
        - Efficiency (for production assets)
        - Cost of heat production (for gas and oil boilers)
    """
    if site_id:
        assets = get_assets_by_site_id(site_id)
    else:
        assets = get_all_assets()
    return AssetListResponse(assets=assets)


@app.patch("/assets/{asset_id}", response_model=Asset)
async def update_asset_endpoint(asset_id: str, update_data: AssetUpdate):
    """
    Update asset data (name, capacity, efficiency, cost_per_mwh).
    
    Note: Asset ID and type cannot be changed. Only the following fields can be updated:
    - name: Asset name
    - capacity: Production capacity (MW) or storage capacity (MWh)
    - efficiency: Efficiency (0.0-1.0) for production assets
    - cost_per_mwh: Cost per MWh for gas and oil boilers
    
    Args:
        asset_id: Unique identifier of the asset
        update_data: Asset update data (partial update - only provided fields will be updated)
        
    Returns:
        Updated asset
    """
    from fastapi import HTTPException
    
    # Verify asset exists
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    # Convert Pydantic model to dict, excluding None values
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Update the asset
    updated_asset = update_asset(asset_id, update_dict)
    
    if updated_asset is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to update asset"
        )
    
    return updated_asset


@app.get("/assets/{asset_id}/heat-production/current", response_model=HeatProductionCurrent)
async def get_current_heat_production_endpoint(asset_id: str):
    """
    Get the latest (current) heat production measurement for a specific asset.
    
    Args:
        asset_id: Unique identifier of the asset
        
    Returns:
        Current heat production value with timestamp
    """
    from fastapi import HTTPException
    
    # Verify asset exists
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    # Get current production value
    value = get_current_heat_production(asset_id)
    
    return HeatProductionCurrent(
        asset_id=asset_id,
        value=value,
        unit="MW",
        timestamp=datetime.now(),
    )


@app.get("/assets/{asset_id}/heat-production/historical", response_model=HeatProductionHistorical)
async def get_historical_heat_production(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get historical heat production data for a specific heat production asset.
    
    Args:
        asset_id: Unique identifier of the asset
        start_time: Start of the time range (defaults to 24 hours ago)
        end_time: End of the time range (defaults to now)
        
    Returns:
        Historical heat production data points with 15-minute resolution
    """
    from fastapi import HTTPException
    
    # Verify asset exists
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if start_time is None:
        start_time = datetime.now() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.now()
    
    # Generate historical production data
    data_points = generate_historical_heat_production(asset_id, start_time, end_time)
    
    return HeatProductionHistorical(
        asset_id=asset_id,
        data_points=data_points,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
    )


@app.get("/assets/{asset_id}/heat-production/planned", response_model=HeatProductionPlanned)
async def get_planned_heat_production(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get planned heat production data for a specific heat production asset.
    
    Planned production represents the scheduled/planned heat production
    for future time periods, typically used for operational planning.
    Planned values may differ slightly from actual historical values to
    demonstrate the difference between planned and actual production.
    
    Args:
        asset_id: Unique identifier of the asset
        start_time: Start of the planned period (defaults to now)
        end_time: End of the planned period (defaults to 7 days from now)
        
    Returns:
        Planned heat production data points with 15-minute resolution
    """
    from fastapi import HTTPException
    
    # Verify asset exists
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if start_time is None:
        start_time = datetime.now()
    if end_time is None:
        end_time = datetime.now() + timedelta(days=7)
    
    # Generate planned production data
    data_points = generate_planned_heat_production(asset_id, start_time, end_time)
    
    return HeatProductionPlanned(
        asset_id=asset_id,
        data_points=data_points,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
    )


@app.get("/electricity-prices", response_model=ElectricityPriceResponse)
async def get_electricity_prices(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get electricity prices in 15-minute resolution.
    
    Uses deterministic price generation with fixed seed to ensure reproducibility.
    Prices follow realistic patterns:
    - Daily patterns with peaks during morning (06:00-09:00) and evening (17:00-20:00)
    - Lower prices during night hours
    - Weekend prices typically lower than weekdays
    - Some days have flat prices (constant throughout the day)
    - Some days have constantly high prices
    
    Args:
        start_time: Start of the time range (defaults to 24 hours ago)
        end_time: End of the time range (defaults to now)
        
    Returns:
        Electricity prices with 15-minute resolution
    """
    if start_time is None:
        start_time = datetime.now() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.now()
    
    # Generate deterministic electricity prices
    prices = generate_electricity_prices(start_time, end_time)
    
    return ElectricityPriceResponse(
        prices=prices,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
        currency="EUR",
        unit="MWh",
    )


@app.get("/assets/{asset_id}/storage/charge-discharge", response_model=StorageChargeDischargeResponse)
async def get_storage_charge_discharge(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get storage charge/discharge data for a specific storage asset.
    
    Charge represents heat being stored (consumption), discharge represents
    heat being released (production). Net flow = discharge - charge.
    
    Args:
        asset_id: Unique identifier of the storage asset
        start_time: Start of the time range (defaults to 24 hours ago)
        end_time: End of the time range (defaults to now)
        
    Returns:
        Storage charge/discharge data with 15-minute resolution
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if asset.type != AssetType.HEAT_STORAGE:
        raise HTTPException(
            status_code=400,
            detail=f"Asset '{asset_id}' is not a storage asset"
        )
    
    if start_time is None:
        start_time = datetime.now() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.now()
    
    # Find site for this asset
    sites = get_all_sites()
    site_id = None
    for site in sites:
        if asset_id in site.asset_ids:
            site_id = site.id
            break
    
    data_points = generate_storage_charge_discharge(asset_id, start_time, end_time, site_id)
    
    return StorageChargeDischargeResponse(
        asset_id=asset_id,
        data_points=data_points,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
    )


@app.get("/assets/{asset_id}/storage/charge-discharge/planned", response_model=StorageChargeDischargeResponse)
async def get_planned_storage_charge_discharge(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get planned storage charge/discharge data for a specific storage asset.
    
    Planned charge/discharge represents scheduled storage operations for future periods.
    Energy balance is maintained per site.
    
    Args:
        asset_id: Unique identifier of the storage asset
        start_time: Start of the planned period (defaults to now)
        end_time: End of the planned period (defaults to 7 days from now)
        
    Returns:
        Planned storage charge/discharge data with 15-minute resolution
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if asset.type != AssetType.HEAT_STORAGE:
        raise HTTPException(
            status_code=400,
            detail=f"Asset '{asset_id}' is not a storage asset"
        )
    
    if start_time is None:
        start_time = datetime.now()
    if end_time is None:
        end_time = datetime.now() + timedelta(days=7)
    
    # Find site for this asset
    sites = get_all_sites()
    site_id = None
    for site in sites:
        if asset_id in site.asset_ids:
            site_id = site.id
            break
    
    data_points = generate_planned_storage_charge_discharge(asset_id, start_time, end_time, site_id)
    
    return StorageChargeDischargeResponse(
        asset_id=asset_id,
        data_points=data_points,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
    )


@app.get("/assets/{asset_id}/storage/state", response_model=StorageState)
async def get_storage_state_endpoint(asset_id: str):
    """
    Get current storage state for a specific storage asset.
    
    Args:
        asset_id: Unique identifier of the storage asset
        
    Returns:
        Current storage state including stored energy, capacity, and state of charge
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if asset.type != AssetType.HEAT_STORAGE:
        raise HTTPException(
            status_code=400,
            detail=f"Asset '{asset_id}' is not a storage asset"
        )
    
    state = get_storage_state(asset_id)
    if state is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve storage state"
        )
    
    return StorageState(
        asset_id=asset_id,
        stored_energy_mwh=state["stored_energy_mwh"],
        capacity_mwh=state["capacity_mwh"],
        state_of_charge_percent=state["state_of_charge_percent"],
        timestamp=datetime.now(),
    )


@app.get("/assets/{asset_id}/storage/state/historical", response_model=StorageStateHistorical)
async def get_historical_storage_state(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get historical storage state data for a specific storage asset.
    
    Storage state is calculated from charge/discharge history to ensure consistency.
    Energy balance is maintained per site.
    
    Args:
        asset_id: Unique identifier of the storage asset
        start_time: Start of the time range (defaults to 24 hours ago)
        end_time: End of the time range (defaults to now)
        
    Returns:
        Historical storage state data with 15-minute resolution
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if asset.type != AssetType.HEAT_STORAGE:
        raise HTTPException(
            status_code=400,
            detail=f"Asset '{asset_id}' is not a storage asset"
        )
    
    if asset.capacity is None:
        raise HTTPException(
            status_code=500,
            detail="Storage asset has no capacity defined"
        )
    
    if start_time is None:
        start_time = datetime.now() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.now()
    
    # Find site for this asset
    sites = get_all_sites()
    site_id = None
    for site in sites:
        if asset_id in site.asset_ids:
            site_id = site.id
            break
    
    state_data_points = generate_historical_storage_state(asset_id, start_time, end_time, site_id)
    
    return StorageStateHistorical(
        asset_id=asset_id,
        capacity_mwh=asset.capacity,
        data_points=state_data_points,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
    )


@app.get("/assets/{asset_id}/heat-consumption", response_model=HeatConsumptionResponse)
async def get_heat_consumption(
    asset_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    """
    Get heat consumption for a specific asset.
    
    For District Heating Networks: Shows actual consumption (demand).
    Consumption is calculated to maintain energy balance:
    Consumption = Production + Storage Discharge - Storage Charge
    
    For Storage Assets: Shows charge rate (consumption when charging).
    
    For Production Assets: Returns empty (they produce, not consume).
    
    Args:
        asset_id: Unique identifier of the asset
        start_time: Start of the time range (defaults to 24 hours ago)
        end_time: End of the time range (defaults to now)
        
    Returns:
        Heat consumption data for the asset with 15-minute resolution
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    if start_time is None:
        start_time = datetime.now() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.now()
    
    consumption_data = generate_heat_consumption(asset_id, start_time, end_time)
    
    return HeatConsumptionResponse(
        asset_id=asset_id,
        consumption=consumption_data,
        start_time=start_time,
        end_time=end_time,
        resolution_minutes=15,
        unit="MW",
    )


@app.get("/assets/{asset_id}/heat-consumption/forecast", response_model=HeatConsumptionForecastResponse)
async def get_heat_consumption_forecast(asset_id: str):
    """
    Get forecasted heat consumption for a specific asset for the next 5 days.
    
    Args:
        asset_id: Unique identifier of the asset
        
    Returns:
        Forecasted heat consumption data with 15-minute resolution
        covering the next 5 days from the current time
    """
    from fastapi import HTTPException
    
    asset = get_asset_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset with id '{asset_id}' not found")
    
    now = datetime.now()
    forecast_end = now + timedelta(days=5)
    
    forecast_data = generate_heat_consumption_forecast(asset_id, now, forecast_end)
    
    return HeatConsumptionForecastResponse(
        asset_id=asset_id,
        forecast=forecast_data,
        forecast_start=now,
        forecast_end=forecast_end,
        resolution_minutes=15,
        unit="MW",
    )

