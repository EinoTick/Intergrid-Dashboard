import { Navigate, Route, Routes } from 'react-router-dom'
import Home from '@pages/Home'
import SiteDashboard from '@pages/SiteDashboard'
import NavigationBar from '@components/NavigationBar'

export default function App() {
  return (
    <>
      <NavigationBar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/site/:siteId" element={<SiteDashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  )
}
