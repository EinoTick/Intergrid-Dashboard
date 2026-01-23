import { Navigate, Route, Routes } from 'react-router-dom'
import Home from '@pages/Home'
import SiteDashboard from '@pages/SiteDashboard'
import Profile from '@pages/Profile'
import ChangePassword from '@pages/ChangePassword'
import NavigationBar from '@components/NavigationBar'

export default function App() {
  return (
    <>
      <NavigationBar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/site/:siteId" element={<SiteDashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/change-password" element={<ChangePassword />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  )
}
