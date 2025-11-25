import Nav from '../../components/Nav/Nav'
import './Home.scss'

const Home = () => {
  return (
    <div className="home">
      <Nav />
      <div className="home-container">
        <div className="home-content">
          <h1 className="home-title">Statistics Dashboard</h1>
          <div className="home-image-container">
            <div className="home-image-placeholder">
              <svg
                width="200"
                height="200"
                viewBox="0 0 200 200"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect width="200" height="200" fill="#3498db" opacity="0.1" />
                <path
                  d="M50 150 L70 120 L90 130 L110 100 L130 110 L150 80 L150 150 Z"
                  stroke="#3498db"
                  strokeWidth="3"
                  fill="#3498db"
                  fillOpacity="0.2"
                />
                <circle cx="70" cy="120" r="5" fill="#3498db" />
                <circle cx="90" cy="130" r="5" fill="#3498db" />
                <circle cx="110" cy="100" r="5" fill="#3498db" />
                <circle cx="130" cy="110" r="5" fill="#3498db" />
                <circle cx="150" cy="80" r="5" fill="#3498db" />
              </svg>
            </div>
          </div>
          <div className="home-description">
            <h2>Welcome to the Statistics Dashboard</h2>
            <p>
              This system provides comprehensive statistics about the vacation management platform.
              View detailed analytics including vacation statistics, user counts, likes distribution,
              and more.
            </p>
            <p>
              <strong>Admin access required:</strong> Please log in with your admin credentials
              to view the statistics.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home

