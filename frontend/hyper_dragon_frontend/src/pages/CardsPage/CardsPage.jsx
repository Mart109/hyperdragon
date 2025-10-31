import React, { useState, useEffect } from 'react'
import './CardsPage.css'

// Импортируем изображения карточек
import goldenDragonImage from '../../assets/cards/golden_dragon.jpg'
import sportDragonImage from '../../assets/cards/sport_dragon.jpg'
import dragonLambaImage from '../../assets/cards/dragon_lamba.jpg'
import dragonImage from '../../assets/cards/dragon.jpg'

const CardsPage = () => {
  const [coins, setCoins] = useState(0)

  // Данные карточек из таблицы с импортированными изображениями
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
  ]

  // Загрузка данных игрока
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins')
    if (savedCoins) setCoins(parseInt(savedCoins))
  }, [])

  const handleBuyCard = (cardPrice, cardName) => {
    if (coins >= cardPrice) {
      setCoins((prev) => prev - cardPrice)
      localStorage.setItem('hypeDragon_coins', (coins - cardPrice).toString())
      alert(`🎉 Карта "${cardName}" успешно куплена!`)
    } else {
      alert('❌ Недостаточно монет для покупки!')
    }
  }

  return (
    <div className="cards-page">
      <div className="cards-container">
        {/* Заголовок */}
        <header className="cards-header">
          <div className="header-content">
            <h1 className="cards-title">🔥 Коллекция Карт</h1>
            <p className="cards-subtitle">
              Собирай карты и получай пассивный доход!
            </p>
          </div>
          <div className="header-decoration">
            <div className="decoration-coin">💰</div>
            <div className="decoration-gem">💎</div>
            <div className="decoration-fire">🔥</div>
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

        {/* Витрина карточек */}
        <div className="cards-showcase">
          <h2 className="section-title">
            <span className="title-icon">🛒</span>
            Витрина карт
          </h2>

          <div className="cards-grid">
            {cards.map((card) => (
              <div key={card.id} className="card-item">
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
                    {card.price <= 200
                      ? '⚡ Обычная'
                      : card.price <= 500
                      ? '🔷 Редкая'
                      : '💎 Эпическая'}
                  </div>
                </div>

                {/* Информация о карте */}
                <div className="card-info">
                  <h3 className="card-name">{card.name}</h3>
                  <p className="card-description">{card.description}</p>

                  <div className="card-stats">
                    <div className="stat-row">
                      <span className="stat-label">Цена:</span>
                      <span className="stat-value price">💰 {card.price}</span>
                    </div>
                    <div className="stat-row">
                      <span className="stat-label">Пассивный доход:</span>
                      <span className="stat-value income">
                        +{card.income}/мин
                      </span>
                    </div>
                  </div>

                  <button
                    className={`buy-button ${
                      coins < card.price ? 'disabled' : ''
                    }`}
                    onClick={() => handleBuyCard(card.price, card.name)}
                    disabled={coins < card.price}
                  >
                    {coins >= card.price
                      ? `Купить за ${card.price}💰`
                      : 'Недостаточно монет'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Футер */}
        <footer className="cards-footer">
          <p>✨ Коллекция драконов пополняется каждую неделю! ✨</p>
        </footer>
      </div>
    </div>
  )
}

export default CardsPage
