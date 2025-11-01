# 🐉 HyperDragon API Documentation


[![My Skills](https://skillicons.dev/icons?i=spring,react)](https://skillicons.dev)

## 🎯 Base URL
```
http://localhost:8080
```

---

## 👤 **Clicker System**

### Create User
- **Method:** `POST`
- **Endpoint:** `/api/clicker/create-user?username={name}`
- **Description:** Создать нового пользователя
- **Headers:** None
- **Parameters:** 
  - `username` (required) - имя пользователя

### Click Action
- **Method:** `POST`
- **Endpoint:** `/api/clicker/click-by-id`
- **Description:** Сделать клик (заработать монеты)
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Restore Energy
- **Method:** `POST`
- **Endpoint:** `/api/clicker/restore-energy`
- **Description:** Восстановить энергию
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Get User Info
- **Method:** `GET`
- **Endpoint:** `/api/clicker/user-info`
- **Description:** Получить информацию о пользователе
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Get All Users
- **Method:** `GET`
- **Endpoint:** `/api/clicker/all-users`
- **Description:** Получить список всех пользователей
- **Headers:** None
- **Parameters:** None

---

## 🃏 **Card System**

### Get Available Cards
- **Method:** `GET`
- **Endpoint:** `/api/cards/available`
- **Description:** Получить доступные для покупки карточки
- **Headers:** None
- **Parameters:** None

### Get User Cards
- **Method:** `GET`
- **Endpoint:** `/api/cards/my-cards`
- **Description:** Получить карточки пользователя
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Buy Card
- **Method:** `POST`
- **Endpoint:** `/api/cards/buy?cardName={name}`
- **Description:** Купить карточку
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** 
  - `cardName` - название карточки

### Upgrade Card
- **Method:** `POST`
- **Endpoint:** `/api/cards/upgrade?cardId={id}`
- **Description:** Улучшить карточку
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** 
  - `cardId` - ID карточки

### Collect Income
- **Method:** `POST`
- **Endpoint:** `/api/cards/collect-income`
- **Description:** Собрать пассивный доход
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

---

## 🤝 **Referral System**

### Get Referral Info
- **Method:** `GET`
- **Endpoint:** `/api/referral/info`
- **Description:** Получить реферальную информацию
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Claim Bonus
- **Method:** `POST`
- **Endpoint:** `/api/referral/claim-bonus`
- **Description:** Получить бонус за рефералов
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Register with Referral
- **Method:** `POST`
- **Endpoint:** `/api/referral/register?username={name}&referralCode={code}`
- **Description:** Регистрация с реферальным кодом
- **Headers:** None
- **Parameters:** 
  - `username` (required) - имя пользователя
  - `referralCode` (optional) - реферальный код

---

## 👤 **Profile System**

### Get Full Profile
- **Method:** `GET`
- **Endpoint:** `/api/profile`
- **Description:** Полная информация о пользователе
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Get Short Profile
- **Method:** `GET`
- **Endpoint:** `/api/profile/short`
- **Description:** Краткая информация о пользователе
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

---

## 🎮 **Multiplayer Game System**

### Find Match
- **Method:** `POST`
- **Endpoint:** `/api/multiplayer/find-match`
- **Description:** Найти противника для мини-игры
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Get Match Status
- **Method:** `GET`
- **Endpoint:** `/api/multiplayer/match-status/{matchId}`
- **Description:** Статус матча
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Update Score
- **Method:** `POST`
- **Endpoint:** `/api/multiplayer/update-score?matchId={id}&score={points}`
- **Description:** Обновить счет в мини-игре
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** 
  - `matchId` - ID матча
  - `score` - количество очков

### Finish Game
- **Method:** `POST`
- **Endpoint:** `/api/multiplayer/finish-game/{matchId}`
- **Description:** Завершить мини-игру
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Cancel Search
- **Method:** `POST`
- **Endpoint:** `/api/multiplayer/cancel-search`
- **Description:** Отменить поиск матча
- **Headers:** `X-User-Id: {userId}`
- **Parameters:** None

### Get Active Games (Debug)
- **Method:** `GET`
- **Endpoint:** `/api/multiplayer/active-games`
- **Description:** Все активные игры (для отладки)
- **Headers:** None
- **Parameters:** None

---

## 📋 **Game Flow Example**

### 1. Start Game
```bash
# Create user
POST /api/clicker/create-user?username=DragonPlayer

# Earn coins
POST /api/clicker/click-by-id
Headers: X-User-Id: 1

# Buy cards
POST /api/cards/buy?cardName=golden_dragon
Headers: X-User-Id: 1
```

### 2. Multiplayer Game
```bash
# Find opponent
POST /api/multiplayer/find-match
Headers: X-User-Id: 1

# Update score during game
POST /api/multiplayer/update-score?matchId=abc-123&score=25
Headers: X-User-Id: 1

# Finish game
POST /api/multiplayer/finish-game/abc-123
Headers: X-User-Id: 1
```

### 3. Referral System
```bash
# Get referral info
GET /api/referral/info
Headers: X-User-Id: 1

# Claim bonus
POST /api/referral/claim-bonus
Headers: X-User-Id: 1
```

---

## 🏆 **Rewards System**
- **Click:** +1 coin per click
- **Multiplayer Win:** +350 coins
- **Multiplayer Loss:** -100 coins  
- **Referral Bonus:** +10,000 coins per referral
- **Card Income:** Passive income based on card level

## ⚡ **Energy System**
- Start: 500 energy
- Click cost: 1 energy
- Restore: Full restore over time

---

*Last Updated: 2025-10-30*
