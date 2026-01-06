import { useEffect, useState } from 'react'
import { Asset, AssetUpdate } from '@api/types'
import { useUpdateAsset } from '@api/hooks'

export default function AssetEditor({ asset, onClose }: { asset: Asset, onClose: () => void }) {
  const [form, setForm] = useState<AssetUpdate>({
    name: asset.name,
    capacity: asset.capacity ?? undefined,
    efficiency: asset.efficiency ?? undefined,
    cost_per_mwh: asset.cost_per_mwh ?? undefined,
  })
  const updateMutation = useUpdateAsset()

  useEffect(() => {
    setForm({
      name: asset.name,
      capacity: asset.capacity ?? undefined,
      efficiency: asset.efficiency ?? undefined,
      cost_per_mwh: asset.cost_per_mwh ?? undefined,
    })
  }, [asset])

  function onChange<K extends keyof AssetUpdate>(key: K, value: AssetUpdate[K]) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    await updateMutation.mutateAsync({ assetId: asset.id, patch: form })
    onClose()
  }

  return (
    <div className="card" style={{ position: 'relative' }}>
      <h3>Edit Asset</h3>
      <form className="row" onSubmit={onSubmit}>
        <div className="col">
          <div className="label">Name</div>
          <input className="input" value={form.name ?? ''} onChange={(e) => onChange('name', e.target.value)} />
        </div>
        <div className="col">
          <div className="label">Capacity {asset.type === 'heat_storage' ? '(MWh)' : '(MW)'}</div>
          <input className="input" type="number" step="0.01" value={form.capacity ?? ''} onChange={(e) => onChange('capacity', e.target.value === '' ? undefined : Number(e.target.value))} />
        </div>
        <div className="col">
          <div className="label">Efficiency (0-1)</div>
          <input className="input" type="number" step="0.01" min={0} max={1} value={form.efficiency ?? ''} onChange={(e) => onChange('efficiency', e.target.value === '' ? undefined : Number(e.target.value))} />
        </div>
        {(asset.type === 'gas_boiler' || asset.type === 'oil_boiler') && (
          <div className="col">
            <div className="label">Cost per MWh (EUR)</div>
            <input className="input" type="number" step="0.01" value={form.cost_per_mwh ?? ''} onChange={(e) => onChange('cost_per_mwh', e.target.value === '' ? undefined : Number(e.target.value))} />
          </div>
        )}
        <div className="col" style={{ alignSelf: 'flex-end', display: 'flex', gap: 8 }}>
          <button type="button" className="button secondary" onClick={onClose}>Cancel</button>
          <button type="submit" className="button">Save</button>
        </div>
      </form>
      {updateMutation.isError && <div className="alert danger" style={{ marginTop: 8 }}>Failed to update asset</div>}
    </div>
  )
}
