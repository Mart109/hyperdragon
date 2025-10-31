import React, { useState } from 'react'
import './ProfilePage.css'

const ProfilePage = () => {
  const [userData, setUserData] = useState({
    username: 'DragonMaster',
    level: 0,
    gold: 0,
  })

  const [copied, setCopied] = useState(false)
  const referralLink =
    '/api/referral/register?username={name}&referralCode={code}'

  const copyReferralLink = () => {
    navigator.clipboard.writeText(referralLink)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        {/* Заголовок профиля */}
        <header className="profile-header">
          <div className="header-content">
            <h1 className="profile-title">Профиль</h1>
            <p className="profile-subtitle">Основная информация</p>
          </div>
        </header>

        {/* Основная информация */}
        <div className="profile-main">
          <div className="profile-card main-info">
            <div className="profile-avatar">🐉</div>
            <h2 className="player-name">{userData.username}</h2>
            <div className="player-level">Уровень {userData.level}</div>

            <div className="player-resources">
              <div className="resource-item">
                <div className="resource-icon gold">💰</div>
                <div className="resource-info">
                  <div className="resource-value">
                    {userData.gold.toLocaleString()}
                  </div>
                  <div className="resource-label">Золото</div>
                </div>
              </div>
            </div>
          </div>

          {/* Реферальная ссылка */}
          <div className="profile-card referral-card">
            <div className="section-header">
              <span className="section-icon">👥</span>
              <h3>Пригласи друга</h3>
            </div>
            <p className="referral-text">
              Поделись ссылкой и получай бонусы за приглашенных друзей!
            </p>
            <div className="referral-link-container">
              <input
                type="text"
                value={referralLink}
                readOnly
                className="referral-input"
              />
              <button
                className={`copy-btn ${copied ? 'copied' : ''}`}
                onClick={copyReferralLink}
              >
                {copied ? '✓' : 'Копировать'}
              </button>
            </div>
            {copied && <div className="copy-message">Ссылка скопирована!</div>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
