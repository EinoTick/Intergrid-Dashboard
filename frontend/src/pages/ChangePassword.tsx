import { useState } from 'react'

export default function ChangePassword() {
  const [form, setForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  function onChange(key: string, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
    setError('')
    setSuccess(false)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setSuccess(false)

    // Validation
    if (!form.currentPassword || !form.newPassword || !form.confirmPassword) {
      setError('All fields are required')
      return
    }

    if (form.newPassword !== form.confirmPassword) {
      setError('New password and confirm password do not match')
      return
    }

    if (form.newPassword.length < 8) {
      setError('New password must be at least 8 characters long')
      return
    }

    // In a real app, this would save to backend
    setSuccess(true)
    setForm({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
  }

  return (
    <div className="container">
      <div className="header" style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>Change Password</h1>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Update Your Password</h3>
        <p className="small" style={{ marginBottom: 24 }}>
          Enter your current password and choose a new password. Make sure your new password is at least 8 characters long.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col">
              <div className="label">Current Password</div>
              <input
                className="input"
                type="password"
                value={form.currentPassword}
                onChange={(e) => onChange('currentPassword', e.target.value)}
                placeholder="Enter current password"
              />
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div className="col">
              <div className="label">New Password</div>
              <input
                className="input"
                type="password"
                value={form.newPassword}
                onChange={(e) => onChange('newPassword', e.target.value)}
                placeholder="Enter new password"
              />
            </div>
            <div className="col">
              <div className="label">Confirm New Password</div>
              <input
                className="input"
                type="password"
                value={form.confirmPassword}
                onChange={(e) => onChange('confirmPassword', e.target.value)}
                placeholder="Confirm new password"
              />
            </div>
          </div>

          {error && (
            <div className="alert danger" style={{ marginTop: 16 }}>
              {error}
            </div>
          )}

          {success && (
            <div className="alert" style={{ marginTop: 16, background: '#1a3a1a', color: '#86efac', border: '1px solid #22c55e' }}>
              Password changed successfully!
            </div>
          )}

          <div style={{ marginTop: 24, display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
            <button type="submit" className="button">
              Change Password
            </button>
          </div>
        </form>
      </div>

      <footer style={{ marginTop: 48, paddingBottom: 48, textAlign: 'center' }}>
        <div className="small">© {new Date().getFullYear()} Industrial Automation Dashboard. All rights reserved.</div>
      </footer>
    </div>
  )
}
