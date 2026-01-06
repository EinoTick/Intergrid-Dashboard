import { useNavigate } from 'react-router-dom'
import { useSites } from '@api/hooks'

export default function SiteSelector() {
  const { data: sites, isLoading, error } = useSites()
  const navigate = useNavigate()

  if (isLoading) return <div className="card">Loading sites...</div>
  if (error) return <div className="card alert danger">Failed to load sites</div>

  return (
    <div className="card">
      <div className="label">Select a site</div>
      <select className="select" onChange={(e) => e.target.value && navigate(`/site/${e.target.value}`)} defaultValue="">
        <option value="" disabled>Choose a site...</option>
        {sites?.map(s => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>
    </div>
  )
}
