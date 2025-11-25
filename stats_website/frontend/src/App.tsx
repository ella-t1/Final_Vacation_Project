import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div>Statistics Website - Coming Soon</div>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

