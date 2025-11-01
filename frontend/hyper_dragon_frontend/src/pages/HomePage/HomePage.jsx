import React, { useState, useEffect } from 'react'
import './HomePage.css'
import dragonImage from '../../assets/dragons/dragon.jpg'

const HomePage = () => {
  const [coins, setCoins] = useState(0)
  const [level, setLevel] = useState(1)
  const [energy, setEnergy] = useState(500)
  const [maxEnergy] = useState(500)
  const [isClicking, setIsClicking] = useState(false)
  const [clickEffect, setClickEffect] = useState(false)
  const [energyRestores, setEnergyRestores] = useState(3)
  const [lastResetDate, setLastResetDate] = useState('')

  useEffect(() => {
    const energyInterval = setInterval(() => {
      setEnergy((prev) => (prev < maxEnergy ? prev + 1 : prev))
    }, 1500)
    return () => clearInterval(energyInterval)
  }, [maxEnergy])

  useEffect(() => {
    const checkDailyReset = () => {
      const today = new Date().toDateString()
      const storedDate = localStorage.getItem('hypeDragon_lastResetDate')
      if (storedDate !== today) {
        setEnergyRestores(3)
        setLastResetDate(today)
        localStorage.setItem('hypeDragon_lastResetDate', today)
        localStorage.setItem('hypeDragon_energyRestores', '3')
      } else {
        const storedRestores = localStorage.getItem('hypeDragon_energyRestores')
        if (storedRestores) setEnergyRestores(parseInt(storedRestores))
      }
    }
    checkDailyReset()
    const resetInterval = setInterval(checkDailyReset, 60 * 60 * 1000)
    return () => clearInterval(resetInterval)
  }, [])

  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    const savedLevel = localStorage.getItem('hypeDragon_level')
    const savedEnergy = localStorage.getItem('hypeDragon_energy')
    const savedRestores = localStorage.getItem('hypeDragon_energyRestores')
    const savedResetDate = localStorage.getItem('hypeDragon_lastResetDate')
    if (savedCoins) setCoins(parseInt(savedCoins))
    if (savedLevel) setLevel(parseInt(savedLevel))
    if (savedEnergy) setEnergy(parseInt(savedEnergy))
    if (savedRestores) setEnergyRestores(parseInt(savedRestores))
    if (savedResetDate) setLastResetDate(savedResetDate)
  }, [])

  useEffect(() => {
    localStorage.setItem('hypeDragon_coins', coins.toString())
    localStorage.setItem('hypeDragon_level', level.toString())
    localStorage.setItem('hypeDragon_energy', energy.toString())
  }, [coins, level, energy])

  const handleClick = () => {
    if (energy <= 0) return
    setIsClicking(true)
    setClickEffect(true)
    const newCoins = coins + 1
    setCoins(newCoins)
    setEnergy((prev) => prev - 1)
    const coinsNeededForNextLevel = level * 1000
    if (newCoins >= coinsNeededForNextLevel) setLevel((prev) => prev + 1)
    setTimeout(() => {
      setIsClicking(false)
      setClickEffect(false)
    }, 200)
  }

  const handleRestoreEnergy = () => {
    if (energyRestores > 0 && energy < maxEnergy) {
      setEnergy(maxEnergy)
      const newRestores = energyRestores - 1
      setEnergyRestores(newRestores)
      localStorage.setItem('hypeDragon_energyRestores', newRestores.toString())
      alert(
        `⚡ Энергия восстановлена!\nОсталось восстановлений на сегодня: ${newRestores}`,
      )
    } else if (energyRestores <= 0) {
      alert('❌ Достигнут лимит восстановлений на сегодня!')
    } else if (energy >= maxEnergy) {
      alert('ℹ️ Энергия уже полная!')
    }
  }

  const energyPercentage = (energy / maxEnergy) * 100
  const coinsNeededForNextLevel = level * 1000
  const progressPercentage = Math.min(
    (coins / coinsNeededForNextLevel) * 100,
    100,
  )

  return (
    <div className="home-page">
      <div className="game-container">
        <header className="game-header">
          <div className="header-content">
            <h1 className="game-title">🔥 Hype Dragon</h1>
            <p className="game-subtitle">Кликни дракона и собирай сокровища!</p>
          </div>
          <div className="header-decoration">
            <div className="decoration-coin">💰</div>
            <div className="decoration-gem">💎</div>
            <div className="decoration-fire">🔥</div>
          </div>
        </header>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon gold">💰</div>
            <div className="stat-content">
              <div className="stat-title">Монеты</div>
              <div className="stat-value">{coins.toLocaleString()}</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon blue">⭐</div>
            <div className="stat-content">
              <div className="stat-title">Уровень</div>
              <div className="stat-value">{level}</div>
            </div>
          </div>
          {/* ОБНОВЛЕННЫЙ БЛОК: Используем обертку для центрирования на мобильных */}
          <div className="button-wrapper-center">
            <div className="stat-card energy-button">
              <div className="stat-icon energy">⚡</div>
              <div className="stat-content">
                <div className="stat-title">Энергия</div>
                <div className="stat-value">
                  {energy}/{maxEnergy}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="progress-section">
          <div className="progress-container">
            <div className="progress-header">
              <span className="progress-title">
                <span className="progress-icon">⭐</span>
                До уровня {level + 1}
              </span>
              <span className="progress-percent">
                {Math.round(progressPercentage)}%
              </span>
            </div>
            <div className="progress-bar level-bar">
              <div
                className="progress-fill level-fill"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <div className="progress-info">
              Нужно монет: {coins}/{coinsNeededForNextLevel}
            </div>
          </div>
        </div>
        <div className="progress-section">
          <div className="progress-container">
            <div className="progress-header">
              <span className="progress-title">
                <span className="progress-icon">⚡</span>
                Энергия
              </span>
              <span className="progress-percent">
                {Math.round(energyPercentage)}%
              </span>
            </div>
            <div className="progress-bar energy-bar">
              <div
                className="progress-fill energy-fill"
                style={{ width: `${energyPercentage}%` }}
              ></div>
            </div>
            <div className="progress-info">
              Восстановление: 1 энергия каждые 1.5 секунды
            </div>
          </div>
        </div>
        <div className="clicker-section">
          <div className="clicker-container">
            <button
              className={`clicker-button ${isClicking ? 'clicking' : ''} ${
                clickEffect ? 'click-effect' : ''
              } ${energy <= 0 ? 'disabled' : ''}`}
              onClick={handleClick}
              disabled={energy <= 0}
            >
              <div className="dragon-full-image">
                <img
                  src={dragonImage}
                  alt="Dragon"
                  className="dragon-image-full"
                />
              </div>
              {clickEffect && (
                <div className="click-effects">
                  {[...Array(12)].map((_, i) => (
                    <div key={i} className={`click-particle particle-${i}`}>
                      {i % 3 === 0 ? '💰' : i % 3 === 1 ? '💎' : '✨'}
                    </div>
                  ))}
                </div>
              )}
              <div className="button-aura"></div>
            </button>
            {energy <= 0 && (
              <div className="energy-warning">
                ⚡ Энергия закончилась! Жди восстановления...
              </div>
            )}
          </div>
        </div>
        <div className="upgrades-section">
          <h3 className="section-title">
            <span className="title-icon">🚀</span>
            Бусты
          </h3>
          <div className="upgrades-grid">
            {/* Кнопка восстановления энергии добавлена сюда */}
            <div className="upgrade-card" onClick={handleRestoreEnergy}>
              <div className="upgrade-icon">🔋</div>
              <div className="upgrade-content">
                <div className="upgrade-title">Восстановить энергию</div>
                <div className="upgrade-description">
                  Мгновенно заполнить энергию.
                </div>
              </div>
              <div className="upgrade-cost">
                {energyRestores} / 3 <span>(ежедневно)</span>
              </div>
            </div>
          </div>{' '}
          {/* Конец upgrades-grid */}
        </div>{' '}
        {/* Конец upgrades-section */}
      </div>{' '}
      {/* Конец game-container */}
    </div> /* Конец home-page */
  )
}

export default HomePage
