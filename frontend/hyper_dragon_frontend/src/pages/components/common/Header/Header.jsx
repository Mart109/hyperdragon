import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Header.css'

const Header = () => {
  const location = useLocation()

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <span className="dragon-icon">🐉</span>
          <span className="logo-text">HyperDragon</span>
        </div>

        <nav className="navigation">
          <Link
            to="/"
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            <span className="nav-icon">🏠</span>
            <span className="nav-text">Главная</span>
          </Link>
          <Link
            to="/cards"
            className={`nav-link ${
              location.pathname === '/cards' ? 'active' : ''
            }`}
          >
            <span className="nav-icon">🃏</span>
            <span className="nav-text">Карты</span>
          </Link>
          <Link
            to="/tasks"
            className={`nav-link ${
              location.pathname === '/tasks' ? 'active' : ''
            }`}
          >
            <span className="nav-icon">📝</span>
            <span className="nav-text">Задания</span>
          </Link>
          <Link
            to="/battle"
            className={`nav-link ${
              location.pathname === '/battle' ? 'active' : ''
            }`}
          >
            <span className="nav-icon">⚔️</span>
            <span className="nav-text">Битва</span>
          </Link>
          <Link
            to="/profile"
            className={`nav-link ${
              location.pathname === '/profile' ? 'active' : ''
            }`}
          >
            <span className="nav-icon">👤</span>
            <span className="nav-text">Профиль</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}

export default Header
