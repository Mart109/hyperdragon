package com.example.hyperDragon.dto;

import lombok.Data;

@Data
public class CardResponse {
    private Long id;
    private String name;
    private String displayName;
    private String description;
    private Integer level;
    private Integer baseIncome;
    private Integer upgradeCost;
    private Integer incomePerLevel;
    private Boolean isAvailable;
    private Integer nextUpgradeCost;
    private Integer currentIncome;
    private Long ownerId;
    private String ownerUsername;
}