import React, { useState, useEffect } from 'react'
import './BattlePage.css'

// Импортируем изображения (замени на свои пути)
import targetImage from '../../assets/BattleDragon.png'
import dragonImage from '../../assets/dragons/dragon.jpg'

const BattlePage = () => {
  const [coins, setCoins] = useState(0)
  const [gameStarted, setGameStarted] = useState(false)
  const [gameTime, setGameTime] = useState(60)
  const [score, setScore] = useState(0)
  const [targets, setTargets] = useState([])
  const [gameInterval, setGameInterval] = useState(null)
  const [targetInterval, setTargetInterval] = useState(null)

  // Типы драконов с разными характеристиками
  const dragonTypes = [
    {
      type: 'fast',
      name: 'Быстрый дракон',
      lifetime: 1000, // 1 секунда
      points: 5, // очков за попадание
      color: '#ff4444',
      size: 40, // меньший размер
    },
    {
      type: 'normal',
      name: 'Обычный дракон',
      lifetime: 2000, // 2 секунды
      points: 10,
      color: '#44aaff',
      size: 60,
    },
    {
      type: 'slow',
      name: 'Медленный дракон',
      lifetime: 4000, // 4 секунды
      points: 20,
      color: '#44ff44',
      size: 80, // больший размер
    },
    {
      type: 'boss',
      name: 'Босс дракон',
      lifetime: 6000, // 6 секунд
      points: 50,
      color: '#ff44ff',
      size: 100, // самый большой
    },
  ]

  // Загрузка баланса монет
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    if (savedCoins) setCoins(parseInt(savedCoins))
  }, [])

  // Очистка интервалов при размонтировании
  useEffect(() => {
    return () => {
      if (gameInterval) clearInterval(gameInterval)
      if (targetInterval) clearInterval(targetInterval)
    }
  }, [gameInterval, targetInterval])

  const startGame = () => {
    setGameStarted(true)
    setGameTime(60)
    setScore(0)
    setTargets([])

    // Таймер игры
    const timer = setInterval(() => {
      setGameTime((prev) => {
        if (prev <= 1) {
          endGame()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    // Создание целей - разные типы с разной частотой появления
    const targetCreator = setInterval(() => {
      createRandomTarget()
    }, 800) // Новая цель каждые 0.8 секунды

    setGameInterval(timer)
    setTargetInterval(targetCreator)
  }

  const createRandomTarget = () => {
    const randomType = getRandomDragonType()
    const dragonType = dragonTypes.find((dragon) => dragon.type === randomType)

    const newTarget = {
      id: Date.now() + Math.random(),
      x: Math.random() * 80 + 10, // 10-90% по X
      y: Math.random() * 70 + 15, // 15-85% по Y
      size: dragonType.size,
      type: dragonType.type,
      lifetime: dragonType.lifetime,
      points: dragonType.points,
      color: dragonType.color,
      name: dragonType.name,
    }

    setTargets((prev) => [...prev, newTarget])

    // Удаление цели через определенное время
    setTimeout(() => {
      setTargets((prev) => prev.filter((target) => target.id !== newTarget.id))
    }, dragonType.lifetime)
  }

  // Вероятность появления разных типов драконов
  const getRandomDragonType = () => {
    const random = Math.random()
    if (random < 0.4) return 'fast' // 40% - быстрые
    if (random < 0.7) return 'normal' // 30% - обычные
    if (random < 0.9) return 'slow' // 20% - медленные
    return 'boss' // 10% - боссы
  }

  const hitTarget = (targetId) => {
    const target = targets.find((t) => t.id === targetId)
    if (target) {
      setTargets((prev) => prev.filter((target) => target.id !== targetId))
      setScore((prev) => prev + target.points)
    }
  }

  const endGame = () => {
    if (gameInterval) clearInterval(gameInterval)
    if (targetInterval) clearInterval(targetInterval)

    // Начисление награды (1 монета за каждое очко)
    const reward = score
    const newCoins = coins + reward
    setCoins(newCoins)
    localStorage.setItem('hypeDragon_coins', newCoins.toString())

    setGameStarted(false)
  }

  const cancelGame = () => {
    if (gameInterval) clearInterval(gameInterval)
    if (targetInterval) clearInterval(targetInterval)
    setGameStarted(false)
    setTargets([])
  }

  // Получение класса для цели в зависимости от типа
  const getTargetClass = (targetType) => {
    return `target target-${targetType}`
  }

  // Получение текста для времени исчезновения
  const getLifetimeText = (lifetime) => {
    return `${lifetime / 1000}сек`
  }

  return (
    <div className="battle-page">
      <div className="battle-container">
        {/* Заголовок */}
        <header className="battle-header">
          <div className="header-content">
            <h1 className="battle-title">⚔️ Battle Arena</h1>
            <p className="battle-subtitle">
              Уничтожай драконов и зарабатывай монеты!
            </p>
          </div>
          <div className="header-decoration">
            <div className="decoration-sword">⚔️</div>
            <div className="decoration-shield">🛡️</div>
            <div className="decoration-target">🎯</div>
          </div>
        </header>

        {/* Баланс монет */}
        <div className="balance-section">
          <div className="balance-card">
            <div className="balance-icon">💰</div>
            <div className="balance-content">
              <div className="balance-title">Ваш баланс</div>
              <div className="balance-value">
                {coins.toLocaleString()} монет
              </div>
            </div>
          </div>
        </div>

        {/* Основной игровой контент */}
        <div className="battle-main">
          {/* Статистика битвы */}
          <div className="battle-stats">
            <div className="stat-item">
              <div className="stat-icon">🎯</div>
              <div className="stat-info">
                <div className="stat-value">{score}</div>
                <div className="stat-label">Набрано очков</div>
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-icon">⏱️</div>
              <div className="stat-info">
                <div className="stat-value">{gameTime}s</div>
                <div className="stat-label">Осталось времени</div>
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-icon">💰</div>
              <div className="stat-info">
                <div className="stat-value">{score}</div>
                <div className="stat-label">Текущий выигрыш</div>
              </div>
            </div>
          </div>

          {/* Кнопка начала игры */}
          {!gameStarted && (
            <div className="start-section">
              <div className="game-rules">
                <h3>🎯 Правила игры:</h3>
                <ul>
                  <li>
                    • <span style={{ color: '#ff4444' }}>Быстрые драконы</span>{' '}
                    - 5 очков, 1 сек
                  </li>
                  <li>
                    • <span style={{ color: '#44aaff' }}>Обычные драконы</span>{' '}
                    - 10 очков, 2 сек
                  </li>
                  <li>
                    •{' '}
                    <span style={{ color: '#44ff44' }}>Медленные драконы</span>{' '}
                    - 20 очков, 4 сек
                  </li>
                  <li>
                    • <span style={{ color: '#ff44ff' }}>Босс драконы</span> -
                    50 очков, 6 сек
                  </li>
                  <li>• 1 очко = 1 монета награды</li>
                  <li>• Время: 60 секунд</li>
                </ul>
              </div>
              <button className="start-button" onClick={startGame}>
                <span className="button-icon">🎮</span>
                Начать битву!
              </button>
            </div>
          )}

          {/* Игровое поле */}
          {gameStarted && (
            <div className="game-field" onClick={(e) => e.stopPropagation()}>
              <div className="game-header-info">
                <div className="time-left">Осталось: {gameTime}с</div>
                <div className="current-score">Очки: {score}</div>
                <button className="cancel-button" onClick={cancelGame}>
                  ❌ Отмена
                </button>
              </div>

              {/* Цели */}
              {targets.map((target) => (
                <div
                  key={target.id}
                  className={getTargetClass(target.type)}
                  style={{
                    left: `${target.x}%`,
                    top: `${target.y}%`,
                    width: `${target.size}px`,
                    height: `${target.size}px`,
                    borderColor: target.color,
                  }}
                  onClick={() => hitTarget(target.id)}
                >
                  <img
                    src={targetImage}
                    alt="Target"
                    className="target-image"
                    onError={(e) => {
                      e.target.style.display = 'none'
                    }}
                  />
                  <div className="target-info">
                    <div className="target-points">+{target.points}</div>
                    <div className="target-timer">
                      {getLifetimeText(target.lifetime)}
                    </div>
                  </div>
                </div>
              ))}

              <div className="game-instruction">🎯 Кликай по драконам!</div>
            </div>
          )}
        </div>

        {/* Модальное окно результатов */}
        {!gameStarted && score > 0 && (
          <div className="results-modal">
            <div className="modal-content">
              <h2>🎉 Битва завершена!</h2>
              <div className="results-stats">
                <div className="result-item">
                  <span className="result-label">Набрано очков:</span>
                  <span className="result-value">{score}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Заработано монет:</span>
                  <span className="result-value reward">{score}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Общий баланс:</span>
                  <span className="result-value">{coins.toLocaleString()}</span>
                </div>
              </div>
              <button className="play-again-button" onClick={startGame}>
                <span className="button-icon">🔄</span>
                Играть снова
              </button>
            </div>
          </div>
        )}

        {/* Футер */}
        <footer className="battle-footer">
          <p>✨ Уничтожай драконов и становись королем арены! ✨</p>
        </footer>
      </div>
    </div>
  )
}

export default BattlePage
