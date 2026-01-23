import { useState } from 'react'

export default function Profile() {
  const [form, setForm] = useState({
    email: 'user@example.com',
    name: 'John Doe',
    company: 'Intergrid',
    phone: '+1 234 567 8900',
    description: 'Industrial automation specialist with expertise in energy management systems.'
  })

  const [isEditing, setIsEditing] = useState(false)

  function onChange(key: string, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setIsEditing(false)
    // In a real app, this would save to backend
  }

  function handleCancel() {
    setIsEditing(false)
    // Reset form to original values (in real app, fetch from backend)
    setForm({
      email: 'user@example.com',
      name: 'John Doe',
      company: 'Intergrid',
      phone: '+1 234 567 8900',
      description: 'Industrial automation specialist with expertise in energy management systems.'
    })
  }

  return (
    <div className="container">
      <div className="header" style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>User Profile</h1>
      </div>

      <div className="card">
        <div className="header" style={{ marginBottom: 16 }}>
          <h3 style={{ margin: 0 }}>Profile Information</h3>
          {!isEditing && (
            <button className="button" onClick={() => setIsEditing(true)}>
              Edit Profile
            </button>
          )}
        </div>

        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col">
              <div className="label">Email</div>
              {isEditing ? (
                <input
                  className="input"
                  type="email"
                  value={form.email}
                  onChange={(e) => onChange('email', e.target.value)}
                />
              ) : (
                <div style={{ padding: '8px', color: 'var(--text)' }}>{form.email}</div>
              )}
            </div>
            <div className="col">
              <div className="label">Name</div>
              {isEditing ? (
                <input
                  className="input"
                  type="text"
                  value={form.name}
                  onChange={(e) => onChange('name', e.target.value)}
                />
              ) : (
                <div style={{ padding: '8px', color: 'var(--text)' }}>{form.name}</div>
              )}
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div className="col">
              <div className="label">Company</div>
              {isEditing ? (
                <input
                  className="input"
                  type="text"
                  value={form.company}
                  onChange={(e) => onChange('company', e.target.value)}
                />
              ) : (
                <div style={{ padding: '8px', color: 'var(--text)' }}>{form.company}</div>
              )}
            </div>
            <div className="col">
              <div className="label">Phone</div>
              {isEditing ? (
                <input
                  className="input"
                  type="tel"
                  value={form.phone}
                  onChange={(e) => onChange('phone', e.target.value)}
                />
              ) : (
                <div style={{ padding: '8px', color: 'var(--text)' }}>{form.phone}</div>
              )}
            </div>
          </div>

          <div style={{ marginTop: 16 }}>
            <div className="label">Description</div>
            {isEditing ? (
              <textarea
                className="input"
                rows={4}
                value={form.description}
                onChange={(e) => onChange('description', e.target.value)}
              />
            ) : (
              <div style={{ padding: '8px', color: 'var(--text)', lineHeight: '1.6' }}>{form.description}</div>
            )}
          </div>

          {isEditing && (
            <div style={{ marginTop: 24, display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
              <button type="button" className="button secondary" onClick={handleCancel}>
                Cancel
              </button>
              <button type="submit" className="button">
                Save Changes
              </button>
            </div>
          )}
        </form>
      </div>

      <footer style={{ marginTop: 48, paddingBottom: 48, textAlign: 'center' }}>
        <div className="small">© {new Date().getFullYear()} Industrial Automation Dashboard. All rights reserved.</div>
      </footer>
    </div>
  )
}
