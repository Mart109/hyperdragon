package com.example.hyperDragon.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "mini_game_results")
public class MiniGameResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users user;

    @Column(name = "points_destroyed")
    private Integer pointsDestroyed;

    @Column(name = "coins_earned")
    private Integer coinsEarned;

    @Column(name = "won")
    private Boolean won;

    @Column(name = "play_date")
    private LocalDateTime playDate;

    public MiniGameResult() {
        this.playDate = LocalDateTime.now();
    }
}