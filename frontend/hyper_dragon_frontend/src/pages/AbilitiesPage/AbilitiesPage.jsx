import React, { useState, useEffect } from 'react';
import './AbilitiesPage.css';

const AbilitiesPage = () => {
  const [coins, setCoins] = useState(0);
  const [activeCategory, setActiveCategory] = useState('boosts');
  const [playerAbilities, setPlayerAbilities] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [modalData, setModalData] = useState(null);
  const [purchaseHistory, setPurchaseHistory] = useState([]);

  // Загрузка данных игрока
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins');
    const savedAbilities = localStorage.getItem('hypeDragon_abilities');
    const savedHistory = localStorage.getItem('hypeDragon_purchaseHistory');

    if (savedCoins) {
      setCoins(parseInt(savedCoins));
    }
    if (savedAbilities) {
      setPlayerAbilities(JSON.parse(savedAbilities));
    }
    if (savedHistory) {
      setPurchaseHistory(JSON.parse(savedHistory));
    }
  }, []);

  // Сохранение данных
  const saveGameData = (newCoins, newAbilities, newHistory) => {
    localStorage.setItem('hypeDragon_coins', newCoins.toString());
    localStorage.setItem('hypeDragon_abilities', JSON.stringify(newAbilities));
    localStorage.setItem('hypeDragon_purchaseHistory', JSON.stringify(newHistory));
  };

  // Способности магазина
  const abilities = {
    boosts: [
      {
        id: 'damage_boost',
        name: 'Усиление Атаки',
        icon: '⚔️',
        rarity: 'basic',
        description: 'Постоянно увеличивает вашу базовую атаку на 5 единиц за уровень',
        price: 200,
        maxLevel: 10,
        effect: { attack: 5 },
        type: 'permanent'
      },
      {
        id: 'health_boost',
        name: 'Усиление Здоровья',
        icon: '❤️',
        rarity: 'basic',
        description: 'Увеличивает максимальное здоровье на 20 единиц за уровень',
        price: 250,
        maxLevel: 10,
        effect: { maxHealth: 20 },
        type: 'permanent'
      },
      {
        id: 'shield_boost',
        name: 'Энергетический Щит',
        icon: '🛡️',
        rarity: 'basic',
        description: 'Добавляет постоянную защиту, снижающую получаемый урон',
        price: 300,
        maxLevel: 8,
        effect: { armor: 5 },
        type: 'permanent'
      }
    ],
    abilities: [
      {
        id: 'time_slow',
        name: 'Замедление Времени',
        icon: '⏰',
        rarity: 'medium',
        description: 'Замедляет врагов на 3 хода. Враги пропускают каждый второй ход',
        price: 800,
        maxLevel: 3,
        effect: { slowDuration: 3 },
        type: 'active',
        cooldown: 8,
        usage: 'battle'
      },
      {
        id: 'double_strike',
        name: 'Двойной Удар',
        icon: '⚡',
        rarity: 'medium',
        description: 'Следующая атака наносит двойной урон. Идеально против боссов',
        price: 1200,
        maxLevel: 2,
        effect: { damageMultiplier: 2 },
        type: 'active',
        cooldown: 5,
        usage: 'battle'
      },
      {
        id: 'healing_aura',
        name: 'Аура Исцеления',
        icon: '💫',
        rarity: 'epic',
        description: 'Исцеляет 15% от максимального здоровья каждый ход в течение 5 ходов',
        price: 2000,
        maxLevel: 1,
        effect: { healPercent: 15, duration: 5 },
        type: 'active',
        cooldown: 10,
        usage: 'battle'
      }
    ]
  };

  // Получение текущего уровня способности
  const getAbilityLevel = (abilityId) => {
    return playerAbilities[abilityId]?.level || 0;
  };

  // Получение следующей цены улучшения
  const getNextPrice = (ability, currentLevel) => {
    if (currentLevel >= ability.maxLevel) return null;
    return ability.price * (currentLevel + 1);
  };

  // Покупка/улучшение способности
  const handlePurchase = (ability) => {
    const currentLevel = getAbilityLevel(ability.id);
    const nextPrice = getNextPrice(ability, currentLevel);

    if (currentLevel >= ability.maxLevel) {
      showPurchaseModal('Максимальный уровень', 'Эта способность уже достигла максимального уровня!', 'info');
      return;
    }

    if (coins < nextPrice) {
      showPurchaseModal('Недостаточно монет', `Вам нужно ${nextPrice} монет для улучшения этой способности.`, 'error');
      return;
    }

    const newLevel = currentLevel + 1;
    const newAbilities = {
      ...playerAbilities,
      [ability.id]: {
        level: newLevel,
        ...ability
      }
    };

    const newCoins = coins - nextPrice;
    const newHistory = [...purchaseHistory, {
      ability: ability.name,
      level: newLevel,
      price: nextPrice,
      timestamp: new Date().toLocaleString()
    }];

    setCoins(newCoins);
    setPlayerAbilities(newAbilities);
    setPurchaseHistory(newHistory);
    saveGameData(newCoins, newAbilities, newHistory);

    showPurchaseModal(
      'Успешная покупка!', 
      `Вы улучшили "${ability.name}" до уровня ${newLevel}!`, 
      'success'
    );
  };

  // Показать модальное окно
  const showPurchaseModal = (title, message, type = 'info') => {
    setModalData({ title, message, type });
    setShowModal(true);
  };

  // Закрыть модальное окно
  const closeModal = () => {
    setShowModal(false);
    setModalData(null);
  };

  // Получение активных способностей
  const getActiveAbilities = () => {
    return Object.values(playerAbilities).filter(ability => ability.level > 0);
  };

  // Рендер способности
  const renderAbilityCard = (ability) => {
    const currentLevel = getAbilityLevel(ability.id);
    const nextPrice = getNextPrice(ability, currentLevel);
    const canUpgrade = currentLevel < ability.maxLevel && coins >= nextPrice;

    return (
      <div key={ability.id} className={`ability-card ${ability.rarity}`}>
        <div className="ability-header">
          <div className="ability-icon">{ability.icon}</div>
          <div>
            <div className="ability-title">{ability.name}</div>
            <div className="ability-rarity">
              {ability.rarity === 'basic' && 'Базовая'}
              {ability.rarity === 'medium' && 'Средняя'}
              {ability.rarity === 'epic' && 'Эпическая'}
            </div>
          </div>
        </div>

        <div className="ability-description">
          {ability.description}
        </div>

        <div className="ability-stats">
          <div className="ability-stat">
            <span className="stat-icon">📊</span>
            <span>Уровень: {currentLevel}/{ability.maxLevel}</span>
          </div>
          <div className="ability-stat">
            <span className="stat-icon">💰</span>
            <span>Цена: {nextPrice || 'Макс.'}</span>
          </div>
          {ability.type === 'active' && (
            <>
              <div className="ability-stat">
                <span className="stat-icon">⏱️</span>
                <span>Перезарядка: {ability.cooldown} ходов</span>
              </div>
              <div className="ability-stat">
                <span className="stat-icon">🎯</span>
                <span>Тип: Активная</span>
              </div>
            </>
          )}
        </div>

        <div className="ability-actions">
          <button 
            className={`buy-button ${canUpgrade ? 'upgrade-button' : ''}`}
            onClick={() => handlePurchase(ability)}
            disabled={!canUpgrade && currentLevel < ability.maxLevel}
          >
            {currentLevel === 0 ? 'Купить' : 'Улучшить'}
            {nextPrice && ` (${nextPrice})`}
          </button>
          <button className="info-button" title="Информация о способности">
            ℹ️
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="ability-shop">
      <div className="shop-container">
        <header className="shop-header">
          <h1 className="shop-title">🏪 Магазин Способностей</h1>
          <p className="shop-subtitle">
            Улучшайте своего героя и получайте мощные способности для PvP боев!
          </p>
        </header>

        <div className="balance-section">
          <div className="balance-card">
            <div className="balance-icon">💰</div>
            <div className="balance-content">
              <div className="balance-title">Ваш баланс</div>
              <div className="balance-value">{coins.toLocaleString()} монет</div>
            </div>
          </div>
        </div>

        <div className="shop-main">
          {/* Навигация по категориям */}
          <div className="shop-categories">
            <button 
              className={`category-button ${activeCategory === 'boosts' ? 'active' : ''}`}
              onClick={() => setActiveCategory('boosts')}
            >
              📈 Усиления
            </button>
            <button 
              className={`category-button ${activeCategory === 'abilities' ? 'active' : ''}`}
              onClick={() => setActiveCategory('abilities')}
            >
              ✨ Способности
            </button>
          </div>

          {/* Сетка способностей */}
          <div className="abilities-grid">
            {abilities[activeCategory].map(renderAbilityCard)}
          </div>

          {/* Активные способности */}
          {getActiveAbilities().length > 0 && (
            <div className="active-abilities">
              <h3>🎯 Ваши Улучшения</h3>
              <div className="active-abilities-grid">
                {getActiveAbilities().map(ability => (
                  <div key={ability.id} className="active-ability-item">
                    <div className="active-ability-icon">{ability.icon}</div>
                    <div className="active-ability-info">
                      <div className="active-ability-name">{ability.name}</div>
                      <div className="active-ability-level">Уровень {ability.level}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Модальное окно */}
        {showModal && modalData && (
          <div className="ability-modal">
            <div className="modal-content">
              <div className="modal-icon">
                {modalData.type === 'success' && '🎉'}
                {modalData.type === 'error' && '❌'}
                {modalData.type === 'info' && 'ℹ️'}
              </div>
              <h2 className="modal-title">{modalData.title}</h2>
              <p className="modal-message">{modalData.message}</p>
              <div className="modal-actions">
                <button className="modal-button confirm" onClick={closeModal}>
                  Понятно
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AbilitiesPage;