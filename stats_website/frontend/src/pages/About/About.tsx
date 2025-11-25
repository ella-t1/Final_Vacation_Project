import Nav from '../../components/Nav/Nav'
import './About.scss'

const About = () => {
  return (
    <div className="about">
      <Nav />
      <div className="about-container">
        <div className="about-content">
          <h1 className="about-title">About</h1>
          <div className="about-section">
            <h2>Statistics Dashboard</h2>
            <p>
              This is a comprehensive statistics dashboard for the vacation management system.
              It provides detailed analytics and insights into the platform's data.
            </p>
          </div>
          <div className="about-section">
            <h2>Developer Information</h2>
            <p>
              <strong>Name:</strong> Ella Tubali
            </p>
            <p>
              <strong>Project:</strong> Full Stack Web Developer
            </p>
            <p>
              <strong>Institution:</strong> John Bryce 
            </p>
            <p>
              <strong>Technologies:</strong> React.js, TypeScript, Redux Toolkit, Python, Flask, PostgreSQL, Docker
            </p>
          </div>
          <div className="about-section">
            <h2>Features</h2>
            <ul>
              <li>Admin-only authentication</li>
              <li>Real-time vacation statistics</li>
              <li>User engagement metrics</li>
              <li>Likes distribution by destination</li>
              <li>Modern, responsive UI</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default About

