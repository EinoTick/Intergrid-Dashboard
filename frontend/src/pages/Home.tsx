import { useNavigate } from 'react-router-dom'
import { useSites } from '@api/hooks'

export default function Home() {
  const navigate = useNavigate()
  const { data: sites, isLoading, error } = useSites()

  return (
    <div className="container">
      <div className="header" style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>Welcome to Intergrid Dashboard</h1>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>About</h3>
        <p style={{ marginBottom: 0, lineHeight: '1.6' }}>
          The Intergrid Dashboard provides comprehensive monitoring and management for industrial automation sites. 
          View real-time asset data, production metrics, storage levels, electricity prices, and consumption forecasts 
          for all your connected sites. Select a site from the navigation bar or the list below to get started.
        </p>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Available Sites</h3>
        {isLoading && <div className="small">Loading sites...</div>}
        {error && <div className="alert danger">Failed to load sites</div>}
        {sites && sites.length > 0 ? (
          <div className="grid" style={{ marginTop: 16 }}>
            {sites.map(site => (
              <div key={site.id} className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }} 
                   onClick={() => navigate(`/site/${site.id}`)}
                   onMouseEnter={(e) => e.currentTarget.style.borderColor = '#22c55e'}
                   onMouseLeave={(e) => e.currentTarget.style.borderColor = '#1f2937'}>
                <h3 style={{ marginTop: 0, marginBottom: 8 }}>{site.name}</h3>
                <div className="small">Assets: {site.asset_ids.length}</div>
                <div className="small" style={{ marginTop: 8, color: 'var(--accent)' }}>Click to view dashboard →</div>
              </div>
            ))}
          </div>
        ) : sites && sites.length === 0 ? (
          <div className="small" style={{ marginTop: 16 }}>No sites available</div>
        ) : null}
      </div>

      <footer style={{ marginTop: 48, paddingBottom: 48, textAlign: 'center' }}>
        <div className="small">© {new Date().getFullYear()} Industrial Automation Dashboard. All rights reserved.</div>
      </footer>
    </div>
  )
}
