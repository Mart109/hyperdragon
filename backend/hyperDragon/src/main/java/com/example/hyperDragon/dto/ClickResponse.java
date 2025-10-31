package com.example.hyperDragon.dto;

import lombok.Data;

@Data
public class ClickResponse {
    private String username;
    private Integer coins;
    private Integer level;
    private Long userId;
    private Integer energy;
    private Integer maxEnergy;
    private String message;

    public ClickResponse() {}

    public ClickResponse(String username, Integer coins, Integer level, Long userId,
                         Integer energy, Integer maxEnergy, String message) {
        this.username = username;
        this.coins = coins;
        this.level = level;
        this.userId = userId;
        this.energy = energy;
        this.maxEnergy = maxEnergy;
        this.message = message;
    }
}