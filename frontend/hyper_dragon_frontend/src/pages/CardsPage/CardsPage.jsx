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
    if (savedCoins) setCoins(parseInt(savedCoins, 10)) // Используем radix 10 для parseInt
  }, [])

  const handleBuyCard = (cardPrice, cardName) => {
    if (coins >= cardPrice) {
      const newCoins = coins - cardPrice
      setCoins(newCoins)
      // Обновляем localStorage с новым значением
      localStorage.setItem('hypeDragon_coins', newCoins.toString())
      alert(`🎉 Карта "${cardName}" успешно куплена!`)
    } else {
      alert('❌ Недостаточно монет для покупки!')
    }
  }

  // Функция для определения редкости (для большей чистоты кода)
  const getCardRarity = (price) => {
    if (price <= 200) return '⚡ Обычная'
    if (price <= 500) return '🔷 Редкая'
    if (price <= 10000) return '💎 Эпическая'
    return '🏆 Легендарная'
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

                  <div className="card-rarity">{getCardRarity(card.price)}</div>
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
