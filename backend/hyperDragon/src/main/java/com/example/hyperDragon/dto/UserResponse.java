package com.example.hyperDragon.dto;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
public class UserResponse {

    private Long id;
    private String username;
    private Integer coins;
    private Integer level;
    private Integer energy;
    private Integer maxEnergy;
    private LocalDateTime lastEnergyUpdate;
    private LocalDateTime lastPassiveIncome;
    private List<CardResponse> cards;

}
