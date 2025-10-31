package com.example.hyperDragon.controllers;

import com.example.hyperDragon.dto.GameSession;
import com.example.hyperDragon.dto.MatchmakingResponse;
import com.example.hyperDragon.service.MatchmakingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/multiplayer")
public class MultiplayerGameController {

    @Autowired
    private MatchmakingService matchmakingService;

    // Начать поиск противника
    @PostMapping("/find-match")
    public ResponseEntity<MatchmakingResponse> findMatch(@RequestHeader("X-User-Id") Long userId) {
        try {
            MatchmakingResponse response = matchmakingService.findOpponent(userId);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // Получить статус матча
    @GetMapping("/match-status/{matchId}")
    public ResponseEntity<GameSession> getMatchStatus(@PathVariable String matchId) {
        GameSession game = matchmakingService.getGameSession(matchId);
        if (game == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(game);
    }

    // Обновить счет игрока (фронтенд отправляет каждые N секунд)
    @PostMapping("/update-score")
    public ResponseEntity<?> updateScore(
            @RequestHeader("X-User-Id") Long userId,
            @RequestParam String matchId,
            @RequestParam Integer score) {
        try {
            matchmakingService.updatePlayerScore(matchId, userId, score);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // Завершить игру
    @PostMapping("/finish-game/{matchId}")
    public ResponseEntity<GameSession> finishGame(@PathVariable String matchId) {
        try {
            GameSession result = matchmakingService.finishGame(matchId);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // Отменить поиск
    @PostMapping("/cancel-search")
    public ResponseEntity<?> cancelSearch(@RequestHeader("X-User-Id") Long userId) {
        matchmakingService.cancelMatchmaking(userId);
        return ResponseEntity.ok().build();
    }

    // Получить все активные игры (для отладки)
    @GetMapping("/active-games")
    public ResponseEntity<Map<String, GameSession>> getActiveGames() {
        Map<String, GameSession> games = matchmakingService.getActiveGames();
        return ResponseEntity.ok(games);
    }
}