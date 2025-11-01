import React, { useState, useEffect } from 'react'
import './TasksPage.css'

const QuestsPage = () => {
  const [activeTab, setActiveTab] = useState('daily')
  const [completedQuests, setCompletedQuests] = useState([])
  const [energy, setEnergy] = useState(350)
  const [maxEnergy] = useState(500)
  const [coins, setCoins] = useState(1250)
  const [gems, setGems] = useState(25)
  const [level, setLevel] = useState(8)

  // Загрузка прогресса из localStorage
  useEffect(() => {
    const savedCompleted = localStorage.getItem('hypeDragon_completedQuests')
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    const savedGems = localStorage.getItem('hypeDragon_gems')
    const savedLevel = localStorage.getItem('hypeDragon_level')

    if (savedCompleted) setCompletedQuests(JSON.parse(savedCompleted))
    if (savedCoins) setCoins(parseInt(savedCoins))
    if (savedGems) setGems(parseInt(savedGems))
    if (savedLevel) setLevel(parseInt(savedLevel))
  }, [])

  // Сохранение прогресса
  useEffect(() => {
    localStorage.setItem(
      'hypeDragon_completedQuests',
      JSON.stringify(completedQuests),
    )
    localStorage.setItem('hypeDragon_coins', coins.toString())
    localStorage.setItem('hypeDragon_gems', gems.toString())
    localStorage.setItem('hypeDragon_level', level.toString())
  }, [completedQuests, coins, gems, level])

  const quests = {
    daily: [
      {
        id: 1,
        title: '3 реферала',
        description: 'Пригласите 3 друга',
        reward: { coins: 10000 },
        progress: { current: 0, total: 100 },
        icon: '🖱️',
        type: 'referal',
      },
      {
        id: 2,
        title: 'Заработайте 5 уровень',
        description: 'получить 5 уровень',
        reward: { coins: 75, gems: 2 },
        progress: { current: 120, total: 200 },
        icon: '🎯',
        type: 'level',
      },
    ],
  }

  const handleClaimReward = (quest) => {
    if (completedQuests.includes(quest.id)) return

    const progress = quest.progress.current / quest.progress.total
    if (progress >= 1) {
      setCompletedQuests((prev) => [...prev, quest.id])
      setCoins((prev) => prev + quest.reward.coins)
      setGems((prev) => prev + quest.reward.gems)

      // Анимация получения награды
      alert(
        `🎉 Награда получена!\n+${quest.reward.coins} монет\n+${quest.reward.gems} самоцветов`,
      )
    }
  }

  const getProgressPercentage = (quest) => {
    return Math.min((quest.progress.current / quest.progress.total) * 100, 100)
  }

  const isQuestCompleted = (quest) => {
    return completedQuests.includes(quest.id)
  }

  const energyPercentage = (energy / maxEnergy) * 100

  return (
    <div className="quests-page">
      <div className="game-container">
        {/* Заголовок */}
        <header className="game-header">
          <div className="header-content">
            <h1 className="game-title">🎯 Задания</h1>
            <p className="game-subtitle">
              Выполняйте задания и получайте награды!
            </p>
          </div>
          <div className="header-decoration">
            <div className="decoration-coin">🎯</div>
            <div className="decoration-gem">🏆</div>
            <div className="decoration-fire">⚡</div>
          </div>
        </header>

        {/* Статистика */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon gold">💰</div>
            <div className="stat-content">
              <div className="stat-title">Монеты</div>
              <div className="stat-value">{coins.toLocaleString()}</div>
            </div>
          </div>
        </div>
        {/* Вкладки */}
        <div className="tabs-section">
          <div className="tabs-container">
            <div className="quests-grid">
              {quests[activeTab].map((quest) => {
                const progressPercent = getProgressPercentage(quest)
                const isCompleted = isQuestCompleted(quest)
                const canClaim = progressPercent >= 100 && !isCompleted

                return (
                  <div
                    key={quest.id}
                    className={`quest-card ${isCompleted ? 'completed' : ''} ${
                      canClaim ? 'can-claim' : ''
                    }`}
                  >
                    <div className="quest-header">
                      <div className="quest-icon">{quest.icon}</div>
                      <div className="quest-content">
                        <h4 className="quest-title">{quest.title}</h4>
                        <p className="quest-description">{quest.description}</p>
                      </div>
                      <div className="quest-reward">
                        <div className="reward-coins">
                          +{quest.reward.coins}💰
                        </div>
                        <div className="reward-gems">
                          +{quest.reward.gems}💎
                        </div>
                      </div>
                    </div>

                    <div className="quest-progress">
                      <div className="progress-info">
                        <span>
                          {quest.progress.current}/{quest.progress.total}
                        </span>
                        <span>{Math.round(progressPercent)}%</span>
                      </div>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{ width: `${progressPercent}%` }}
                        ></div>
                      </div>
                    </div>

                    <button
                      className={`claim-button ${canClaim ? 'active' : ''} ${
                        isCompleted ? 'claimed' : ''
                      }`}
                      onClick={() => handleClaimReward(quest)}
                      disabled={!canClaim || isCompleted}
                    >
                      {isCompleted
                        ? '🎉 Получено'
                        : canClaim
                        ? 'Забрать награду'
                        : 'В процессе'}
                    </button>
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        <footer className="game-footer">
          <p>✨ Выполняйте задания каждый день для максимальных наград! ✨</p>
        </footer>
      </div>
    </div>
  )
}

export default QuestsPage
