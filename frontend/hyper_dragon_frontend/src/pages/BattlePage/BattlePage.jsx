import React, { useState, useEffect, useRef } from 'react'
import './BattlePage.css'

// Импортируем изображения
import targetImage from '../../assets/BattleDragon.png'
import dragonImage from '../../assets/dragons/dragon.jpg'

// Сервис для работы с API
const battleService = {
  async findOpponent(userId) {
    const response = await fetch('http://localhost:8080/api/matchmaking/find', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId }),
    })
    return await response.json()
  },

  async updateScore(matchId, userId, score) {
    await fetch('http://localhost:8080/api/game/score', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ matchId, userId, score }),
    })
  },

  async finishGame(matchId) {
    const response = await fetch(
      `http://localhost:8080/api/game/finish/${matchId}`,
      {
        method: 'POST',
      },
    )
    return await response.json()
  },

  async cancelMatchmaking(userId) {
    await fetch('http://localhost:8080/api/matchmaking/cancel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId }),
    })
  },

  async getGameSession(matchId) {
    const response = await fetch(
      `http://localhost:8080/api/game/session/${matchId}`,
    )
    return await response.json()
  },
}

const BattlePage = () => {
  const [coins, setCoins] = useState(0)
  const [userId] = useState(1) // В реальном приложении брать из контекста/стора

  // Состояния матчмейкинга
  const [matchStatus, setMatchStatus] = useState('IDLE') // IDLE, SEARCHING, FOUND, PLAYING, FINISHED
  const [matchId, setMatchId] = useState(null)
  const [opponent, setOpponent] = useState(null)
  const [countdown, setCountdown] = useState(0)

  // Игровые состояния
  const [gameTime, setGameTime] = useState(60)
  const [playerScore, setPlayerScore] = useState(0)
  const [opponentScore, setOpponentScore] = useState(0)
  const [targets, setTargets] = useState([])
  const [gameSession, setGameSession] = useState(null)

  const gameInterval = useRef(null)
  const targetInterval = useRef(null)
  const sessionCheckInterval = useRef(null)

  // Типы драконов
  const dragonTypes = [
    {
      type: 'fast',
      name: 'Быстрый дракон',
      lifetime: 1000,
      points: 5,
      color: '#ff4444',
      size: 40,
    },
    {
      type: 'normal',
      name: 'Обычный дракон',
      lifetime: 2000,
      points: 10,
      color: '#44aaff',
      size: 60,
    },
    {
      type: 'slow',
      name: 'Медленный дракон',
      lifetime: 4000,
      points: 20,
      color: '#44ff44',
      size: 80,
    },
    {
      type: 'boss',
      name: 'Босс дракон',
      lifetime: 6000,
      points: 50,
      color: '#ff44ff',
      size: 100,
    },
  ]

  // Загрузка баланса монет
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    if (savedCoins) setCoins(parseInt(savedCoins))
  }, [])

  // Очистка интервалов
  useEffect(() => {
    return () => {
      if (gameInterval.current) clearInterval(gameInterval.current)
      if (targetInterval.current) clearInterval(targetInterval.current)
      if (sessionCheckInterval.current)
        clearInterval(sessionCheckInterval.current)
    }
  }, [])

  // Поиск противника
  const findOpponent = async () => {
    setMatchStatus('SEARCHING')
    try {
      const response = await battleService.findOpponent(userId)

      if (response.status === 'FOUND') {
        setMatchId(response.matchId)
        setOpponent({
          id: response.opponentId,
          name: response.opponentName,
        })
        setCountdown(response.countdownSeconds)
        setMatchStatus('FOUND')

        // Запускаем отсчет до начала игры
        startCountdown(response.countdownSeconds)
      } else if (response.status === 'SEARCHING') {
        // Продолжаем поиск
        checkMatchmakingStatus()
      }
    } catch (error) {
      console.error('Ошибка поиска противника:', error)
      setMatchStatus('IDLE')
    }
  }

  // Проверка статуса матчмейкинга
  const checkMatchmakingStatus = () => {
    const checkInterval = setInterval(async () => {
      try {
        const response = await battleService.findOpponent(userId)

        if (response.status === 'FOUND') {
          clearInterval(checkInterval)
          setMatchId(response.matchId)
          setOpponent({
            id: response.opponentId,
            name: response.opponentName,
          })
          setCountdown(response.countdownSeconds)
          setMatchStatus('FOUND')
          startCountdown(response.countdownSeconds)
        }
      } catch (error) {
        console.error('Ошибка проверки статуса:', error)
        clearInterval(checkInterval)
        setMatchStatus('IDLE')
      }
    }, 2000)
  }

  // Отсчет до начала игры
  const startCountdown = (seconds) => {
    let count = seconds
    const countdownInterval = setInterval(() => {
      setCountdown(count)
      count--

      if (count < 0) {
        clearInterval(countdownInterval)
        startMultiplayerGame()
      }
    }, 1000)
  }

  // Запуск мультиплеерной игры
  const startMultiplayerGame = () => {
    setMatchStatus('PLAYING')
    setGameTime(60)
    setPlayerScore(0)
    setOpponentScore(0)
    setTargets([])

    // Таймер игры
    gameInterval.current = setInterval(() => {
      setGameTime((prev) => {
        if (prev <= 1) {
          endMultiplayerGame()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    // Создание целей
    targetInterval.current = setInterval(() => {
      createRandomTarget()
    }, 800)

    // Проверка состояния сессии (счет противника)
    sessionCheckInterval.current = setInterval(async () => {
      if (matchId) {
        try {
          const session = await battleService.getGameSession(matchId)
          setGameSession(session)

          // Обновляем счет противника
          if (session.player1Id === userId) {
            setOpponentScore(session.player2Score || 0)
          } else {
            setOpponentScore(session.player1Score || 0)
          }
        } catch (error) {
          console.error('Ошибка получения сессии:', error)
        }
      }
    }, 1000)
  }

  const createRandomTarget = () => {
    const randomType = getRandomDragonType()
    const dragonType = dragonTypes.find((dragon) => dragon.type === randomType)

    const newTarget = {
      id: Date.now() + Math.random(),
      x: Math.random() * 80 + 10,
      y: Math.random() * 70 + 15,
      size: dragonType.size,
      type: dragonType.type,
      lifetime: dragonType.lifetime,
      points: dragonType.points,
      color: dragonType.color,
      name: dragonType.name,
    }

    setTargets((prev) => [...prev, newTarget])

    setTimeout(() => {
      setTargets((prev) => prev.filter((target) => target.id !== newTarget.id))
    }, dragonType.lifetime)
  }

  const getRandomDragonType = () => {
    const random = Math.random()
    if (random < 0.4) return 'fast'
    if (random < 0.7) return 'normal'
    if (random < 0.9) return 'slow'
    return 'boss'
  }

  const hitTarget = async (targetId) => {
    const target = targets.find((t) => t.id === targetId)
    if (target) {
      setTargets((prev) => prev.filter((target) => target.id !== targetId))
      const newScore = playerScore + target.points
      setPlayerScore(newScore)

      // Синхронизируем счет с сервером
      if (matchId) {
        try {
          await battleService.updateScore(matchId, userId, newScore)
        } catch (error) {
          console.error('Ошибка обновления счета:', error)
        }
      }
    }
  }

  const endMultiplayerGame = async () => {
    // Очистка интервалов
    if (gameInterval.current) clearInterval(gameInterval.current)
    if (targetInterval.current) clearInterval(targetInterval.current)
    if (sessionCheckInterval.current)
      clearInterval(sessionCheckInterval.current)

    // Завершаем игру на сервере
    if (matchId) {
      try {
        const finishedGame = await battleService.finishGame(matchId)
        setGameSession(finishedGame)

        // Обновляем баланс монет
        if (finishedGame.winnerId === userId) {
          const newCoins = coins + 350 // WIN_REWARD
          setCoins(newCoins)
          localStorage.setItem('hypeDragon_coins', newCoins.toString())
        } else {
          const newCoins = coins - 100 // LOSS_PENALTY
          setCoins(Math.max(0, newCoins))
          localStorage.setItem(
            'hypeDragon_coins',
            Math.max(0, newCoins).toString(),
          )
        }
      } catch (error) {
        console.error('Ошибка завершения игры:', error)
      }
    }

    setMatchStatus('FINISHED')
    setTargets([])
  }

  const cancelMatchmaking = async () => {
    if (matchStatus === 'SEARCHING') {
      try {
        await battleService.cancelMatchmaking(userId)
      } catch (error) {
        console.error('Ошибка отмены поиска:', error)
      }
    }

    // Очистка интервалов
    if (gameInterval.current) clearInterval(gameInterval.current)
    if (targetInterval.current) clearInterval(targetInterval.current)
    if (sessionCheckInterval.current)
      clearInterval(sessionCheckInterval.current)

    setMatchStatus('IDLE')
    setTargets([])
  }

  const getTargetClass = (targetType) => {
    return `target target-${targetType}`
  }

  const getLifetimeText = (lifetime) => {
    return `${lifetime / 1000}сек`
  }

  const isWinner = gameSession?.winnerId === userId

  return (
    <div className="battle-page">
      <div className="battle-container">
        {/* Заголовок */}
        <header className="battle-header">
          <div className="header-content">
            <h1 className="battle-title">⚔️ Battle Arena</h1>
            <p className="battle-subtitle">
              Сражайся с другими игроками и зарабатывай монеты!
            </p>
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
                <div className="stat-value">{playerScore}</div>
                <div className="stat-label">Ваши очки</div>
              </div>
            </div>

            {matchStatus === 'PLAYING' && opponent && (
              <div className="stat-item">
                <div className="stat-icon">⚔️</div>
                <div className="stat-info">
                  <div className="stat-value">{opponentScore}</div>
                  <div className="stat-label">{opponent.name}</div>
                </div>
              </div>
            )}

            <div className="stat-item">
              <div className="stat-icon">⏱️</div>
              <div className="stat-info">
                <div className="stat-value">
                  {matchStatus === 'FOUND' ? countdown : gameTime}s
                </div>
                <div className="stat-label">
                  {matchStatus === 'FOUND' ? 'До начала' : 'Осталось'}
                </div>
              </div>
            </div>
          </div>

          {/* Состояния матчмейкинга */}
          {matchStatus === 'IDLE' && (
            <div className="start-section">
              <div className="game-rules">
                <h3>🎯 Мультиплеерная битва:</h3>
                <ul>
                  <li>• Играйте против реальных соперников</li>
                  <li>
                    • Победа:{' '}
                    <span style={{ color: '#44ff44' }}>+350 монет</span>
                  </li>
                  <li>
                    • Поражение:{' '}
                    <span style={{ color: '#ff4444' }}>-100 монет</span>
                  </li>
                  <li>• Время раунда: 60 секунд</li>
                  <li>• Уничтожайте драконов для набора очков</li>
                </ul>
              </div>
              <button className="start-button" onClick={findOpponent}>
                <span className="button-icon">🔍</span>
                Найти противника
              </button>
            </div>
          )}

          {matchStatus === 'SEARCHING' && (
            <div className="matchmaking-section">
              <div className="searching-animation">
                <div className="loading-spinner"></div>
                <h3>Поиск противника...</h3>
                <p>Ожидаем подходящего соперника</p>
                <button className="cancel-button" onClick={cancelMatchmaking}>
                  ❌ Отменить поиск
                </button>
              </div>
            </div>
          )}

          {matchStatus === 'FOUND' && (
            <div className="found-section">
              <div className="opponent-found">
                <h3>🎉 Противник найден!</h3>
                <p>
                  Соперник: <strong>{opponent?.name}</strong>
                </p>
                <div className="countdown">
                  Игра начнется через: <strong>{countdown} сек</strong>
                </div>
                <div className="game-starting">Готовьтесь к битве!</div>
              </div>
            </div>
          )}

          {/* Игровое поле */}
          {matchStatus === 'PLAYING' && (
            <div className="game-field" onClick={(e) => e.stopPropagation()}>
              <div className="game-header-info">
                <div className="time-left">Осталось: {gameTime}с</div>
                <div className="score-board">
                  <span>Вы: {playerScore}</span>
                  <span>VS</span>
                  <span>
                    {opponent?.name}: {opponentScore}
                  </span>
                </div>
                <button className="cancel-button" onClick={cancelMatchmaking}>
                  ❌ Сдаться
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

              <div className="game-instruction">
                🎯 Кликай по драконам для набора очков!
              </div>
            </div>
          )}

          {/* Результаты игры */}
          {matchStatus === 'FINISHED' && gameSession && (
            <div className="results-modal">
              <div className="modal-content">
                <h2>{isWinner ? '🎉 Победа!' : '💪 Хорошая попытка!'}</h2>

                <div className="results-stats">
                  <div className="result-item">
                    <span className="result-label">Ваш счет:</span>
                    <span className="result-value">{playerScore}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Счет {opponent?.name}:</span>
                    <span className="result-value">{opponentScore}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Результат:</span>
                    <span
                      className={`result-value ${isWinner ? 'win' : 'loss'}`}
                    >
                      {isWinner ? '+350 монет' : '-100 монет'}
                    </span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Общий баланс:</span>
                    <span className="result-value">
                      {coins.toLocaleString()}
                    </span>
                  </div>
                </div>

                <button
                  className="play-again-button"
                  onClick={() => {
                    setMatchStatus('IDLE')
                    setGameSession(null)
                  }}
                >
                  <span className="button-icon">🔄</span>
                  Играть снова
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Футер */}
        <footer className="battle-footer">
          <p>
            ✨ Сражайся с реальными противниками и становись королем арены! ✨
          </p>
        </footer>
      </div>
    </div>
  )
}

export default BattlePage
