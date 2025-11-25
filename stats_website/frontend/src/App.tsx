import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home/Home'
import Login from './pages/Login/Login'
import Statistics from './pages/Statistics/Statistics'
import About from './pages/About/About'
import NotFound from './pages/NotFound/NotFound'
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/statistics"
        element={
          <ProtectedRoute>
            <Statistics />
          </ProtectedRoute>
        }
      />
      <Route path="/about" element={<About />} />
      <Route path="/*" element={<NotFound />} />
    </Routes>
  )
}

export default App


