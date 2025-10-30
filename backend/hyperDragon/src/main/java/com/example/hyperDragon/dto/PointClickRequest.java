package com.example.hyperDragon.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class PointClickRequest {
    private String sessionId;
    private Integer pointX;
    private Integer pointY;
    private LocalDateTime clickTime;
}