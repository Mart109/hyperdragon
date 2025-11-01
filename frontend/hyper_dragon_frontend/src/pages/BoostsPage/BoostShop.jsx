import React, { useState } from 'react';
import './BoostShop.css';

const BoostShop = () => {
  const [balance, setBalance] = useState(1250);
  const [boostLevels, setBoostLevels] = useState({
    multiClick: 1,
    energy: 1,
    clone: 0
  });

  const boosts = [
    {
      id: 'multiClick',
      name: 'Мульти-Клик',
      icon: '⚡',
      description: 'Увеличивает количество кликов за одно нажатие',
      price: 50,
      currentLevel: boostLevels.multiClick,
      effect: `Ур. ${boostLevels.multiClick} → ${boostLevels.multiClick + 1}`,
      rarity: 'EPIC'
    },
    {
      id: 'energy',
      name: 'Усилитель Энергии',
      icon: '🔋',
      description: 'Повышает максимальный запас энергии +20',
      price: 100,
      currentLevel: boostLevels.energy,
      effect: `Ур. ${boostLevels.energy} → ${boostLevels.energy + 1}`,
      rarity: 'RARE'
    },
    {
      id: 'clone',
      name: 'Создание Клона',
      icon: '👥',
      description: 'Клон автоматически тапает за вас каждую секунду',
      price: 200,
      currentLevel: boostLevels.clone,
      effect: `Клонов: ${boostLevels.clone} → ${boostLevels.clone + 1}`,
      rarity: 'LEGENDARY'
    }
  ];

  const buyBoost = (boost) => {
    if (balance >= boost.price) {
      setBalance(prev => prev - boost.price);
      setBoostLevels(prev => ({
        ...prev,
        [boost.id]: prev[boost.id] + 1
      }));
      
      // Здесь можно добавить вызов API для сохранения покупки
      console.log(`Куплен буст: ${boost.name}`);
    }
  };

  return (
    <div className="boost-shop">
      {/* Фоновые элементы */}
      <div className="background-effects">
        <div className="decoration-coin">🪙</div>
        <div className="decoration-gem">💎</div>
        <div className="decoration-fire">🔥</div>
      </div>

      <div className="shop-container">
        {/* Заголовок */}
        <div className="shop-header">
          <div className="header-content">
            <h1 className="shop-title">Магазин Бустов</h1>
            <p className="shop-subtitle">
              Улучшайте свои возможности и достигайте новых вершин!
            </p>
          </div>
          <div className="header-decoration">
            <span className="decoration-coin">🪙</span>
            <span className="decoration-gem">💎</span>
            <span className="decoration-fire">🔥</span>
          </div>
        </div>

        {/* Баланс */}
        <div className="balance-section">
          <div className="balance-card">
            <div className="balance-icon">💰</div>
            <div className="balance-content">
              <div className="balance-title">Ваш баланс</div>
              <div className="balance-value">{balance}</div>
            </div>
          </div>
        </div>

        {/* Витрина бустов */}
        <div className="boosts-showcase">
          <div className="section-title">
            <span className="title-icon">🚀</span>
            Доступные улучшения
          </div>

          <div className="boosts-grid">
            {boosts.map(boost => (
              <div key={boost.id} className={`boost-item ${boost.id === 'energy' ? 'energy-item' : ''}`}>
                <div className="boost-rarity">{boost.rarity}</div>
                
                <div className="boost-image-container">
                  <div className="boost-image-placeholder">
                    <div className="boost-illustration">
                      {boost.icon}
                    </div>
                  </div>
                </div>

                <div className="boost-info">
                  <h3 className="boost-name">{boost.name}</h3>
                  <p className="boost-description">{boost.description}</p>
                  
                  {/* Эффект в одну строку */}
                  <div className="boost-stats">
                    <div className="effect-single-line">
                      <span className="effect-label">Улучшение:</span>
                      <span className="effect-value">{boost.effect}</span>
                      <span className="price-badge">💵 {boost.price}</span>
                    </div>
                  </div>

                  {/* Кнопка покупки */}
                  <div className={`button-container ${boost.id === 'energy' ? 'energy-button' : ''}`}>
                    <button
                      className={`buy-button ${balance >= boost.price ? '' : 'disabled'}`}
                      onClick={() => buyBoost(boost)}
                      disabled={balance < boost.price}
                    >
                      {balance >= boost.price ? 'Приобрести' : 'Недостаточно'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Текущие статы */}
        <div className="stats-section">
          <div className="info-card">
            <div className="info-title">
              <span className="info-icon">📊</span>
              Ваши текущие улучшения
            </div>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">⚡</div>
                <div className="stat-content">
                  <div className="stat-name">Мульти-Клик</div>
                  <div className="stat-value">x{boostLevels.multiClick}</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🔋</div>
                <div className="stat-content">
                  <div className="stat-name">Уровень энергии</div>
                  <div className="stat-value">{boostLevels.energy}</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">👥</div>
                <div className="stat-content">
                  <div className="stat-name">Активные клоны</div>
                  <div className="stat-value">{boostLevels.clone}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Футер */}
        <div className="shop-footer">
          <p>Обновляйте улучшения для максимальной эффективности!</p>
        </div>
      </div>
    </div>
  );
};

export default BoostShop;