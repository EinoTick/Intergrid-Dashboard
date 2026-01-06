import { Navigate, Route, Routes } from 'react-router-dom'
import Home from '@pages/Home'
import SiteDashboard from '@pages/SiteDashboard'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/site/:siteId" element={<SiteDashboard />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
