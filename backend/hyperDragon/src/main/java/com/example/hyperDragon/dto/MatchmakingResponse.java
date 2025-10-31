package com.example.hyperDragon.dto;

import lombok.Data;

@Data
public class MatchmakingResponse {
    private String matchId;
    private String status; // SEARCHING, FOUND, CANCELLED
    private Long opponentId;
    private String opponentName;
    private Integer countdownSeconds;

    // Конструктор по умолчанию
    public MatchmakingResponse() {}

    // Конструктор с параметрами (убедитесь что он правильный)
    public MatchmakingResponse(String matchId, String status, Long opponentId, String opponentName, Integer countdownSeconds) {
        this.matchId = matchId;
        this.status = status;
        this.opponentId = opponentId;
        this.opponentName = opponentName;
        this.countdownSeconds = countdownSeconds;
    }
}