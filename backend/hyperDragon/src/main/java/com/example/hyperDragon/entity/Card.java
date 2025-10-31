package com.example.hyperDragon.entity;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "cards")
public class Card {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false)
    private String displayName;

    @Column(nullable = false)
    private String description;

    @Column(nullable = false)
    private Integer level = 1;

    @Column(nullable = false)
    private Integer baseIncome;

    @Column(nullable = false)
    private Integer upgradeCost;

    @Column(nullable = false)
    private Integer incomePerLevel;

    @Column(nullable = false)
    private Boolean isAvailable = true;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users owner;

    public Card() {}

    public Card(String name, String displayName, String description, Integer baseIncome,
                Integer upgradeCost, Integer incomePerLevel) {
        this.name = name;
        this.displayName = displayName;
        this.description = description;
        this.baseIncome = baseIncome;
        this.upgradeCost = upgradeCost;
        this.incomePerLevel = incomePerLevel;
    }

    public Integer getCurrentIncome() {
        return baseIncome + (level - 1) * incomePerLevel;
    }

    public Integer getNextUpgradeCost() {
        return upgradeCost * level;
    }
}