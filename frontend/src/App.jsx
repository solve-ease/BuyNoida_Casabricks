import { useState } from 'react'
import './App.css'

function App() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (email) {
      setSubmitted(true)
      setTimeout(() => {
        setSubmitted(false)
        setEmail('')
      }, 3000)
    }
  }

  return (
    <div className="coming-soon-container">
      {/* Property Images Background */}
      <div className="property-showcase">
        <div className="property-image property-1">
          <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80" alt="Modern Property" />
        </div>
        <div className="property-image property-2">
          <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80" alt="Luxury Home" />
        </div>
        <div className="property-image property-3">
          <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80" alt="Premium Property" />
        </div>
      </div>

      {/* Overlay */}
      <div className="overlay"></div>

      {/* Main Content */}
      <div className="content">
        <div className="brand-section">
          <div className="logo-icon">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <rect x="20" y="30" width="60" height="50" fill="none" stroke="currentColor" strokeWidth="2.5" rx="2"/>
              <rect x="30" y="40" width="15" height="15" fill="currentColor" opacity="0.6"/>
              <rect x="55" y="40" width="15" height="15" fill="currentColor" opacity="0.6"/>
              <rect x="30" y="60" width="15" height="15" fill="currentColor" opacity="0.6"/>
              <rect x="55" y="60" width="15" height="15" fill="currentColor" opacity="0.6"/>
              <path d="M20 30 L50 15 L80 30" fill="none" stroke="currentColor" strokeWidth="2.5"/>
            </svg>
          </div>
          <h2 className="brand-name">CASABRICK</h2>
          <h1 className="main-title">
            <span className="title-word">Buy</span>
            <span className="title-word highlight">Noida</span>
          </h1>
          <p className="tagline">Premium Properties in Noida</p>
        </div>

        <div className="info-section">
          <p className="description">
            Something special is on the way. Be the first to explore exclusive properties.
          </p>

          <form onSubmit={handleSubmit} className="notify-form">
            <div className="input-wrapper">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                className="email-input"
                required
              />
              <button type="submit" className="notify-btn">
                {submitted ? '✓' : 'Get Notified'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
