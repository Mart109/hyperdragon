import React, { useState, useEffect, useCallback } from 'react';
import './BattlePage.css';

// Типы клеток поля с эмодзи
const CELL_TYPES = {
  EMPTY: { 
    name: 'Пусто', 
    color: 'transparent', 
    icon: ' ',
    description: 'Пустая клетка',
    type: 'EMPTY'
  },
  PLAYER: { 
    name: 'Игрок', 
    color: 'transparent', 
    icon: '🤺',
    description: 'Ваш персонаж',
    type: 'PLAYER'
  },
  TREASURE_SMALL: { 
    name: 'Малое сокровище', 
    color: 'transparent', 
    icon: '💰',
    description: '+25 очков',
    points: 25,
    type: 'TREASURE_SMALL'
  },
  TREASURE_MEDIUM: { 
    name: 'Среднее сокровище', 
    color: 'transparent', 
    icon: '💎',
    description: '+50 очков',
    points: 50,
    type: 'TREASURE_MEDIUM'
  },
  TREASURE_LARGE: { 
    name: 'Большое сокровище', 
    color: 'transparent', 
    icon: '🏆',
    description: '+100 очков', 
    points: 100,
    type: 'TREASURE_LARGE'
  },
  ENEMY_WEAK: { 
    name: 'Гоблин', 
    color: 'transparent', 
    icon: '👺',
    description: 'Урон: 5',
    damage: 5,
    type: 'ENEMY_WEAK',
    speed: 1
  },
  ENEMY_MEDIUM: { 
    name: 'Орк', 
    color: 'transparent', 
    icon: '🧌',
    description: 'Урон: 8',
    damage: 8,
    type: 'ENEMY_MEDIUM',
    speed: 1
  },
  ENEMY_STRONG: { 
    name: 'Тролль', 
    color: 'transparent', 
    icon: '🧌',
    description: 'Урон: 10',
    damage: 10,
    type: 'ENEMY_STRONG',
    speed: 1
  },
  ENEMY_ARCHER: { 
    name: 'Темный лучник', 
    color: 'transparent', 
    icon: '🏹',
    description: 'Дальний урон: 6',
    damage: 6,
    type: 'ENEMY_ARCHER',
    speed: 1,
    range: 2
  },
  ENEMY_MAGE: { 
    name: 'Маг', 
    color: 'transparent', 
    icon: '🧙',
    description: 'Магический урон: 8',
    damage: 8,
    type: 'ENEMY_MAGE',
    speed: 1,
    range: 3
  },
  TRAP_VISIBLE: { 
    name: 'Ловушка', 
    color: 'transparent', 
    icon: '⚠️',
    description: 'Урон: 8',
    damage: 8,
    type: 'TRAP_VISIBLE'
  },
  TRAP_HIDDEN: { 
    name: 'Скрытая ловушка', 
    color: 'transparent', 
    icon: ' ',
    description: 'Скрытая ловушка! Урон: 12',
    damage: 12,
    type: 'TRAP_HIDDEN',
    hidden: true
  },
  HEAL_SMALL: { 
    name: 'Малое лечение', 
    color: 'transparent', 
    icon: '💚',
    description: '+40 здоровья',
    heal: 40,
    type: 'HEAL_SMALL'
  },
  HEAL_LARGE: { 
    name: 'Большое лечение', 
    color: 'transparent', 
    icon: '💙',
    description: '+80 здоровья',
    heal: 80,
    type: 'HEAL_LARGE'
  },
  BOSS: { 
    name: 'Дракон', 
    color: 'transparent', 
    icon: '🐉',
    description: 'Урон: 15, Награда: 300',
    damage: 15,
    points: 300,
    type: 'BOSS',
    speed: 1
  },
  QUEST: { 
    name: 'Древний свиток', 
    color: 'transparent', 
    icon: '📜',
    description: '+200 очков',
    points: 200,
    type: 'QUEST'
  },
  PORTAL: { 
    name: 'Магический портал', 
    color: 'transparent', 
    icon: '🌀',
    description: 'Телепортация',
    type: 'PORTAL'
  },
  ARMOR: { 
    name: 'Мифриловая броня', 
    color: 'transparent', 
    icon: '🛡️',
    description: '+30 брони',
    armor: 30,
    type: 'ARMOR'
  },
  WEAPON: { 
    name: 'Легендарный меч', 
    color: 'transparent', 
    icon: '⚔️',
    description: '+25 к атаке',
    attack: 25,
    type: 'WEAPON'
  },
  WALL: {
    name: 'Каменная стена',
    color: 'transparent',
    icon: '🧱',
    description: 'Непроходимое препятствие',
    type: 'WALL'
  },
  SPAWNER: {
    name: 'Портал монстров',
    color: 'transparent',
    icon: '⚫',
    description: 'Порождает монстров',
    type: 'SPAWNER'
  }
};

// Уровни сложности
const DIFFICULTY_LEVELS = [
  { 
    turns: 25, 
    reward: 500, 
    name: "Новичок",
    description: "Идеально для обучения",
    enemyRatio: 0.04,
    trapRatio: 0.03,
    wallRatio: 0.01,
    spawnerCount: 1,
    fieldSize: 10
  },
  { 
    turns: 40, 
    reward: 1000, 
    name: "Воин", 
    description: "Легкие испытания",
    enemyRatio: 0.06,
    trapRatio: 0.05,
    wallRatio: 0.02,
    spawnerCount: 2,
    fieldSize: 12
  },
  { 
    turns: 60, 
    reward: 2000, 
    name: "Мастер",
    description: "Средняя сложность", 
    enemyRatio: 0.08,
    trapRatio: 0.07,
    wallRatio: 0.03,
    spawnerCount: 3,
    fieldSize: 14
  },
  { 
    turns: 80, 
    reward: 4000, 
    name: "Легенда",
    description: "Для опытных игроков",
    enemyRatio: 0.10,
    trapRatio: 0.09,
    wallRatio: 0.04,
    spawnerCount: 4,
    fieldSize: 16
  }
];

// Компонент кнопки способности
const AbilityButton = ({ ability, cooldowns, activeEffects, onUse }) => {
  const cooldown = cooldowns[ability.id] || 0;
  const isActive = activeEffects.some(effect => effect.abilityId === ability.id);
  const canUse = cooldown === 0;
  
  return (
    <button
      className={`ability-button ${ability.rarity} ${isActive ? 'active' : ''} ${!canUse ? 'cooldown' : ''}`}
      onClick={() => canUse && onUse(ability)}
      disabled={!canUse}
      title={`${ability.name} - ${ability.description}\nПерезарядка: ${ability.cooldown} ходов`}
    >
      <span className="ability-icon">{ability.icon}</span>
      <span className="ability-name">{ability.name}</span>
      {cooldown > 0 && (
        <span className="cooldown-counter">{cooldown}</span>
      )}
      {isActive && <span className="active-indicator">⚡</span>}
    </button>
  );
};

const BattlePage = () => {
  const [coins, setCoins] = useState(0);
  const [gameState, setGameState] = useState('MENU');
  const [selectedDifficulty, setSelectedDifficulty] = useState(0);
  const [gameField, setGameField] = useState([]);
  const [playerPosition, setPlayerPosition] = useState({ x: 0, y: 0 });
  const [playerAbilities, setPlayerAbilities] = useState({});
  const [activeEffects, setActiveEffects] = useState([]);
  const [abilityCooldowns, setAbilityCooldowns] = useState({});
  const [enemyMovePending, setEnemyMovePending] = useState(false);
  
  const [playerStats, setPlayerStats] = useState({
    health: 100,
    maxHealth: 100,
    armor: 0,
    attack: 10,
    turnsLeft: 0,
    totalTurns: 0,
    score: 0,
    inventory: [],
    kills: 0,
    level: 1
  });
  const [currentTurn, setCurrentTurn] = useState(0);
  const [gameLog, setGameLog] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [screenShake, setScreenShake] = useState(false);
  const [combo, setCombo] = useState(0);
  const [comboTimer, setComboTimer] = useState(null);
  const [fieldSize, setFieldSize] = useState(12);

  // Определение размера экрана
  const getFieldSize = () => {
    const width = window.innerWidth;
    if (width < 480) return 8;
    if (width < 768) return 10;
    if (width < 1024) return 12;
    return DIFFICULTY_LEVELS[selectedDifficulty].fieldSize;
  };

  // Загрузка данных игрока
  useEffect(() => {
    const savedCoins = localStorage.getItem('hypeDragon_coins');
    const savedAbilities = localStorage.getItem('hypeDragon_abilities');
    
    if (savedCoins) {
      setCoins(parseInt(savedCoins));
    } else {
      const startCoins = 1000;
      setCoins(startCoins);
      localStorage.setItem('hypeDragon_coins', startCoins.toString());
    }
    
    if (savedAbilities) {
      setPlayerAbilities(JSON.parse(savedAbilities));
    }
  }, []);

  // Адаптация к размеру экрана
  useEffect(() => {
    const handleResize = () => {
      setFieldSize(getFieldSize());
    };

    window.addEventListener('resize', handleResize);
    setFieldSize(getFieldSize());

    return () => window.removeEventListener('resize', handleResize);
  }, [selectedDifficulty]);

  // Эффект для комбо
  useEffect(() => {
    if (combo > 0) {
      if (comboTimer) {
        clearTimeout(comboTimer);
      }
      const timer = setTimeout(() => {
        setCombo(0);
        setGameLog(prev => [...prev.slice(-9), `💔 Комбо потеряно!`]);
      }, 5000);
      setComboTimer(timer);
      return () => clearTimeout(timer);
    }
  }, [combo]);

  // Функция расчета бонусов от способностей
  const calculateAbilityBonuses = () => {
    let attack = 0;
    let armor = 0;
    let extraHealth = 0;
    
    Object.values(playerAbilities).forEach(ability => {
      if (ability.level > 0) {
        switch (ability.id) {
          case 'damage_boost':
            attack += ability.effect.attack * ability.level;
            break;
          case 'shield_boost':
            armor += ability.effect.armor * ability.level;
            break;
          case 'health_boost':
            extraHealth += ability.effect.maxHealth * ability.level;
            break;
          default:
            break;
        }
      }
    });
    
    return { attack, armor, extraHealth };
  };

  // Случайное размещение объектов
  const getRandomObject = (difficulty, isSpawner = false) => {
    const random = Math.random();
    
    if (random < 0.70) return 'EMPTY';
    if (random < 0.75) return 'TREASURE_SMALL';
    if (random < 0.78) return 'TREASURE_MEDIUM';
    if (random < 0.79) return 'TREASURE_LARGE';
    if (random < 0.79 + difficulty.enemyRatio * 0.15) return 'ENEMY_WEAK';
    if (random < 0.79 + difficulty.enemyRatio * 0.25) return 'ENEMY_MEDIUM';
    if (random < 0.79 + difficulty.enemyRatio * 0.35) return 'ENEMY_STRONG';
    if (random < 0.79 + difficulty.enemyRatio * 0.45) return 'ENEMY_ARCHER';
    if (random < 0.79 + difficulty.enemyRatio * 0.50) return 'ENEMY_MAGE';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio * 0.6) return 'TRAP_VISIBLE';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio) return 'TRAP_HIDDEN';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.04) return 'HEAL_SMALL';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.06) return 'HEAL_LARGE';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.07) return 'ARMOR';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.08) return 'WEAPON';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.082) return 'QUEST';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.084) return 'PORTAL';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.085) return 'BOSS';
    if (isSpawner && random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + 0.09) return 'SPAWNER';
    if (random < 0.79 + difficulty.enemyRatio + difficulty.trapRatio + difficulty.wallRatio) return 'WALL';
    
    return 'EMPTY';
  };

  // Инициализация игрового поля
  const initializeGameField = () => {
    const currentFieldSize = fieldSize;
    console.log(`🔄 Создаем адаптивное поле ${currentFieldSize}x${currentFieldSize}...`);
    
    const field = [];
    const difficulty = DIFFICULTY_LEVELS[selectedDifficulty];
    const center = Math.floor(currentFieldSize / 2);
    
    // Создаем пустое поле
    for (let y = 0; y < currentFieldSize; y++) {
      const row = [];
      for (let x = 0; x < currentFieldSize; x++) {
        row.push({ ...CELL_TYPES.EMPTY });
      }
      field.push(row);
    }

    // Размещаем объекты
    for (let y = 0; y < currentFieldSize; y++) {
      for (let x = 0; x < currentFieldSize; x++) {
        const distanceToCenter = Math.abs(x - center) + Math.abs(y - center);
        if (distanceToCenter > 2) {
          const objectType = getRandomObject(difficulty, true);
          field[y][x] = { ...CELL_TYPES[objectType] };
        }
      }
    }

    // Размещаем игрока в центре
    field[center][center] = { ...CELL_TYPES.PLAYER };
    setPlayerPosition({ x: center, y: center });
    
    // Размещаем спавнеры монстров
    const placeSpawners = (count) => {
      let placedCount = 0;
      let attempts = 0;
      while (placedCount < count && attempts < 100) {
        const x = Math.floor(Math.random() * currentFieldSize);
        const y = Math.floor(Math.random() * currentFieldSize);
        const distanceToPlayer = Math.abs(x - center) + Math.abs(y - center);
        
        if (distanceToPlayer > 3 && field[y][x].type === 'EMPTY') {
          field[y][x] = { ...CELL_TYPES.SPAWNER };
          placedCount++;
        }
        attempts++;
      }
    };

    // Гарантированно размещаем полезные объекты
    const placeGuaranteedObject = (type, count = 1) => {
      let placedCount = 0;
      let attempts = 0;
      while (placedCount < count && attempts < 100) {
        const x = Math.floor(Math.random() * currentFieldSize);
        const y = Math.floor(Math.random() * currentFieldSize);
        const distanceToPlayer = Math.abs(x - center) + Math.abs(y - center);
        
        if (distanceToPlayer > 2 && field[y][x].type === 'EMPTY') {
          field[y][x] = { ...CELL_TYPES[type] };
          placedCount++;
        }
        attempts++;
      }
    };

    placeSpawners(difficulty.spawnerCount);
    placeGuaranteedObject('HEAL_SMALL', 2);
    placeGuaranteedObject('HEAL_LARGE', 1);
    placeGuaranteedObject('TREASURE_MEDIUM', 2);
    placeGuaranteedObject('TREASURE_LARGE', 1);

    console.log(`🎉 Адаптивное поле ${currentFieldSize}x${currentFieldSize} создано!`);
    return field;
  };

  // Спавн монстров из спавнеров
  const spawnMonsters = useCallback(() => {
    if (gameState !== 'PLAYING') return;

    setGameField(prevField => {
      const newField = prevField.map(row => [...row]);
      const newLog = [];
      let monstersSpawned = 0;

      for (let y = 0; y < fieldSize; y++) {
        for (let x = 0; x < fieldSize; x++) {
          if (newField[y][x].type === 'SPAWNER') {
            if (currentTurn % 2 === 0) {
              const directions = [
                { dx: 1, dy: 0 }, { dx: -1, dy: 0 }, 
                { dx: 0, dy: 1 }, { dx: 0, dy: -1 }
              ];

              for (const { dx, dy } of directions) {
                const newX = x + dx;
                const newY = y + dy;
                
                if (newX >= 0 && newX < fieldSize && newY >= 0 && newY < fieldSize && 
                    newField[newY][newX].type === 'EMPTY' &&
                    Math.random() < 0.6) {
                  
                  const monsterTypes = ['ENEMY_WEAK', 'ENEMY_MEDIUM', 'ENEMY_ARCHER'];
                  const monsterType = monsterTypes[Math.floor(Math.random() * monsterTypes.length)];
                  
                  newField[newY][newX] = { ...CELL_TYPES[monsterType] };
                  monstersSpawned++;
                  
                  if (monstersSpawned >= 3) break;
                }
              }
            }
          }
        }
      }

      if (monstersSpawned > 0) {
        newLog.push(`⚡ Портал призвал ${monstersSpawned} монстров!`);
      }

      if (newLog.length > 0) {
        setGameLog(prev => [...prev.slice(-9), ...newLog]);
      }

      return newField;
    });
  }, [gameState, currentTurn, fieldSize]);

  // Движение врагов
  const moveEnemies = useCallback(() => {
    if (gameState !== 'PLAYING') return;

    setGameField(prevField => {
      const newField = prevField.map(row => [...row]);
      let newLog = [];
      let playerHit = false;

      // Проверка эффекта замедления
      const isEnemySlowed = activeEffects.some(effect => effect.type === 'slow');

      for (let y = 0; y < fieldSize; y++) {
        for (let x = 0; x < fieldSize; x++) {
          const cell = newField[y][x];
          if (cell.type.includes('ENEMY') || cell.type === 'BOSS') {
            const enemyData = CELL_TYPES[cell.type];

            // Дальнобойные атаки (работают всегда)
            if (enemyData.range) {
              const distanceToPlayer = Math.abs(x - playerPosition.x) + Math.abs(y - playerPosition.y);
              if (distanceToPlayer <= enemyData.range && distanceToPlayer > 1) {
                const damage = Math.max(1, enemyData.damage - playerStats.armor);
                const newHealth = Math.max(0, playerStats.health - damage);
                
                setPlayerStats(prev => ({
                  ...prev,
                  health: newHealth
                }));
                
                newLog.push(`🎯 ${enemyData.name} атаковал с расстояния! Урон: ${damage}`);
                setScreenShake(true);
                setTimeout(() => setScreenShake(false), 500);
                
                if (newHealth <= 0) {
                  setTimeout(() => endGame(playerStats.score, false), 100);
                }
                
                playerHit = true;
                continue;
              }
            }

            // Движение (может быть пропущено из-за замедления)
            if (isEnemySlowed && Math.random() < 0.5) {
              continue; // Пропускаем движение этого врага
            }

            const directions = [
              { dx: 1, dy: 0 }, { dx: -1, dy: 0 }, 
              { dx: 0, dy: 1 }, { dx: 0, dy: -1 }
            ].filter(({ dx, dy }) => {
              const newX = x + dx;
              const newY = y + dy;
              return newX >= 0 && newX < fieldSize && newY >= 0 && newY < fieldSize;
            });

            // Сортируем направления по близости к игроку
            directions.sort((a, b) => {
              const distA = Math.abs((x + a.dx) - playerPosition.x) + Math.abs((y + a.dy) - playerPosition.y);
              const distB = Math.abs((x + b.dx) - playerPosition.x) + Math.abs((y + b.dy) - playerPosition.y);
              return distA - distB;
            });

            let moved = false;
            for (const { dx, dy } of directions) {
              const newX = x + dx;
              const newY = y + dy;
              
              // Атака ближнего боя
              if (newX === playerPosition.x && newY === playerPosition.y) {
                const damage = Math.max(1, enemyData.damage - playerStats.armor);
                const newHealth = Math.max(0, playerStats.health - damage);
                
                setPlayerStats(prev => ({
                  ...prev,
                  health: newHealth
                }));
                
                newLog.push(`⚔️ ${enemyData.name} атаковал вблизи! Урон: ${damage}`);
                setScreenShake(true);
                setTimeout(() => setScreenShake(false), 500);
                
                if (newHealth <= 0) {
                  setTimeout(() => endGame(playerStats.score, false), 100);
                }
                
                playerHit = true;
                moved = true;
                break;
              }
              
              // Движение в пустую клетку
              if (newField[newY][newX].type === 'EMPTY') {
                newField[newY][newX] = { ...cell };
                newField[y][x] = { ...CELL_TYPES.EMPTY };
                moved = true;
                break;
              }
            }
          }
        }
      }

      if (playerHit && newLog.length > 0) {
        setGameLog(prev => [...prev.slice(-8), ...newLog.slice(-2)]);
      }

      return newField;
    });
  }, [gameState, playerPosition, fieldSize, activeEffects, playerStats]);

  // Обработка активных эффектов
  const processActiveEffects = () => {
    setActiveEffects(prev => {
      const newEffects = [];
      const newLog = [];
      
      prev.forEach(effect => {
        if (effect.duration > 1) {
          // Эффект ауры исцеления
          if (effect.type === 'healing_aura') {
            const healAmount = Math.floor(playerStats.maxHealth * 0.15);
            setPlayerStats(prevStats => ({
              ...prevStats,
              health: Math.min(prevStats.maxHealth, prevStats.health + healAmount)
            }));
            newLog.push(`💫 Аура исцеления: +${healAmount} здоровья`);
          }
          
          newEffects.push({ ...effect, duration: effect.duration - 1 });
        } else if (effect.duration === 1) {
          newLog.push(`🔚 Завершилось: ${getAbilityName(effect.abilityId)}`);
        }
      });
      
      if (newLog.length > 0) {
        setGameLog(prev => [...prev.slice(-8), ...newLog]);
      }
      
      return newEffects;
    });
    
    // Обновление перезарядки способностей
    setAbilityCooldowns(prev => {
      const newCooldowns = {};
      Object.keys(prev).forEach(abilityId => {
        if (prev[abilityId] > 1) {
          newCooldowns[abilityId] = prev[abilityId] - 1;
        }
      });
      return newCooldowns;
    });
  };

  // Получение имени способности по ID
  const getAbilityName = (abilityId) => {
    const abilities = {
      'time_slow': 'Замедление Времени',
      'double_strike': 'Двойной Удар',
      'healing_aura': 'Аура Исцеления'
    };
    return abilities[abilityId] || 'Способность';
  };

  // Ход врагов - вызывается после хода игрока
  const executeEnemyTurn = useCallback(() => {
    if (gameState !== 'PLAYING') return;
    
    console.log(`🎯 Ход врагов (ход ${currentTurn})`);
    
    // Обработка эффектов
    processActiveEffects();
    
    // Спавн монстров
    spawnMonsters();
    
    // Движение врагов
    moveEnemies();
    
    // Сбрасываем флаг ожидания хода врагов
    setEnemyMovePending(false);
  }, [gameState, currentTurn, processActiveEffects, spawnMonsters, moveEnemies]);

  // Эффект для выполнения хода врагов когда установлен флаг
  useEffect(() => {
    if (enemyMovePending && gameState === 'PLAYING') {
      const timer = setTimeout(() => {
        executeEnemyTurn();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [enemyMovePending, gameState, executeEnemyTurn]);

  // Обработчик использования способности
  const handleAbilityUse = (ability) => {
    const newCooldowns = { ...abilityCooldowns, [ability.id]: ability.cooldown };
    const newLog = [...gameLog];
    
    switch (ability.id) {
      case 'time_slow':
        setActiveEffects(prev => [...prev, {
          abilityId: ability.id,
          duration: ability.effect.slowDuration,
          type: 'slow'
        }]);
        newLog.push(`⏰ Время замедлено! Враги пропускают ходы ${ability.effect.slowDuration} раунда`);
        break;
        
      case 'double_strike':
        setActiveEffects(prev => [...prev, {
          abilityId: ability.id,
          duration: 1,
          type: 'double_damage'
        }]);
        newLog.push(`⚡ Следующая атака нанесет двойной урон!`);
        break;
        
      case 'healing_aura':
        setActiveEffects(prev => [...prev, {
          abilityId: ability.id,
          duration: ability.effect.duration,
          type: 'healing_aura'
        }]);
        // Немедленное исцеление при активации
        const immediateHeal = Math.floor(playerStats.maxHealth * 0.15);
        setPlayerStats(prev => ({
          ...prev,
          health: Math.min(prev.maxHealth, prev.health + immediateHeal)
        }));
        newLog.push(`💫 Аура исцеления! +${immediateHeal} здоровья сейчас и каждый ход`);
        break;
        
      default:
        break;
    }
    
    setAbilityCooldowns(newCooldowns);
    setGameLog(newLog.slice(-8));
  };

  const startGame = () => {
    console.log('🎮 Запускаем игру...');
    setIsLoading(true);
    
    try {
      const difficulty = DIFFICULTY_LEVELS[selectedDifficulty];
      const abilityBonuses = calculateAbilityBonuses();
      
      const newField = initializeGameField();
      
      if (!newField || !Array.isArray(newField)) {
        throw new Error('Некорректное игровое поле');
      }

      setGameField(newField);
      setPlayerStats({
        health: 100 + abilityBonuses.extraHealth,
        maxHealth: 100 + abilityBonuses.extraHealth,
        armor: abilityBonuses.armor,
        attack: 10 + abilityBonuses.attack,
        turnsLeft: difficulty.turns,
        totalTurns: difficulty.turns,
        score: 0,
        inventory: [],
        kills: 0,
        level: 1
      });
      setCurrentTurn(0);
      setCombo(0);
      setActiveEffects([]);
      setAbilityCooldowns({});
      setEnemyMovePending(false);
      setGameLog([
        `🎮 Начало приключения!`,
        `🎯 Сложность: ${difficulty.name}`,
        abilityBonuses.attack > 0 && `⚔️ Бонус атаки: +${abilityBonuses.attack}`,
        abilityBonuses.armor > 0 && `🛡️ Бонус брони: +${abilityBonuses.armor}`,
        abilityBonuses.extraHealth > 0 && `❤️ Доп. здоровье: +${abilityBonuses.extraHealth}`,
        `⏱️ Выживи ${difficulty.turns} ходов`,
        `💰 Награда: ${difficulty.reward} монет`,
        `📱 Поле: ${fieldSize}x${fieldSize} клеток`,
        `🚶 Вы в центре поля...`
      ].filter(Boolean));
      setSelectedCell(null);
      
      setTimeout(() => {
        setGameState('PLAYING');
        setIsLoading(false);
      }, 800);
      
    } catch (error) {
      console.error('❌ ОШИБКА при запуске игры:', error);
      setGameLog(['❌ Ошибка при создании игрового поля']);
      setIsLoading(false);
    }
  };

  const handleCellClick = (x, y) => {
    if (gameState !== 'PLAYING') return;
    if (playerStats.turnsLeft <= 0) return;
    if (enemyMovePending) return; // Не позволяем ходить пока враги не походили

    const distance = Math.abs(playerPosition.x - x) + Math.abs(playerPosition.y - y);
    if (distance !== 1) {
      setSelectedCell({ x, y, type: gameField[y][x].type });
      return;
    }

    const cellType = gameField[y][x].type;
    const newField = gameField.map(row => [...row]);
    const newLog = [...gameLog];
    let newPlayerStats = { ...playerStats };
    let gameOver = false;
    let teleport = false;
    let comboPoints = 0;

    if (cellType === 'WALL') {
      newLog.push(`🧱 Здесь стена! Нельзя пройти.`);
      setGameLog(prev => [...prev.slice(-9), ...newLog.slice(-1)]);
      return;
    }

    newField[playerPosition.y][playerPosition.x] = { ...CELL_TYPES.EMPTY };
    
    const cellData = CELL_TYPES[cellType];
    
    switch (cellType) {
      case 'TREASURE_SMALL':
      case 'TREASURE_MEDIUM':
      case 'TREASURE_LARGE':
        comboPoints = cellData.points * (1 + combo * 0.1);
        newPlayerStats.score += comboPoints;
        newLog.push(`💰 ${cellData.name}! +${Math.floor(comboPoints)} очков ${combo > 0 ? `(комбо x${combo + 1})` : ''}`);
        setCombo(prev => prev + 1);
        break;

      case 'ENEMY_WEAK':
      case 'ENEMY_MEDIUM':
      case 'ENEMY_STRONG':
      case 'ENEMY_ARCHER':
      case 'ENEMY_MAGE':
        let finalDamage = Math.max(1, cellData.damage - newPlayerStats.armor);
        
        const hasDoubleStrike = activeEffects.some(effect => effect.type === 'double_damage');
        if (hasDoubleStrike) {
          finalDamage *= 2;
          newLog.push(`⚡ Двойной удар! Урон удвоен`);
          setActiveEffects(prev => prev.filter(effect => effect.type !== 'double_damage'));
        }
        
        newPlayerStats.health = Math.max(0, newPlayerStats.health - finalDamage);
        newPlayerStats.kills += 1;
        comboPoints = 10 * (1 + combo * 0.2);
        newPlayerStats.score += comboPoints;
        newLog.push(`⚔️ Победа над ${cellData.name}! Урон: ${finalDamage} +${Math.floor(comboPoints)} очков ${combo > 0 ? `(комбо x${combo + 1})` : ''}`);
        setCombo(prev => prev + 1);
        setScreenShake(true);
        setTimeout(() => setScreenShake(false), 300);
        if (newPlayerStats.health <= 0) gameOver = true;
        break;

      case 'TRAP_VISIBLE':
        const trapDamage = Math.max(1, cellData.damage - newPlayerStats.armor);
        newPlayerStats.health = Math.max(0, newPlayerStats.health - trapDamage);
        newLog.push(`⚠️ ${cellData.name}! Урон: ${trapDamage}`);
        setCombo(0);
        if (newPlayerStats.health <= 0) gameOver = true;
        break;

      case 'TRAP_HIDDEN':
        const hiddenTrapDamage = Math.max(1, cellData.damage - newPlayerStats.armor);
        newPlayerStats.health = Math.max(0, newPlayerStats.health - hiddenTrapDamage);
        newField[y][x] = { ...CELL_TYPES.TRAP_VISIBLE };
        newLog.push(`💥 Скрытая ловушка! Урон: ${hiddenTrapDamage}`);
        setCombo(0);
        setScreenShake(true);
        setTimeout(() => setScreenShake(false), 500);
        if (newPlayerStats.health <= 0) gameOver = true;
        break;

      case 'HEAL_SMALL':
      case 'HEAL_LARGE':
        newPlayerStats.health = Math.min(newPlayerStats.maxHealth, newPlayerStats.health + cellData.heal);
        newLog.push(`❤️ ${cellData.name}! Здоровье +${cellData.heal}`);
        setCombo(prev => prev + 1);
        break;

      case 'BOSS':
        const bossDamage = Math.max(5, cellData.damage - newPlayerStats.armor);
        newPlayerStats.health = Math.max(0, newPlayerStats.health - bossDamage);
        if (newPlayerStats.health <= 0) {
          newLog.push(`🐉 ${cellData.name} победил вас...`);
          gameOver = true;
        } else {
          comboPoints = cellData.points * (1 + combo * 0.3);
          newPlayerStats.score += comboPoints;
          newPlayerStats.kills += 1;
          newLog.push(`🎊 ${cellData.name} повержен! +${Math.floor(comboPoints)} очков ${combo > 0 ? `(комбо x${combo + 1})` : ''}`);
          setCombo(prev => prev + 3);
          setScreenShake(true);
          setTimeout(() => setScreenShake(false), 800);
        }
        break;

      case 'QUEST':
        comboPoints = cellData.points * (1 + combo * 0.2);
        newPlayerStats.score += comboPoints;
        newLog.push(`📜 ${cellData.name}! +${Math.floor(comboPoints)} очков ${combo > 0 ? `(комбо x${combo + 1})` : ''}`);
        setCombo(prev => prev + 2);
        break;

      case 'PORTAL':
        teleport = true;
        newLog.push(`🌀 ${cellData.name}! Телепортация...`);
        setCombo(0);
        break;

      case 'ARMOR':
        newPlayerStats.armor += cellData.armor;
        newLog.push(`🛡️ ${cellData.name}! Защита +${cellData.armor}`);
        setCombo(prev => prev + 1);
        break;

      case 'WEAPON':
        newPlayerStats.attack += cellData.attack;
        newLog.push(`⚔️ ${cellData.name}! Атака +${cellData.attack}`);
        setCombo(prev => prev + 1);
        break;

      case 'SPAWNER':
        newLog.push(`⚡ Уничтожен портал монстров!`);
        setCombo(prev => prev + 2);
        break;

      default:
        newLog.push(`🚶 Перемещение`);
        setCombo(0);
    }

    if (teleport) {
      let newX, newY;
      let attempts = 0;
      do {
        newX = Math.floor(Math.random() * fieldSize);
        newY = Math.floor(Math.random() * fieldSize);
        attempts++;
      } while (
        (newField[newY][newX].type !== 'EMPTY') && 
        attempts < 100
      );
      
      newField[newY][newX] = { ...CELL_TYPES.PLAYER };
      setPlayerPosition({ x: newX, y: newY });
    } else {
      newField[y][x] = { ...CELL_TYPES.PLAYER };
      setPlayerPosition({ x, y });
    }

    newPlayerStats.turnsLeft -= 1;
    setCurrentTurn(prev => prev + 1);
    setGameField(newField);
    setPlayerStats(newPlayerStats);
    setGameLog(newLog.slice(-8));
    setSelectedCell(null);

    // Устанавливаем флаг для хода врагов после хода игрока
    setEnemyMovePending(true);

    if (gameOver || newPlayerStats.turnsLeft <= 0) {
      setTimeout(() => {
        endGame(newPlayerStats.score, !gameOver && newPlayerStats.health > 0);
      }, 500);
    }
  };

  const endGame = (finalScore, survived) => {
    const difficulty = DIFFICULTY_LEVELS[selectedDifficulty];
    let coinsEarned = 0;

    if (survived) {
      coinsEarned = difficulty.reward + 
                   Math.floor(finalScore / 2) + 
                   (playerStats.kills * 20) +
                   (combo * 10);
    } else {
      const progress = currentTurn / difficulty.turns;
      coinsEarned = Math.floor(difficulty.reward * progress * 0.3);
    }

    const newCoins = coins + coinsEarned;
    setCoins(newCoins);
    localStorage.setItem('hypeDragon_coins', newCoins.toString());
    
    setGameLog(prev => [
      ...prev.slice(-6),
      survived ? '🎉 Победа!' : '💀 Вы пали в бою...',
      `💰 Получено монет: ${coinsEarned}`,
      `⭐ Итоговый счет: ${finalScore}`,
      `👹 Убито врагов: ${playerStats.kills}`,
      combo > 0 ? `🔥 Максимальное комбо: x${combo + 1}` : ''
    ].filter(Boolean));
    
    setGameState('FINISHED');
  };

  const renderCell = (cell, x, y) => {
    if (!cell || !cell.type) {
      return (
        <div 
          className="cell empty"
          key={`${x}-${y}`}
        >
          {' '}
        </div>
      );
    }

    const isRevealed = 
      Math.abs(x - playerPosition.x) <= 3 && 
      Math.abs(y - playerPosition.y) <= 3;

    if (!isRevealed && gameState === 'PLAYING') {
      return (
        <div 
          className="cell hidden"
          key={`${x}-${y}`}
          onClick={() => setSelectedCell({ x, y, type: 'HIDDEN' })}
        >
          {' '}
        </div>
      );
    }

    const isSelected = selectedCell && selectedCell.x === x && selectedCell.y === y;
    const cellType = cell.type || 'EMPTY';
    
    const displayType = cellType === 'TRAP_HIDDEN' ? 'EMPTY' : cellType;
    const cellData = CELL_TYPES[displayType] || CELL_TYPES.EMPTY;

    return (
      <div 
        className={`cell ${displayType.toLowerCase()} ${x === playerPosition.x && y === playerPosition.y ? 'player' : ''} ${isSelected ? 'selected' : ''}`}
        key={`${x}-${y}`}
        onClick={() => !enemyMovePending && handleCellClick(x, y)}
        title={cellType === 'TRAP_HIDDEN' ? 'Неизвестно' : cellData.description}
      >
        {cellData.icon}
        {isSelected && gameState === 'PLAYING' && (
          <div className="cell-tooltip">
            {cellType === 'TRAP_HIDDEN' ? '❓ Неизвестно' : cellData.description}
          </div>
        )}
      </div>
    );
  };

  const resetGame = () => {
    setGameState('MENU');
    setGameLog([]);
    setSelectedCell(null);
    setScreenShake(false);
    setCombo(0);
    setActiveEffects([]);
    setAbilityCooldowns({});
    setEnemyMovePending(false);
    if (comboTimer) {
      clearTimeout(comboTimer);
    }
  };

  // Получение активных способностей для отображения
  const getActiveAbilitiesForBattle = () => {
    return Object.values(playerAbilities).filter(ability => 
      ability.level > 0 && ability.type === 'active'
    );
  };

  return (
    <div className={`battle-page ${screenShake ? 'screen-shake' : ''}`}>
      <div className="battle-container">
        <header className="battle-header">
          <div className="header-content">
            <h1 className="battle-title">🎮 Адаптивная Арена</h1>
            <p className="battle-subtitle">
              Идеально для мобильных! Поле {fieldSize}x{fieldSize} клеток
            </p>
          </div>
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

        <div className="battle-main">
          {isLoading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
              <p>Создаем поле {fieldSize}x{fieldSize}...</p>
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          {gameState === 'MENU' && !isLoading && (
            <div className="game-menu">
              <h3>🎯 Выберите уровень сложности:</h3>
              <div className="difficulty-selector">
                {DIFFICULTY_LEVELS.map((level, index) => (
                  <div 
                    key={index}
                    className={`difficulty-option ${selectedDifficulty === index ? 'selected' : ''}`}
                    onClick={() => setSelectedDifficulty(index)}
                  >
                    <div className="difficulty-name">{level.name}</div>
                    <div className="difficulty-stats">
                      ⏱️ {level.turns} ходов | 🎯 {level.fieldSize}x{level.fieldSize}
                    </div>
                    <div className="difficulty-desc">{level.description}</div>
                  </div>
                ))}
              </div>
              
              <div className="device-info">
                <span>📱 Размер поля: {fieldSize}x{fieldSize} (адаптивно)</span>
              </div>
              
              <button 
                className="start-button" 
                onClick={startGame}
                disabled={isLoading}
              >
                <span className="button-icon">🎮</span>
                {isLoading ? 'Загрузка...' : 'Начать Игру'}
              </button>

              <div className="game-rules">
                <h3>📱 ОПТИМИЗИРОВАНО ДЛЯ ТЕЛЕФОНОВ:</h3>
                <div className="rules-grid">
                  <div className="rule-item">
                    <span className="rule-icon">📏</span>
                    <span className="rule-text">Авто-размер поля</span>
                  </div>
                  <div className="rule-item">
                    <span className="rule-icon">👆</span>
                    <span className="rule-text">Большие клетки для тапов</span>
                  </div>
                  <div className="rule-item">
                    <span className="rule-icon">📱</span>
                    <span className="rule-text">Идеально на мобильных</span>
                  </div>
                  <div className="rule-item">
                    <span className="rule-icon">🖥️</span>
                    <span className="rule-text">Также на компьютере</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {gameState === 'PLAYING' && !isLoading && gameField.length > 0 && (
            <div className="strategy-game">
              {/* Панель способностей */}
              {getActiveAbilitiesForBattle().length > 0 && (
                <div className="abilities-panel">
                  <h4>✨ Активные способности:</h4>
                  <div className="abilities-list">
                    {getActiveAbilitiesForBattle().map(ability => (
                      <AbilityButton 
                        key={ability.id}
                        ability={ability}
                        cooldowns={abilityCooldowns}
                        activeEffects={activeEffects}
                        onUse={handleAbilityUse}
                      />
                    ))}
                  </div>
                </div>
              )}

              <div className="game-info-panel">
                <div className="player-stats">
                  <div className="stat">❤️ {Math.max(0, playerStats.health)}/{playerStats.maxHealth}</div>
                  <div className="stat">🛡️ {playerStats.armor}</div>
                  <div className="stat">⚔️ {playerStats.attack}</div>
                  <div className="stat">⭐ {playerStats.score}</div>
                  <div className="stat">👹 {playerStats.kills}</div>
                  <div className="stat">⏱️ {playerStats.turnsLeft}</div>
                  {combo > 0 && (
                    <div className="stat combo">🔥 x{combo + 1}</div>
                  )}
                </div>
                <button className="cancel-button" onClick={resetGame}>
                  ❌ Выйти
                </button>
              </div>

              <div className="field-size-info">
                Поле: {fieldSize}x{fieldSize} | Ход: {currentTurn}
                {enemyMovePending && ' | ⏳ Враги ходят...'}
                {activeEffects.some(effect => effect.type === 'slow') && ' | ⏰ Замедление!'}
                {activeEffects.some(effect => effect.type === 'healing_aura') && ' | 💫 Исцеление!'}
              </div>

              <div className="game-field-container">
                <div className="game-field-strategy adaptive-field">
                  {gameField.map((row, y) => (
                    <div key={y} className="field-row">
                      {row.map((cell, x) => renderCell(cell, x, y))}
                    </div>
                  ))}
                </div>
              </div>

              <div className="game-log">
                <h4>📜 Журнал:</h4>
                <div className="log-entries">
                  {gameLog.map((log, index) => (
                    <div key={index} className="log-entry">{log}</div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {gameState === 'FINISHED' && (
            <div className="results-modal">
              <div className="modal-content">
                <h2>{playerStats.health > 0 ? '🎉 Победа!' : '💀 Поражение'}</h2>
                
                <div className="results-stats">
                  <div className="result-item">
                    <span className="result-label">Прожито ходов:</span>
                    <span className="result-value">{currentTurn}/{DIFFICULTY_LEVELS[selectedDifficulty].turns}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Набрано очков:</span>
                    <span className="result-value">{playerStats.score}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Убито врагов:</span>
                    <span className="result-value">{playerStats.kills}</span>
                  </div>
                  <div className="result-item">
                    <span className="result-label">Финальное здоровье:</span>
                    <span className="result-value">{Math.max(0, playerStats.health)}</span>
                  </div>
                  {combo > 0 && (
                    <div className="result-item">
                      <span className="result-label">Максимальное комbo:</span>
                      <span className="result-value">x{combo + 1}</span>
                    </div>
                  )}
                  <div className="result-item">
                    <span className="result-label">Получено монет:</span>
                    <span className="result-value reward">
                      {Math.floor(DIFFICULTY_LEVELS[selectedDifficulty].reward * (playerStats.health > 0 ? 1 : (currentTurn / DIFFICULTY_LEVELS[selectedDifficulty].turns * 0.3)) + playerStats.kills * 20 + combo * 10)}
                    </span>
                  </div>
                </div>

                <button className="play-again-button" onClick={resetGame}>
                  <span className="button-icon">🔄</span>
                  Играть Снова
                </button>
              </div>
            </div>
          )}
        </div>

        <footer className="battle-footer">
          <p>✨ Адаптивное поле | Идеально для телефонов | Авто-размер клеток ✨</p>
        </footer>
      </div>
    </div>
  );
};

export default BattlePage;