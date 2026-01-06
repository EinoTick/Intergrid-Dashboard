import { useMemo, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { formatISO, subDays } from 'date-fns'
import { useAssets, useElectricityPrices, useHeatConsumption, useHeatConsumptionForecast, useHeatProductionHistorical, useHeatProductionPlanned, useSiteDetail, useStorageChargeDischarge, useStorageStateHistorical, useSites } from '@api/hooks'
import { Asset } from '@api/types'
import AssetCard from '@components/AssetCard'
import { AreaSeriesChart, BarSeriesChart, LineSeriesChart } from '@components/charts/TimeSeries'

export default function SiteDashboard() {
  const { siteId } = useParams()
  const navigate = useNavigate()
  const { data: allSites } = useSites()
  const { data: siteDetail, isLoading, error } = useSiteDetail(siteId)
  const { data: assets } = useAssets(siteId)

  // Time range: last 24h
  const end = new Date()
  const start = subDays(end, 1)
  const startISO = formatISO(start)
  const endISO = formatISO(end)

  const network = assets?.find(a => a.type === 'district_heating_network')
  const storageAssets = assets?.filter(a => a.type === 'heat_storage') ?? []
  const productionAssets = assets?.filter(a => ['gas_boiler','oil_boiler','electric_boiler'].includes(a.type)) ?? []

  // Electricity prices
  const { data: prices } = useElectricityPrices(startISO, endISO)
  const priceData = useMemo(() => prices?.prices?.map(p => ({ timestamp: p.timestamp, price: p.price })) ?? [], [prices])

  if (isLoading) return <div className="container"><div className="card">Loading site...</div></div>
  if (error || !siteDetail) return <div className="container"><div className="card alert danger">Failed to load site</div></div>

  return (
    <div className="container">
      <div className="header">
        <h2 style={{ margin: 0 }}>{siteDetail.site.name}</h2>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button className="button secondary" onClick={() => navigate('/')}>Back</button>
          <select
            className="select"
            style={{ width: 280 }}
            value={siteId}
            onChange={(e) => navigate(`/site/${e.target.value}`)}
          >
            {allSites?.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>
      </div>

      <div className="grid">
        {siteDetail.assets.map((a: Asset) => (
          <AssetCard key={a.id} asset={a} />
        ))}
      </div>

      {productionAssets.length > 0 && (
        <div className="card" style={{ marginTop: 16 }}>
          <h3>Production assets: Actual vs Planned (last 24h)</h3>
          {productionAssets.map(asset => (
            <ProductionCharts key={asset.id} asset={asset} startISO={startISO} endISO={endISO} />
          ))}
        </div>
      )}

      {storageAssets.length > 0 && (
        <div className="card" style={{ marginTop: 16 }}>
          <h3>Storage charge/discharge and state (last 24h)</h3>
          {storageAssets.map(asset => (
            <StorageCharts key={asset.id} asset={asset} startISO={startISO} endISO={endISO} />
          ))}
        </div>
      )}

      {network && (
        <div className="card" style={{ marginTop: 16 }}>
          <h3>Network consumption and forecast</h3>
          <NetworkCharts asset={network} startISO={startISO} endISO={endISO} />
        </div>
      )}

      <div className="card" style={{ marginTop: 16 }}>
        <h3>Electricity prices (last 24h)</h3>
        <LineSeriesChart data={priceData} series={[{ name: 'Price', dataKey: 'price', color: '#22c55e' }]} yUnit="€" />
      </div>
    </div>
  )
}

function ProductionCharts({ asset, startISO, endISO }: { asset: Asset, startISO: string, endISO: string }) {
  const { data: hist } = useHeatProductionHistorical(asset.id, startISO, endISO)
  const { data: plan } = useHeatProductionPlanned(asset.id, startISO, endISO)

  const data = useMemo(() => {
    const map = new Map<string, any>()
    hist?.data_points.forEach(p => map.set(p.timestamp, { timestamp: p.timestamp, actual: p.value }))
    plan?.data_points.forEach(p => map.set(p.timestamp, { ...(map.get(p.timestamp) || { timestamp: p.timestamp }), planned: p.value }))
    return Array.from(map.values()).sort((a, b) => a.timestamp.localeCompare(b.timestamp))
  }, [hist, plan])

  return (
    <div style={{ marginTop: 8 }}>
      <div className="small" style={{ marginBottom: 6 }}>{asset.name}</div>
      <LineSeriesChart
        data={data}
        series={[
          { name: 'Actual', dataKey: 'actual', color: '#22c55e' },
          { name: 'Planned', dataKey: 'planned', color: '#60a5fa' },
        ]}
        yUnit=" MW"
      />
    </div>
  )
}

function StorageCharts({ asset, startISO, endISO }: { asset: Asset, startISO: string, endISO: string }) {
  const { data: flow } = useStorageChargeDischarge(asset.id, startISO, endISO, false)
  const { data: state } = useStorageStateHistorical(asset.id, startISO, endISO)

  const flowData = flow?.data_points?.map(p => ({ timestamp: p.timestamp, charge: p.charge, discharge: p.discharge, net: p.net_flow })) ?? []
  const stateData = state?.data_points?.map(p => ({ timestamp: p.timestamp, soc: p.state_of_charge_percent, energy: p.stored_energy_mwh })) ?? []

  return (
    <div style={{ marginTop: 8 }}>
      <div className="small" style={{ marginBottom: 6 }}>{asset.name}</div>
      <BarSeriesChart
        data={flowData}
        series={[
          { name: 'Charge', dataKey: 'charge', color: '#60a5fa', type: 'bar' },
          { name: 'Discharge', dataKey: 'discharge', color: '#22c55e', type: 'bar' },
        ]}
        yUnit=" MW"
      />
      <AreaSeriesChart
        data={stateData}
        series={[{ name: 'State of charge %', dataKey: 'soc', color: '#f59e0b', type: 'area' }]}
        yUnit=" %"
      />
    </div>
  )
}

function NetworkCharts({ asset, startISO, endISO }: { asset: Asset, startISO: string, endISO: string }) {
  const { data: cons } = useHeatConsumption(asset.id, startISO, endISO)
  const { data: forecast } = useHeatConsumptionForecast(asset.id)

  const consData = cons?.consumption?.map(p => ({ timestamp: p.timestamp, value: p.value })) ?? []
  const forecastData = forecast?.forecast?.map(p => ({ timestamp: p.timestamp, value: p.value })) ?? []

  return (
    <div className="row">
      <div className="col">
        <div className="small" style={{ marginBottom: 6 }}>Actual consumption (last 24h)</div>
        <AreaSeriesChart data={consData} series={[{ name: 'Consumption', dataKey: 'value', color: '#ef4444' }]} yUnit=" MW" />
      </div>
      <div className="col">
        <div className="small" style={{ marginBottom: 6 }}>Forecast (next 5 days)</div>
        <LineSeriesChart data={forecastData} series={[{ name: 'Forecast', dataKey: 'value', color: '#60a5fa' }]} yUnit=" MW" />
      </div>
    </div>
  )
}
