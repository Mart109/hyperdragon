import React, { useState, useEffect } from 'react'
import './CardsPage.css'

// Импортируем изображения карточек
import goldenDragonImage from '../../assets/cards/golden_dragon.jpg'
import sportDragonImage from '../../assets/cards/sport_dragon.jpg'
import dragonLambaImage from '../../assets/cards/dragon_lamba.jpg'
import dragonImage from '../../assets/cards/dragon.jpg'
import BlackDragonImage from '../../assets/cards/black_dragon.jpg'
import BattleDragon123Image from '../../assets/cards/battle_dragon123.jpg'
import CryptoDragonImage from '../../assets/cards/crypto_dragon.jpg'
import OfficeDragonImage from '../../assets/cards/office_dragon.jpg'
import FateDragonsImage from '../../assets/cards/fate_dragons.jpg'
import TreasureDragonImage from '../../assets/cards/golden_dragon2.jpg'

const CardsPage = () => {
  const [coins, setCoins] = useState(0)
  const [comboSequence, setComboSequence] = useState([])
  const [userCombination, setUserCombination] = useState([])
  const [showComboResult, setShowComboResult] = useState(false)
  const [comboMessage, setComboMessage] = useState('')
  const [comboWon, setComboWon] = useState(false)
  const [comboUsedToday, setComboUsedToday] = useState(false)
  const [ownedCards, setOwnedCards] = useState([])

  const cards = [
    {
      id: 1,
      cardName: 'golden_dragon',
      name: '3 Golden Dragons',
      price: 100,
      income: 50,
      description: 'Три золотых дракона приносят удачу',
      image: goldenDragonImage,
    },
    {
      id: 2,
      cardName: 'sport_dragon',
      name: 'Sport Dragon',
      price: 200,
      income: 100,
      description: 'Спортивный дракон полон энергии',
      image: sportDragonImage,
    },
    {
      id: 3,
      cardName: 'dragon_lamba',
      name: 'Dragon Lamba',
      price: 500,
      income: 300,
      description: 'Дракон Ламба - символ скорости',
      image: dragonLambaImage,
    },
    {
      id: 4,
      cardName: 'dragon',
      name: 'Dragon',
      price: 1000,
      income: 600,
      description: 'Могучий дракон - вершина силы',
      image: dragonImage,
    },
    {
      id: 5,
      cardName: 'black_dragon',
      name: 'Business Dragon',
      price: 1500,
      income: 700,
      description: 'Деловой дракон. Ваш капитал — его приоритет',
      image: BlackDragonImage,
    },
    {
      id: 6,
      cardName: 'battle_dragon123',
      name: 'Battle Dragon',
      price: 2000,
      income: 900,
      description: 'Боевой дракон. Он правит не только деньгами',
      image: BattleDragon123Image,
    },
    {
      id: 7,
      cardName: 'crypto_dragon',
      name: 'Crypto Dragon',
      price: 2500,
      income: 1000,
      description: 'Дракон в котором течет крипта',
      image: CryptoDragonImage,
    },
    {
      id: 8,
      cardName: 'office_dragon',
      name: 'Office Dragon',
      price: 5000,
      income: 2500,
      description:
        'Просто хочу отдых. В коде баги, в пещере — сокровища. Выбор очевиден',
      image: OfficeDragonImage,
    },
    {
      id: 9,
      cardName: 'fate_dragons',
      name: 'Fate Dragons',
      price: 7500,
      income: 3000,
      description:
        'Компания судьбы - это не просто компания, это судьба всего мира',
      image: FateDragonsImage,
    },
    {
      id: 10,
      cardName: 'golden_dragon2',
      name: 'Treasure Dragon',
      price: 100000,
      income: 25000,
      description: 'Дракон-сокровище. Самый ценный актив в портфеле',
      image: TreasureDragonImage,
    },
  ]

  // Загрузка данных игрока
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    const savedOwnedCards = localStorage.getItem('hypeDragon_ownedCards')
    const savedComboDate = localStorage.getItem('hypeDragon_comboDate')
    const savedComboWon = localStorage.getItem('hypeDragon_comboWon')
    const savedComboSequence = localStorage.getItem('hypeDragon_comboSequence')

    if (savedCoins) setCoins(parseInt(savedCoins, 10))
    if (savedOwnedCards) setOwnedCards(JSON.parse(savedOwnedCards))

    // Проверяем актуальность комбинации дня
    const today = new Date().toDateString()
    if (savedComboDate === today) {
      setComboUsedToday(true)
      if (savedComboWon === 'true') setComboWon(true)
      if (savedComboSequence) setComboSequence(JSON.parse(savedComboSequence))
    } else {
      // Новый день - новая комбинация
      generateNewCombo()
      localStorage.setItem('hypeDragon_comboDate', today)
      localStorage.setItem('hypeDragon_comboWon', 'false')
    }
  }, [])

  // Генерация случайной комбинации из 4 уникальных карточек
  const generateNewCombo = () => {
    const uniqueNumbers = new Set()
    while (uniqueNumbers.size < 4) {
      const randomNum = Math.floor(Math.random() * 10) + 1 // числа от 1 до 10
      uniqueNumbers.add(randomNum)
    }
    const newCombo = Array.from(uniqueNumbers)
    setComboSequence(newCombo)
    setUserCombination([])
    setShowComboResult(false)
    setComboMessage('')
    setComboWon(false)
    setComboUsedToday(false)

    localStorage.setItem('hypeDragon_comboSequence', JSON.stringify(newCombo))
    localStorage.setItem('hypeDragon_comboWon', 'false')
  }

  // Автоматическое добавление купленных карт в комбинацию
  useEffect(() => {
    if (comboSequence.length === 0 || comboWon || comboUsedToday) return

    const newUserCombination = [...userCombination]
    let updated = false

    // Проверяем каждую позицию в комбинации
    comboSequence.forEach((requiredCardId, index) => {
      // Если позиция пустая и у нас есть нужная карта
      if (!newUserCombination[index] && ownedCards.includes(requiredCardId)) {
        newUserCombination[index] = requiredCardId
        updated = true
      }
    })

    if (updated) {
      setUserCombination(newUserCombination)

      // Проверяем комбинацию если все 4 карты на месте
      if (
        newUserCombination.length === 4 &&
        newUserCombination.every((card) => card)
      ) {
        setTimeout(() => checkCombo(newUserCombination), 500)
      }
    }
  }, [ownedCards, comboSequence])

  // Проверка комбинации
  const checkCombo = (userCombo) => {
    const isWin = userCombo.every(
      (cardId, index) => cardId === comboSequence[index],
    )

    if (isWin) {
      const reward = 10000
      const newCoins = coins + reward
      setCoins(newCoins)
      setComboWon(true)
      setComboUsedToday(true)

      localStorage.setItem('hypeDragon_coins', newCoins.toString())
      localStorage.setItem('hypeDragon_comboWon', 'true')

      setComboMessage(
        `🎉 Поздравляем! Вы выиграли ${reward.toLocaleString()} монет!`,
      )
    } else {
      setComboMessage('')
    }

    setShowComboResult(true)
  }

  // Покупка карты
  const handleBuyCard = (cardPrice, cardName, cardId) => {
    if (coins >= cardPrice) {
      const newCoins = coins - cardPrice
      const newOwnedCards = [...ownedCards, cardId]

      setCoins(newCoins)
      setOwnedCards(newOwnedCards)

      localStorage.setItem('hypeDragon_coins', newCoins.toString())
      localStorage.setItem(
        'hypeDragon_ownedCards',
        JSON.stringify(newOwnedCards),
      )

      alert(`🎉 Карта "${cardName}" успешно куплена!`)
    } else {
      alert('❌ Недостаточно монет для покупки!')
    }
  }

  // Функция для определения редкости
  const getCardRarity = (price) => {
    if (price <= 200) return '⚡ Обычная'
    if (price <= 500) return '🔷 Редкая'
    if (price <= 10000) return '💎 Эпическая'
    return '🏆 Легендарная'
  }

  // Получение объекта карточки по ID
  const getCardById = (id) => cards.find((card) => card.id === id)

  // Проверка владения картой
  const isCardOwned = (cardId) => ownedCards.includes(cardId)

  return (
    <div className="cards-page">
      <div className="cards-container">
        {/* Заголовок */}
        <header className="cards-header">
          <div className="header-content">
            <h1 className="cards-title">🔥 Коллекция Карт</h1>
            <p className="cards-subtitle">
              Собирай карты, комбинации и получай пассивный доход!
            </p>
          </div>
          <div className="header-decoration">
            <div className="decoration-coin">💰</div>
            <div className="decoration-gem">💎</div>
            <div className="decoration-fire">🔥</div>
          </div>
        </header>

        {/* Секция комбинаций */}
        <div className="combo-section">
          <div className="combo-card">
            <h2 className="combo-title">
              <span className="combo-icon">🎮</span>
              Комбинация Дня
              {comboWon && <span className="combo-badge won">Победа!</span>}
            </h2>

            <div className="combo-info">
              <p className="combo-description">
                {comboWon
                  ? '🎊 Поздравляем! Вы собрали комбинацию и получили 10,000 монет!'
                  : '✨ Покупайте карты - если они в комбинации дня, они автоматически добавятся!'}
              </p>

              <div className="combo-display">
                <div className="user-combo">
                  <h3>Комбинация дня:</h3>
                  <div className="combo-sequence">
                    {[0, 1, 2, 3].map((index) => (
                      <div key={index} className="combo-slot">
                        {userCombination[index] ? (
                          <div className="combo-card-preview">
                            <img
                              src={getCardById(userCombination[index]).image}
                              alt={getCardById(userCombination[index]).name}
                              className="combo-card-image"
                            />
                            <span className="combo-card-name">
                              {getCardById(userCombination[index]).name}
                            </span>
                          </div>
                        ) : (
                          <div className="combo-slot-empty">?</div>
                        )}
                      </div>
                    ))}
                  </div>

                  {!comboWon && (
                    <div className="combo-progress">
                      <div className="progress-text">
                        Собрано: {userCombination.filter((card) => card).length}
                        /4
                      </div>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{
                            width: `${
                              (userCombination.filter((card) => card).length /
                                4) *
                              100
                            }%`,
                          }}
                        ></div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {showComboResult && comboMessage && (
                <div
                  className={`combo-result ${
                    comboMessage.includes('🎉') ? 'success' : 'error'
                  }`}
                >
                  {comboMessage}
                </div>
              )}

              <div className="combo-reward">
                💰 Награда за комбинацию: <strong>10,000 монет</strong>
              </div>
            </div>
          </div>
        </div>

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
          <div className="owned-cards-counter">
            📊 Куплено карт: {ownedCards.length}/10
          </div>
        </div>

        {/* Витрина карточек */}
        <div className="cards-showcase">
          <h2 className="section-title">
            <span className="title-icon">🛒</span>
            Витрина карт
          </h2>

          <div className="cards-grid">
            {cards.map((card) => {
              const isOwned = isCardOwned(card.id)
              const isInCombo = comboSequence.includes(card.id)
              const isInUserCombo = userCombination.includes(card.id)

              return (
                <div
                  key={card.id}
                  className={`card-item ${isOwned ? 'owned' : ''}`}
                >
                  {/* Большой блок для изображения */}
                  <div className="card-image-container">
                    <div className="card-image-placeholder">
                      <img
                        src={card.image}
                        alt={card.name}
                        className="card-image"
                      />
                    </div>

                    <div className="card-rarity">
                      {getCardRarity(card.price)}
                    </div>

                    {/* Статус карты в комбинации */}
                    {isOwned && isInCombo && (
                      <div className="combo-status">
                        {isInUserCombo
                          ? '✅ В комбинации'
                          : '⭐ В комбинации дня'}
                      </div>
                    )}
                  </div>

                  {/* Информация о карте */}
                  <div className="card-info">
                    <h3 className="card-name">{card.name}</h3>
                    <p className="card-description">{card.description}</p>

                    <div className="card-stats">
                      <div className="stat-row">
                        <span className="stat-label">Цена:</span>
                        <span className="stat-value price">
                          💰 {card.price.toLocaleString()}
                        </span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Пассивный доход:</span>
                        <span className="stat-value income">
                          +{card.income.toLocaleString()}/мин
                        </span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Статус:</span>
                        <span className="stat-value status">
                          {isOwned ? '✅ Приобретена' : '❌ Не куплена'}
                        </span>
                      </div>
                    </div>

                    <button
                      className={`buy-button ${
                        coins < card.price || isOwned ? 'disabled' : ''
                      }`}
                      onClick={() =>
                        handleBuyCard(card.price, card.name, card.id)
                      }
                      disabled={coins < card.price || isOwned}
                    >
                      {isOwned
                        ? '✅ Куплена'
                        : coins >= card.price
                        ? `Купить за ${card.price.toLocaleString()}💰`
                        : 'Недостаточно монет'}
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Футер */}
        <footer className="cards-footer">
          <p>✨ Коллекция драконов пополняется каждую неделю! ✨</p>
          <p>🎮 Новая комбинация каждый день!</p>
        </footer>
      </div>
    </div>
  )
}

export default CardsPage
