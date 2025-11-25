import { Link } from 'react-router-dom'
import { useAppDispatch } from '../../hooks/useAppDispatch'
import { useAppSelector } from '../../hooks/useAppSelector'
import { logoutAsync } from '../../store/authSlice'
import './Nav.scss'

const Nav = () => {
  const dispatch = useAppDispatch()
  const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated)

  const handleLogout = () => {
    dispatch(logoutAsync())
  }

  return (
    <nav className="nav">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          Statistics Dashboard
        </Link>
        <ul className="nav-menu">
          <li>
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          {!isAuthenticated ? (
            <li>
              <Link to="/login" className="nav-link">
                Login
              </Link>
            </li>
          ) : (
            <>
              <li>
                <Link to="/statistics" className="nav-link">
                  Statistics
                </Link>
              </li>
              <li>
                <button onClick={handleLogout} className="nav-link nav-button">
                  Logout
                </button>
              </li>
            </>
          )}
          <li>
            <Link to="/about" className="nav-link">
              About
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default Nav
