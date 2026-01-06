"""
Mock data for industrial automation dashboard API.

Contains predefined sites and assets for testing and demonstration.
"""

from typing import Dict, List, Optional

try:
    from .models import Asset, Site, AssetType
except ImportError:
    from models import Asset, Site, AssetType


# Mock assets data
MOCK_ASSETS: Dict[str, Asset] = {
    # Site 1: Helsinki Central District Heating Plant (Small)
    "asset_001": Asset(
        id="asset_001",
        name="Primary Gas Boiler Unit 1",
        type=AssetType.GAS_BOILER,
        capacity=35.0,
        efficiency=0.91,
        cost_per_mwh=42.5,
    ),
    "asset_002": Asset(
        id="asset_002",
        name="Heat Storage Tank Alpha",
        type=AssetType.HEAT_STORAGE,
        capacity=150.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_003": Asset(
        id="asset_003",
        name="Helsinki Central Network",
        type=AssetType.DISTRICT_HEATING_NETWORK,
        capacity=None,
        efficiency=None,
        cost_per_mwh=None,
    ),
    
    # Site 2: Espoo Industrial Heating Facility (Medium)
    "asset_004": Asset(
        id="asset_004",
        name="Main Gas Boiler A",
        type=AssetType.GAS_BOILER,
        capacity=50.0,
        efficiency=0.93,
        cost_per_mwh=41.8,
    ),
    "asset_005": Asset(
        id="asset_005",
        name="Main Gas Boiler B",
        type=AssetType.GAS_BOILER,
        capacity=50.0,
        efficiency=0.92,
        cost_per_mwh=42.2,
    ),
    "asset_006": Asset(
        id="asset_006",
        name="Electric Boiler Unit 1",
        type=AssetType.ELECTRIC_BOILER,
        capacity=30.0,
        efficiency=0.98,
        cost_per_mwh=None,
    ),
    "asset_007": Asset(
        id="asset_007",
        name="Thermal Storage Beta",
        type=AssetType.HEAT_STORAGE,
        capacity=200.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_008": Asset(
        id="asset_008",
        name="Espoo District Network",
        type=AssetType.DISTRICT_HEATING_NETWORK,
        capacity=None,
        efficiency=None,
        cost_per_mwh=None,
    ),
    
    # Site 3: Tampere Regional Heating Complex (Large)
    "asset_009": Asset(
        id="asset_009",
        name="Gas Boiler Unit 1",
        type=AssetType.GAS_BOILER,
        capacity=60.0,
        efficiency=0.94,
        cost_per_mwh=40.5,
    ),
    "asset_010": Asset(
        id="asset_010",
        name="Gas Boiler Unit 2",
        type=AssetType.GAS_BOILER,
        capacity=60.0,
        efficiency=0.93,
        cost_per_mwh=41.0,
    ),
    "asset_011": Asset(
        id="asset_011",
        name="Gas Boiler Unit 3",
        type=AssetType.GAS_BOILER,
        capacity=55.0,
        efficiency=0.92,
        cost_per_mwh=41.5,
    ),
    "asset_012": Asset(
        id="asset_012",
        name="Electric Boiler Primary",
        type=AssetType.ELECTRIC_BOILER,
        capacity=40.0,
        efficiency=0.99,
        cost_per_mwh=None,
    ),
    "asset_013": Asset(
        id="asset_013",
        name="Electric Boiler Secondary",
        type=AssetType.ELECTRIC_BOILER,
        capacity=35.0,
        efficiency=0.98,
        cost_per_mwh=None,
    ),
    "asset_014": Asset(
        id="asset_014",
        name="Oil Boiler Reserve",
        type=AssetType.OIL_BOILER,
        capacity=45.0,
        efficiency=0.88,
        cost_per_mwh=55.2,
    ),
    "asset_015": Asset(
        id="asset_015",
        name="Storage Tank Gamma",
        type=AssetType.HEAT_STORAGE,
        capacity=250.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_016": Asset(
        id="asset_016",
        name="Storage Tank Delta",
        type=AssetType.HEAT_STORAGE,
        capacity=250.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_017": Asset(
        id="asset_017",
        name="Tampere Regional Network",
        type=AssetType.DISTRICT_HEATING_NETWORK,
        capacity=None,
        efficiency=None,
        cost_per_mwh=None,
    ),
    
    # Site 4: Oulu Northern Heating Station (Medium-Large)
    "asset_018": Asset(
        id="asset_018",
        name="Gas Boiler North",
        type=AssetType.GAS_BOILER,
        capacity=55.0,
        efficiency=0.92,
        cost_per_mwh=43.0,
    ),
    "asset_019": Asset(
        id="asset_019",
        name="Gas Boiler South",
        type=AssetType.GAS_BOILER,
        capacity=55.0,
        efficiency=0.91,
        cost_per_mwh=43.5,
    ),
    "asset_020": Asset(
        id="asset_020",
        name="Oil Boiler Backup",
        type=AssetType.OIL_BOILER,
        capacity=40.0,
        efficiency=0.87,
        cost_per_mwh=56.8,
    ),
    "asset_021": Asset(
        id="asset_021",
        name="Electric Boiler Unit",
        type=AssetType.ELECTRIC_BOILER,
        capacity=25.0,
        efficiency=0.97,
        cost_per_mwh=None,
    ),
    "asset_022": Asset(
        id="asset_022",
        name="Heat Storage Epsilon",
        type=AssetType.HEAT_STORAGE,
        capacity=180.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_023": Asset(
        id="asset_023",
        name="Oulu District Network",
        type=AssetType.DISTRICT_HEATING_NETWORK,
        capacity=None,
        efficiency=None,
        cost_per_mwh=None,
    ),
    
    # Site 5: Turku Coastal Heating Plant (Small-Medium)
    "asset_024": Asset(
        id="asset_024",
        name="Main Gas Boiler",
        type=AssetType.GAS_BOILER,
        capacity=45.0,
        efficiency=0.90,
        cost_per_mwh=44.2,
    ),
    "asset_025": Asset(
        id="asset_025",
        name="Electric Boiler",
        type=AssetType.ELECTRIC_BOILER,
        capacity=28.0,
        efficiency=0.98,
        cost_per_mwh=None,
    ),
    "asset_026": Asset(
        id="asset_026",
        name="Storage Tank Zeta",
        type=AssetType.HEAT_STORAGE,
        capacity=120.0,  # Storage capacity in MWh
        efficiency=None,
        cost_per_mwh=None,
    ),
    "asset_027": Asset(
        id="asset_027",
        name="Turku Coastal Network",
        type=AssetType.DISTRICT_HEATING_NETWORK,
        capacity=None,
        efficiency=None,
        cost_per_mwh=None,
    ),
}

# Mock sites data
MOCK_SITES: Dict[str, Site] = {
    "site_001": Site(
        id="site_001",
        name="Helsinki Central District Heating Plant",
        asset_ids=["asset_001", "asset_002", "asset_003"],
    ),
    "site_002": Site(
        id="site_002",
        name="Espoo Industrial Heating Facility",
        asset_ids=["asset_004", "asset_005", "asset_006", "asset_007", "asset_008"],
    ),
    "site_003": Site(
        id="site_003",
        name="Tampere Regional Heating Complex",
        asset_ids=[
            "asset_009", "asset_010", "asset_011", "asset_012", "asset_013",
            "asset_014", "asset_015", "asset_016", "asset_017",
        ],
    ),
    "site_004": Site(
        id="site_004",
        name="Oulu Northern Heating Station",
        asset_ids=["asset_018", "asset_019", "asset_020", "asset_021", "asset_022", "asset_023"],
    ),
    "site_005": Site(
        id="site_005",
        name="Turku Coastal Heating Plant",
        asset_ids=["asset_024", "asset_025", "asset_026", "asset_027"],
    ),
}


def get_all_sites() -> List[Site]:
    """Get all sites."""
    return list(MOCK_SITES.values())


def get_site_by_id(site_id: str) -> Optional[Site]:
    """Get a site by its ID."""
    return MOCK_SITES.get(site_id)


def get_all_assets() -> List[Asset]:
    """Get all assets."""
    return list(MOCK_ASSETS.values())


def get_assets_by_ids(asset_ids: List[str]) -> List[Asset]:
    """Get assets by their IDs."""
    return [MOCK_ASSETS[asset_id] for asset_id in asset_ids if asset_id in MOCK_ASSETS]


def get_assets_by_site_id(site_id: str) -> List[Asset]:
    """Get all assets belonging to a specific site."""
    site = MOCK_SITES.get(site_id)
    if site is None:
        return []
    return get_assets_by_ids(site.asset_ids)


def get_asset_by_id(asset_id: str) -> Optional[Asset]:
    """Get an asset by its ID."""
    return MOCK_ASSETS.get(asset_id)


def update_asset(asset_id: str, update_data: dict) -> Optional[Asset]:
    """
    Update an asset with new data.
    
    Note: Asset ID and type cannot be changed.
    Only name, capacity, efficiency, and cost_per_mwh can be updated.
    
    Args:
        asset_id: Asset identifier
        update_data: Dictionary with fields to update
        
    Returns:
        Updated asset or None if asset not found
    """
    asset = MOCK_ASSETS.get(asset_id)
    if asset is None:
        return None
    
    # Create updated asset data
    updated_data = asset.model_dump()
    
    # Update only provided fields
    if "name" in update_data and update_data["name"] is not None:
        updated_data["name"] = update_data["name"]
    if "capacity" in update_data:
        updated_data["capacity"] = update_data["capacity"]  # Allow None
    if "efficiency" in update_data:
        updated_data["efficiency"] = update_data["efficiency"]  # Allow None
    if "cost_per_mwh" in update_data:
        updated_data["cost_per_mwh"] = update_data["cost_per_mwh"]  # Allow None
    
    # Create new asset instance with updated data
    updated_asset = Asset(**updated_data)
    
    # Update in dictionary
    MOCK_ASSETS[asset_id] = updated_asset
    
    return updated_asset

