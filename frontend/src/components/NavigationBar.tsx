import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { FaSignInAlt, FaSignOutAlt } from 'react-icons/fa'
import { useSites, useSiteDetail } from '@api/hooks'

export default function NavigationBar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { data: sites } = useSites()
  
  // Extract siteId from the URL pathname
  const siteIdMatch = location.pathname.match(/^\/site\/([^/]+)/)
  const siteId = siteIdMatch ? siteIdMatch[1] : undefined
  
  const { data: siteDetail } = useSiteDetail(siteId)
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768)
  const [isExpanded, setIsExpanded] = useState(!isMobile)
  const [isLoggedIn, setIsLoggedIn] = useState(true) // Default to logged in

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768
      setIsMobile(mobile)
      setIsExpanded(!mobile)
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const isDashboard = location.pathname.startsWith('/site/')

  // Generate navigation links for dashboard sections
  const getDashboardLinks = () => {
    if (!siteDetail) return []
    
    const links: Array<{ id: string; label: string }> = []
    
    // Link to assets grid section
    links.push({ id: 'assets-grid', label: 'Assets Overview' })
    
    // Production assets section
    const productionAssets = siteDetail.assets.filter(a => 
      ['gas_boiler', 'oil_boiler', 'electric_boiler'].includes(a.type)
    )
    if (productionAssets.length > 0) {
      links.push({ id: 'production-assets', label: 'Production Assets' })
    }
    
    // Storage assets section
    const storageAssets = siteDetail.assets.filter(a => a.type === 'heat_storage')
    if (storageAssets.length > 0) {
      links.push({ id: 'storage-assets', label: 'Storage Assets' })
    }
    
    // Network section
    const network = siteDetail.assets.find(a => a.type === 'district_heating_network')
    if (network) {
      links.push({ id: 'network-consumption', label: 'Network Consumption' })
    }
    
    // Electricity prices section (always present)
    links.push({ id: 'electricity-prices', label: 'Electricity Prices' })
    
    return links
  }

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      // Close nav on mobile after clicking
      if (isMobile) {
        setIsExpanded(false)
      }
    }
  }

  const dashboardLinks = isDashboard ? getDashboardLinks() : []

  return (
    <>
      {/* Mobile toggle button */}
      {isMobile && (
        <button 
          className="nav-toggle"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>
      )}
      
      {/* Navigation bar */}
      <nav className={`nav-bar ${isExpanded ? 'expanded' : 'collapsed'}`}>
        <div className="nav-content">
          {/* Company name */}
          <div className="nav-header">
            <h2 style={{ margin: 0, fontSize: '18px' }}>Intergrid</h2>
          </div>

          {/* Site selector */}
          <div className="nav-section">
            <div className="label">Select a site</div>
            <select 
              className="select" 
              value={siteId ?? ''}
              onChange={(e) => {
                if (e.target.value) {
                  navigate(`/site/${e.target.value}`)
                } else {
                  navigate('/')
                }
              }}
            >
              <option value="">Home</option>
              {sites?.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>

          {/* Dashboard navigation links */}
          {isDashboard && dashboardLinks.length > 0 && (
            <div className="nav-section">
              <div className="label">Navigation</div>
              <div className="nav-links">
                {dashboardLinks.map(link => (
                  <button
                    key={link.id}
                    className="nav-link"
                    onClick={() => scrollToSection(link.id)}
                  >
                    {link.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Spacer to push login/logout to bottom */}
          <div style={{ flex: 1 }} />

          {/* Login/Logout toggle (visual only) */}
          <div className="nav-section nav-footer">
            <button 
              className="nav-link" 
              style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}
              onClick={() => setIsLoggedIn(!isLoggedIn)}
            >
              {isLoggedIn ? (
                <>
                  <FaSignOutAlt />
                  Logout
                </>
              ) : (
                <>
                  <FaSignInAlt />
                  Login
                </>
              )}
            </button>
          </div>
        </div>
      </nav>
      
      {/* Overlay for mobile */}
      {isMobile && isExpanded && (
        <div className="nav-overlay" onClick={() => setIsExpanded(false)} />
      )}
    </>
  )
}
