export type AssetType =
  | 'electric_boiler'
  | 'gas_boiler'
  | 'oil_boiler'
  | 'heat_storage'
  | 'district_heating_network'

export interface Asset {
  id: string
  name: string
  type: AssetType
  capacity?: number | null
  efficiency?: number | null
  cost_per_mwh?: number | null
}

export interface Site {
  id: string
  name: string
  asset_ids: string[]
}

export interface SiteListResponse { sites: Site[] }
export interface SiteDetailResponse { site: Site; assets: Asset[] }
export interface AssetListResponse { assets: Asset[] }

export interface HeatProductionPoint { timestamp: string; value: number }
export interface HeatProductionHistorical {
  asset_id: string
  data_points: HeatProductionPoint[]
  start_time: string
  end_time: string
  resolution_minutes: number
}
export interface HeatProductionPlanned extends HeatProductionHistorical {}
export interface HeatProductionCurrent { asset_id: string; value: number; unit: string; timestamp: string }

export interface ElectricityPrice { timestamp: string; price: number }
export interface ElectricityPriceResponse {
  prices: ElectricityPrice[]
  start_time: string
  end_time: string
  resolution_minutes: number
  currency: string
  unit: string
}

export interface StorageChargeDischarge { timestamp: string; charge: number; discharge: number; net_flow: number }
export interface StorageChargeDischargeResponse {
  asset_id: string
  data_points: StorageChargeDischarge[]
  start_time: string
  end_time: string
  resolution_minutes: number
}

export interface StorageState { asset_id: string; stored_energy_mwh: number; capacity_mwh: number; state_of_charge_percent: number; timestamp: string }
export interface StorageStateDataPoint { timestamp: string; stored_energy_mwh: number; state_of_charge_percent: number }
export interface StorageStateHistorical {
  asset_id: string
  capacity_mwh: number
  data_points: StorageStateDataPoint[]
  start_time: string
  end_time: string
  resolution_minutes: number
}

export interface HeatConsumption { timestamp: string; value: number }
export interface HeatConsumptionResponse {
  asset_id: string
  consumption: HeatConsumption[]
  start_time: string
  end_time: string
  resolution_minutes: number
  unit: string
}
export interface HeatConsumptionForecast { timestamp: string; value: number }
export interface HeatConsumptionForecastResponse {
  asset_id: string
  forecast: HeatConsumptionForecast[]
  forecast_start: string
  forecast_end: string
  resolution_minutes: number
  unit: string
}

export type AssetUpdate = Partial<Pick<Asset, 'name' | 'capacity' | 'efficiency' | 'cost_per_mwh'>>
