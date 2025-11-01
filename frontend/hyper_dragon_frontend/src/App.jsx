import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage/HomePage'
import CardsPage from './pages/CardsPage/CardsPage'
import BattlePage from './pages/BattlePage/BattlePage'
import ProfilePage from './pages/ProfilePage/ProfilePage'
import Header from './pages/components/common/Header/Header'
import BoostsPage from './pages/BoostsPage/BoostShop'
import TasksPage from './pages/TasksPage/TasksPage'

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/cards" element={<CardsPage />} />
            <Route path="/battle" element={<BattlePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path='/boosts' element={<BoostsPage />} />
            <Route path='/tasks' element={<TasksPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
