import { useState } from 'react'
import { useSites } from '@api/hooks'
import type { AssetType } from '@api/types'

interface AssetFormState {
  name: string
  type: AssetType
  siteId: string
  capacity: string
  efficiency: string
  cost_per_mwh: string
}

export default function CreateAsset() {
  const { data: sites, isLoading, error } = useSites()

  const [form, setForm] = useState<AssetFormState>({
    name: '',
    type: 'gas_boiler',
    siteId: '',
    capacity: '',
    efficiency: '',
    cost_per_mwh: '',
  })

  const [submitted, setSubmitted] = useState(false)
  const [validationError, setValidationError] = useState<string | null>(null)

  function onChange<K extends keyof AssetFormState>(key: K, value: AssetFormState[K]) {
    setForm(prev => ({ ...prev, [key]: value }))
    setValidationError(null)
    setSubmitted(false)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!form.name.trim()) {
      setValidationError('Name is required')
      return
    }
    if (!form.siteId) {
      setValidationError('Site is required')
      return
    }

    if (form.capacity && Number.isNaN(Number(form.capacity))) {
      setValidationError('Capacity must be a number')
      return
    }
    if (form.efficiency && (Number.isNaN(Number(form.efficiency)) || Number(form.efficiency) < 0 || Number(form.efficiency) > 1)) {
      setValidationError('Efficiency must be a number between 0 and 1')
      return
    }
    if (form.cost_per_mwh && Number.isNaN(Number(form.cost_per_mwh))) {
      setValidationError('Cost per MWh must be a number')
      return
    }

    // In a real app, this is where we would POST to the backend
    setSubmitted(true)
  }

  const previewAsset = submitted
    ? {
        id: '(temporary-id)',
        name: form.name,
        type: form.type,
        site_id: form.siteId,
        capacity: form.capacity ? Number(form.capacity) : null,
        efficiency: form.efficiency ? Number(form.efficiency) : null,
        cost_per_mwh: form.cost_per_mwh ? Number(form.cost_per_mwh) : null,
      }
    : null

  return (
    <div className="container">
      <div className="header" style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>Create New Asset</h1>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Asset Details</h3>
        <p className="small" style={{ marginBottom: 24 }}>
          This is a prototype form for creating assets. Submitting will not affect the backend data, but will show a
          preview of the asset payload that would be sent.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col">
              <div className="label">Asset name</div>
              <input
                className="input"
                type="text"
                value={form.name}
                onChange={(e) => onChange('name', e.target.value)}
                placeholder="e.g. Boiler 1"
              />
            </div>
            <div className="col">
              <div className="label">Asset type</div>
              <select
                className="select"
                value={form.type}
                onChange={(e) => onChange('type', e.target.value as AssetType)}
              >
                <option value="gas_boiler">Gas boiler</option>
                <option value="oil_boiler">Oil boiler</option>
                <option value="electric_boiler">Electric boiler</option>
                <option value="heat_storage">Heat storage</option>
                <option value="district_heating_network">District heating network</option>
              </select>
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div className="col">
              <div className="label">Site</div>
              {isLoading && <div className="small">Loading sites...</div>}
              {error && <div className="card alert danger">Failed to load sites</div>}
              {sites && (
                <select
                  className="select"
                  value={form.siteId}
                  onChange={(e) => onChange('siteId', e.target.value)}
                >
                  <option value="">Choose a site...</option>
                  {sites.map(site => (
                    <option key={site.id} value={site.id}>{site.name}</option>
                  ))}
                </select>
              )}
            </div>
            <div className="col">
              <div className="label">Capacity {form.type === 'heat_storage' ? '(MWh)' : '(MW)'}</div>
              <input
                className="input"
                type="number"
                step="0.01"
                value={form.capacity}
                onChange={(e) => onChange('capacity', e.target.value)}
                placeholder="Optional"
              />
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div className="col">
              <div className="label">Efficiency (0 - 1)</div>
              <input
                className="input"
                type="number"
                step="0.01"
                min={0}
                max={1}
                value={form.efficiency}
                onChange={(e) => onChange('efficiency', e.target.value)}
                placeholder="Optional"
              />
            </div>
            {(form.type === 'gas_boiler' || form.type === 'oil_boiler') && (
              <div className="col">
                <div className="label">Cost per MWh (EUR)</div>
                <input
                  className="input"
                  type="number"
                  step="0.01"
                  value={form.cost_per_mwh}
                  onChange={(e) => onChange('cost_per_mwh', e.target.value)}
                  placeholder="Optional"
                />
              </div>
            )}
          </div>

          {validationError && (
            <div className="alert danger" style={{ marginTop: 16 }}>
              {validationError}
            </div>
          )}

          {submitted && !validationError && (
            <div className="alert" style={{ marginTop: 16, background: '#1a3a1a', color: '#86efac', border: '1px solid #22c55e' }}>
              Asset form submitted successfully. This is a visual prototype only; no data was saved.
            </div>
          )}

          <div style={{ marginTop: 24, display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button type="submit" className="button">
              Create Asset (Prototype)
            </button>
          </div>
        </form>
      </div>

      {previewAsset && (
        <div className="card" style={{ marginTop: 24 }}>
          <h3 style={{ marginTop: 0 }}>Preview payload</h3>
          <div className="small" style={{ marginBottom: 8 }}>This is the JSON that would be sent to the backend in a real application.</div>
          <pre style={{ background: '#020617', padding: 12, borderRadius: 8, overflowX: 'auto', fontSize: 12 }}>
            {JSON.stringify(previewAsset, null, 2)}
          </pre>
        </div>
      )}

      <footer style={{ marginTop: 48, paddingBottom: 48, textAlign: 'center' }}>
        <div className="small">© {new Date().getFullYear()} Industrial Automation Dashboard. All rights reserved.</div>
      </footer>
    </div>
  )
}

