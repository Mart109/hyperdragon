package com.example.hyperDragon.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class GameSession {
    private String matchId;
    private Long player1Id;
    private Long player2Id;
    private String player1Name;
    private String player2Name;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private Integer player1Score = 0;
    private Integer player2Score = 0;
    private GameStatus status;
    private Long winnerId;
    private Integer coinsReward;
}