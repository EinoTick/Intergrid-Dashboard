"""
Pydantic models for API request and response schemas.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class AssetType(str, Enum):
    """Types of industrial assets."""
    ELECTRIC_BOILER = "electric_boiler"
    GAS_BOILER = "gas_boiler"
    OIL_BOILER = "oil_boiler"
    HEAT_STORAGE = "heat_storage"
    DISTRICT_HEATING_NETWORK = "district_heating_network"


class Asset(BaseModel):
    """Industrial asset information."""
    id: str = Field(..., description="Unique asset identifier")
    name: str = Field(..., description="Human-readable asset name")
    type: AssetType = Field(..., description="Type of the asset")
    capacity: Optional[float] = Field(
        None,
        description="Production capacity in MW (for production assets) or storage capacity in MWh (for storage assets)",
    )
    efficiency: Optional[float] = Field(
        None,
        description="Efficiency as a decimal (0.0-1.0) for production assets",
        ge=0.0,
        le=1.0,
    )
    cost_per_mwh: Optional[float] = Field(
        None,
        description="Cost of heat production per MWh in EUR (for gas and oil boilers)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "asset_001",
                "name": "Main Gas Boiler",
                "type": "gas_boiler",
                "capacity": 50.0,
                "efficiency": 0.92,
                "cost_per_mwh": 45.5,
            }
        }


class AssetListResponse(BaseModel):
    """Response containing a list of assets."""
    assets: List[Asset] = Field(..., description="List of all assets")


class AssetUpdate(BaseModel):
    """Request model for updating asset data."""
    name: Optional[str] = Field(None, description="Human-readable asset name")
    capacity: Optional[float] = Field(
        None,
        description="Production capacity in MW (for production assets) or storage capacity in MWh (for storage assets)",
    )
    efficiency: Optional[float] = Field(
        None,
        description="Efficiency as a decimal (0.0-1.0) for production assets",
        ge=0.0,
        le=1.0,
    )
    cost_per_mwh: Optional[float] = Field(
        None,
        description="Cost of heat production per MWh in EUR (for gas and oil boilers)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Gas Boiler Name",
                "capacity": 55.0,
                "efficiency": 0.93,
                "cost_per_mwh": 44.0,
            }
        }


class HeatProductionCurrent(BaseModel):
    """Current heat production measurement."""
    asset_id: str = Field(..., description="Asset identifier")
    value: float = Field(..., description="Current heat production value", ge=0.0)
    unit: str = Field(default="MW", description="Unit of measurement")
    timestamp: datetime = Field(..., description="Timestamp of the measurement")

    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": "asset_001",
                "value": 42.5,
                "unit": "MW",
                "timestamp": "2024-01-15T10:30:00Z",
            }
        }


class HeatProductionDataPoint(BaseModel):
    """Single data point in historical heat production."""
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    value: float = Field(..., description="Heat production value", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "value": 42.5,
            }
        }


class HeatProductionHistorical(BaseModel):
    """Historical heat production data."""
    asset_id: str = Field(..., description="Asset identifier")
    data_points: List[HeatProductionDataPoint] = Field(
        ..., description="Historical data points"
    )
    start_time: datetime = Field(..., description="Start of the time range")
    end_time: datetime = Field(..., description="End of the time range")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )


class HeatProductionPlanned(BaseModel):
    """Planned heat production data."""
    asset_id: str = Field(..., description="Asset identifier")
    data_points: List[HeatProductionDataPoint] = Field(
        ..., description="Planned production data points"
    )
    start_time: datetime = Field(..., description="Start of the planned period")
    end_time: datetime = Field(..., description="End of the planned period")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )


class ElectricityPrice(BaseModel):
    """Single electricity price data point."""
    timestamp: datetime = Field(..., description="Timestamp of the price")
    price: float = Field(..., description="Electricity price", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "price": 85.5,
            }
        }


class ElectricityPriceResponse(BaseModel):
    """Response containing electricity prices."""
    prices: List[ElectricityPrice] = Field(..., description="List of price data points")
    start_time: datetime = Field(..., description="Start of the time range")
    end_time: datetime = Field(..., description="End of the time range")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )
    currency: str = Field(default="EUR", description="Currency of the prices")
    unit: str = Field(default="MWh", description="Unit for the price")


class HeatConsumption(BaseModel):
    """Single heat consumption data point."""
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    value: float = Field(..., description="Heat consumption value", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "value": 120.5,
            }
        }


class HeatConsumptionResponse(BaseModel):
    """Response containing heat consumption data."""
    asset_id: str = Field(..., description="Asset identifier")
    consumption: List[HeatConsumption] = Field(
        ..., description="List of consumption data points"
    )
    start_time: datetime = Field(..., description="Start of the time range")
    end_time: datetime = Field(..., description="End of the time range")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )
    unit: str = Field(default="MW", description="Unit of measurement")


class HeatConsumptionForecast(BaseModel):
    """Single forecasted heat consumption data point."""
    timestamp: datetime = Field(..., description="Timestamp of the forecast")
    value: float = Field(..., description="Forecasted heat consumption value", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-20T10:30:00Z",
                "value": 125.0,
            }
        }


class HeatConsumptionForecastResponse(BaseModel):
    """Response containing heat consumption forecast."""
    asset_id: str = Field(..., description="Asset identifier")
    forecast: List[HeatConsumptionForecast] = Field(
        ..., description="List of forecasted consumption data points"
    )
    forecast_start: datetime = Field(..., description="Start of the forecast period")
    forecast_end: datetime = Field(..., description="End of the forecast period")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )
    unit: str = Field(default="MW", description="Unit of measurement")


class Site(BaseModel):
    """Industrial site information."""
    id: str = Field(..., description="Unique site identifier")
    name: str = Field(..., description="Human-readable site name")
    asset_ids: List[str] = Field(
        ..., description="List of asset IDs belonging to this site"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "site_001",
                "name": "Helsinki District Heating Plant",
                "asset_ids": ["asset_001", "asset_002", "asset_003"],
            }
        }


class SiteListResponse(BaseModel):
    """Response containing a list of sites."""
    sites: List[Site] = Field(..., description="List of all sites")


class SiteDetailResponse(BaseModel):
    """Response containing detailed site information with assets."""
    site: Site = Field(..., description="Site information")
    assets: List[Asset] = Field(..., description="List of assets belonging to this site")


class StorageChargeDischarge(BaseModel):
    """Single storage charge/discharge data point."""
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    charge: float = Field(..., description="Charge rate in MW (heat being stored, positive value)", ge=0.0)
    discharge: float = Field(..., description="Discharge rate in MW (heat being released, positive value)", ge=0.0)
    net_flow: float = Field(..., description="Net flow: discharge - charge (positive = discharging, negative = charging)")

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "charge": 5.0,
                "discharge": 0.0,
                "net_flow": -5.0,
            }
        }


class StorageChargeDischargeResponse(BaseModel):
    """Response containing storage charge/discharge data."""
    asset_id: str = Field(..., description="Asset identifier")
    data_points: List[StorageChargeDischarge] = Field(
        ..., description="List of charge/discharge data points"
    )
    start_time: datetime = Field(..., description="Start of the time range")
    end_time: datetime = Field(..., description="End of the time range")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )


class StorageState(BaseModel):
    """Current storage state."""
    asset_id: str = Field(..., description="Asset identifier")
    stored_energy_mwh: float = Field(..., description="Current stored energy in MWh", ge=0.0)
    capacity_mwh: float = Field(..., description="Storage capacity in MWh", ge=0.0)
    state_of_charge_percent: float = Field(
        ..., description="State of charge as percentage (0-100)", ge=0.0, le=100.0
    )
    timestamp: datetime = Field(..., description="Timestamp of the measurement")

    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": "asset_002",
                "stored_energy_mwh": 120.5,
                "capacity_mwh": 200.0,
                "state_of_charge_percent": 60.25,
                "timestamp": "2024-01-15T10:30:00Z",
            }
        }


class StorageStateDataPoint(BaseModel):
    """Single storage state data point."""
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    stored_energy_mwh: float = Field(..., description="Stored energy in MWh", ge=0.0)
    state_of_charge_percent: float = Field(
        ..., description="State of charge as percentage (0-100)", ge=0.0, le=100.0
    )

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "stored_energy_mwh": 120.5,
                "state_of_charge_percent": 60.25,
            }
        }


class StorageStateHistorical(BaseModel):
    """Historical storage state data."""
    asset_id: str = Field(..., description="Asset identifier")
    capacity_mwh: float = Field(..., description="Storage capacity in MWh", ge=0.0)
    data_points: List[StorageStateDataPoint] = Field(
        ..., description="Historical state data points"
    )
    start_time: datetime = Field(..., description="Start of the time range")
    end_time: datetime = Field(..., description="End of the time range")
    resolution_minutes: int = Field(
        default=15, description="Time resolution in minutes"
    )

