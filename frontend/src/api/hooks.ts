import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from './client'
import type {
  Asset, AssetListResponse, AssetUpdate,
  SiteListResponse, SiteDetailResponse,
  HeatProductionHistorical, HeatProductionPlanned, HeatProductionCurrent,
  ElectricityPriceResponse,
  StorageChargeDischargeResponse, StorageState, StorageStateHistorical,
  HeatConsumptionResponse, HeatConsumptionForecastResponse
} from './types'

// Sites
export function useSites() {
  return useQuery({
    queryKey: ['sites'],
    queryFn: async () => (await api.get<SiteListResponse>('/sites')).data.sites,
  })
}
export function useSiteDetail(siteId?: string) {
  return useQuery({
    queryKey: ['site', siteId],
    queryFn: async () => (await api.get<SiteDetailResponse>(`/sites/${siteId}`)).data,
    enabled: !!siteId,
  })
}

// Assets
export function useAssets(siteId?: string) {
  return useQuery({
    queryKey: ['assets', siteId],
    queryFn: async () => {
      const url = siteId ? `/assets?site_id=${encodeURIComponent(siteId)}` : '/assets'
      return (await api.get<AssetListResponse>(url)).data.assets
    },
  })
}

export function useUpdateAsset() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ assetId, patch }: { assetId: string; patch: Partial<AssetUpdate> }) => {
      const { data } = await api.patch<Asset>(`/assets/${assetId}`, patch)
      return data
    },
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['assets'] })
      qc.invalidateQueries({ queryKey: ['site'] })
      qc.invalidateQueries()
      return data
    },
  })
}

// Heat production
export function useHeatProductionHistorical(assetId?: string, start?: string, end?: string) {
  return useQuery({
    queryKey: ['heatProductionHistorical', assetId, start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const { data } = await api.get<HeatProductionHistorical>(`/assets/${assetId}/heat-production/historical`, { params })
      return data
    },
    enabled: !!assetId,
  })
}
export function useHeatProductionPlanned(assetId?: string, start?: string, end?: string) {
  return useQuery({
    queryKey: ['heatProductionPlanned', assetId, start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const { data } = await api.get<HeatProductionPlanned>(`/assets/${assetId}/heat-production/planned`, { params })
      return data
    },
    enabled: !!assetId,
  })
}
export function useHeatProductionCurrent(assetId?: string) {
  return useQuery({
    queryKey: ['heatProductionCurrent', assetId],
    queryFn: async () => (await api.get<HeatProductionCurrent>(`/assets/${assetId}/heat-production/current`)).data,
    enabled: !!assetId,
    refetchInterval: 15000,
  })
}

// Electricity prices
export function useElectricityPrices(start?: string, end?: string) {
  return useQuery({
    queryKey: ['electricityPrices', start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const { data } = await api.get<ElectricityPriceResponse>('/electricity-prices', { params })
      return data
    },
  })
}

// Storage
export function useStorageState(assetId?: string) {
  return useQuery({
    queryKey: ['storageState', assetId],
    queryFn: async () => (await api.get<StorageState>(`/assets/${assetId}/storage/state`)).data,
    enabled: !!assetId,
    refetchInterval: 30000,
  })
}
export function useStorageStateHistorical(assetId?: string, start?: string, end?: string) {
  return useQuery({
    queryKey: ['storageStateHistorical', assetId, start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const { data } = await api.get<StorageStateHistorical>(`/assets/${assetId}/storage/state/historical`, { params })
      return data
    },
    enabled: !!assetId,
  })
}
export function useStorageChargeDischarge(assetId?: string, start?: string, end?: string, planned?: boolean) {
  return useQuery({
    queryKey: ['storageChargeDischarge', planned ? 'planned' : 'actual', assetId, start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const endpoint = planned ? `/assets/${assetId}/storage/charge-discharge/planned` : `/assets/${assetId}/storage/charge-discharge`
      const { data } = await api.get<StorageChargeDischargeResponse>(endpoint, { params })
      return data
    },
    enabled: !!assetId,
  })
}

// Consumption
export function useHeatConsumption(assetId?: string, start?: string, end?: string) {
  return useQuery({
    queryKey: ['heatConsumption', assetId, start, end],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (start) params.set('start_time', start)
      if (end) params.set('end_time', end)
      const { data } = await api.get<HeatConsumptionResponse>(`/assets/${assetId}/heat-consumption`, { params })
      return data
    },
    enabled: !!assetId,
  })
}
export function useHeatConsumptionForecast(assetId?: string) {
  return useQuery({
    queryKey: ['heatConsumptionForecast', assetId],
    queryFn: async () => (await api.get<HeatConsumptionForecastResponse>(`/assets/${assetId}/heat-consumption/forecast`)).data,
    enabled: !!assetId,
  })
}
