import SiteSelector from '@components/SiteSelector'

export default function Home() {
  return (
    <div className="container">
      <div className="header">
        <h2 style={{ margin: 0 }}>Industrial Automation Dashboard</h2>
      </div>
      <SiteSelector />
      <div className="card" style={{ marginTop: 16 }}>
        <div className="small">Start the backend API (see api/README.md) and select a site to view assets, production, storage, prices and consumption.</div>
      </div>
    </div>
  )
}
