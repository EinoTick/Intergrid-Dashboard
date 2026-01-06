import { useState } from 'react'
import { Asset } from '@api/types'
import { useHeatProductionCurrent, useStorageState } from '@api/hooks'
import StorageAlert from './StorageAlert'
import AssetEditor from './AssetEditor'

function AssetMeta({ asset }: { asset: Asset }) {
  return (
    <div className="small">
      <div>Type: <span className="badge">{asset.type}</span></div>
      {asset.capacity != null && <div>Capacity: {asset.capacity} {asset.type === 'heat_storage' ? 'MWh' : 'MW'}</div>}
      {asset.efficiency != null && <div>Efficiency: {(asset.efficiency * 100).toFixed(1)}%</div>}
      {asset.cost_per_mwh != null && <div>Cost: €{asset.cost_per_mwh}/MWh</div>}
    </div>
  )
}

export default function AssetCard({ asset }: { asset: Asset }) {
  const [editing, setEditing] = useState(false)
  const { data: current } = useHeatProductionCurrent(asset.id)
  const { data: storage } = useStorageState(asset.id)

  return (
    <div className="card">
      <div className="header">
        <h3 style={{ margin: 0 }}>{asset.name}</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="button secondary" onClick={() => setEditing(v => !v)}>{editing ? 'Close' : 'Edit'}</button>
        </div>
      </div>

      <AssetMeta asset={asset} />

      {(asset.type === 'gas_boiler' || asset.type === 'oil_boiler' || asset.type === 'electric_boiler') && (
        <div className="alert" style={{ marginTop: 8 }}>Current production: <strong>{current?.value?.toFixed(2) ?? '—'} MW</strong></div>
      )}

      {asset.type === 'heat_storage' && (
        <div style={{ marginTop: 8 }}>
          {storage && <StorageAlert stateOfCharge={storage.state_of_charge_percent} />}
          <div className="small" style={{ marginTop: 8 }}>
            Stored: {storage?.stored_energy_mwh ?? '—'} MWh / Capacity: {storage?.capacity_mwh ?? asset.capacity ?? '—'} MWh
          </div>
        </div>
      )}

      {editing && <div style={{ marginTop: 12 }}><AssetEditor asset={asset} onClose={() => setEditing(false)} /></div>}
    </div>
  )
}
