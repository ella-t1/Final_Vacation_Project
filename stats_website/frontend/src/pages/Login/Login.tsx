import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppDispatch } from '../../hooks/useAppDispatch'
import { useAppSelector } from '../../hooks/useAppSelector'
import { loginAsync, clearError } from '../../store/authSlice'
import Nav from '../../components/Nav/Nav'
import './Login.scss'

const Login = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { loading, error, isAuthenticated } = useAppSelector((state) => state.auth)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/statistics')
    }
  }, [isAuthenticated, navigate])

  // Clear error when component unmounts
  useEffect(() => {
    return () => {
      dispatch(clearError())
    }
  }, [dispatch])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    dispatch(clearError())

    if (!username || !password) {
      return
    }

    try {
      await dispatch(
        loginAsync({
          username,
          password,
        })
      ).unwrap()
      navigate('/statistics')
    } catch (err) {
      // Error is handled by Redux
    }
  }

  return (
    <div className="login">
      <Nav />
      <div className="login-container">
        <div className="login-card">
          <h1 className="login-title">Admin Login</h1>
          <p className="login-subtitle">Please enter your credentials to access the statistics dashboard</p>

          {error && (
            <div className="login-error">
              <span>⚠️</span> {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Username or Email</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username or email"
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                disabled={loading}
              />
            </div>

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login

