package com.example.hyperDragon.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Data
@Entity
@Table(name = "users")
public class Users {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(name = "coins")
    private Integer coins = 0;

    @Column(name = "level")
    private Integer level = 1;

    @Column(name = "energy")
    private Integer energy = 500;

    @Column(name = "max_energy")
    private Integer maxEnergy = 500;

    @Column(name = "last_energy_update")
    private LocalDateTime lastEnergyUpdate;

    @Column(name = "last_passive_income")
    private LocalDateTime lastPassiveIncome;

    // Реферальная система
    @Column(name = "referral_code", unique = true)
    private String referralCode;

    @Column(name = "referrer_id")
    private Long referrerId;

    @Column(name = "referrals_count")
    private Integer referralsCount = 0;

    @Column(name = "referral_bonus_claimed")
    private Boolean referralBonusClaimed = false;

    @OneToMany(mappedBy = "owner", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Card> cards = new ArrayList<>();

    public Users() {}

    public Users(String username) {
        this.username = username;
        this.coins = 0;
        this.level = 1;
        this.energy = 500;
        this.maxEnergy = 500;
        this.lastEnergyUpdate = LocalDateTime.now();
        this.lastPassiveIncome = LocalDateTime.now();
        this.referralCode = generateReferralCode();
        this.referralsCount = 0;
        this.referralBonusClaimed = false;
    }

    // Генерация уникального реферального кода
    private String generateReferralCode() {
        return UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }

    // Метод для добавления реферала
    public void addReferral() {
        this.referralsCount++;
    }

    // Метод для получения реферального бонуса
    public void claimReferralBonus() {
        this.coins += 10000; // Бонус за реферала
        this.referralBonusClaimed = true;
    }
}