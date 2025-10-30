package com.example.hyperDragon.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class UserProfileResponse {
    private Long userId;
    private String username;
    private Integer coins;
    private Integer level;
    private Integer experience;
    private Integer energy;
    private Integer maxEnergy;
    private LocalDateTime lastEnergyUpdate;
    private LocalDateTime lastPassiveIncome;

    // Карточки
    private Integer cardsCount;
    private Integer totalPassiveIncome;

    // Реферальная система
    private String referralCode;
    private Integer referralsCount;
    private Integer referralBonus;
    private Boolean referralBonusClaimed;

    // Статистика
    private Integer totalClicks;
    private LocalDateTime registeredAt;

    public UserProfileResponse() {}
}