package com.example.hyperDragon.service;

import com.example.hyperDragon.dto.GameSession;
import com.example.hyperDragon.dto.GameStatus;
import com.example.hyperDragon.dto.MatchmakingResponse;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.Optional;
import java.util.Queue;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;

@Service
public class MatchmakingService {

    private final Queue<Long> waitingPlayers = new ConcurrentLinkedQueue<>();
    private final Map<String, GameSession> activeGames = new ConcurrentHashMap<>();
    private static final int MATCH_TIMEOUT = 30; // 30 секунд поиска
    private static final int WIN_REWARD = 350;
    private static final int LOSS_PENALTY = -100;

    @Autowired
    private UserRepository userRepository;

    // Поиск противника
    public MatchmakingResponse findOpponent(Long userId) {
        // Проверяем, не ищет ли уже пользователь игру
        if (waitingPlayers.contains(userId)) {
            return new MatchmakingResponse(null, "SEARCHING", null, null, MATCH_TIMEOUT);
        }

        // Ищем противника в очереди
        if (!waitingPlayers.isEmpty() && !waitingPlayers.peek().equals(userId)) {
            Long opponentId = waitingPlayers.poll();
            return createMatch(userId, opponentId);
        }

        // Добавляем в очередь ожидания
        waitingPlayers.offer(userId);
        return new MatchmakingResponse(null, "SEARCHING", null, null, MATCH_TIMEOUT);
    }

    // Создание матча
    private MatchmakingResponse createMatch(Long player1Id, Long player2Id) {
        String matchId = UUID.randomUUID().toString();

        Optional<Users> player1Opt = userRepository.findById(player1Id);
        Optional<Users> player2Opt = userRepository.findById(player2Id);

        if (player1Opt.isEmpty() || player2Opt.isEmpty()) {
            throw new RuntimeException("Игрок не найден");
        }

        GameSession game = new GameSession();
        game.setMatchId(matchId);
        game.setPlayer1Id(player1Id);
        game.setPlayer2Id(player2Id);
        game.setPlayer1Name(player1Opt.get().getUsername());
        game.setPlayer2Name(player2Opt.get().getUsername());
        game.setStartTime(LocalDateTime.now().plusSeconds(5)); // Начало через 5 сек
        game.setEndTime(LocalDateTime.now().plusSeconds(65)); // 60 сек игра + 5 сек подготовка
        game.setPlayer1Score(0);
        game.setPlayer2Score(0);
        game.setStatus(GameStatus.WAITING);

        activeGames.put(matchId, game);

        // Уведомляем обоих игроков
        MatchmakingResponse response = new MatchmakingResponse();
        response.setMatchId(matchId);
        response.setStatus("FOUND");
        response.setOpponentId(player2Id);
        response.setOpponentName(player2Opt.get().getUsername());
        response.setCountdownSeconds(5);

        return response;
    }

    // Получить статус матча
    public GameSession getGameSession(String matchId) {
        return activeGames.get(matchId);
    }

    // Обновить счет игрока
    public void updatePlayerScore(String matchId, Long userId, Integer points) {
        GameSession game = activeGames.get(matchId);
        if (game == null) return;

        if (userId.equals(game.getPlayer1Id())) {
            game.setPlayer1Score(points);
        } else if (userId.equals(game.getPlayer2Id())) {
            game.setPlayer2Score(points);
        }
    }

    // Завершить игру и определить победителя
    @Transactional
    public GameSession finishGame(String matchId) {
        GameSession game = activeGames.get(matchId);
        if (game == null) {
            return null;
        }

        if (game.getStatus() == GameStatus.FINISHED) {
            return game;
        }

        game.setStatus(GameStatus.FINISHED);
        game.setEndTime(LocalDateTime.now());

        // Определяем победителя
        if (game.getPlayer1Score() > game.getPlayer2Score()) {
            game.setWinnerId(game.getPlayer1Id());
        } else if (game.getPlayer2Score() > game.getPlayer1Score()) {
            game.setWinnerId(game.getPlayer2Id());
        } else {
            // Ничья - случайный победитель
            game.setWinnerId(Math.random() > 0.5 ? game.getPlayer1Id() : game.getPlayer2Id());
        }

        // Награждаем победителя и наказываем проигравшего
        distributeRewards(game);

        return game;
    }

    private void distributeRewards(GameSession game) {
        Optional<Users> winnerOpt = userRepository.findById(game.getWinnerId());
        Long loserId = game.getWinnerId().equals(game.getPlayer1Id()) ?
                game.getPlayer2Id() : game.getPlayer1Id();
        Optional<Users> loserOpt = userRepository.findById(loserId);

        if (winnerOpt.isPresent() && loserOpt.isPresent()) {
            Users winner = winnerOpt.get();
            Users loser = loserOpt.get();

            // Проверяем, что у проигравшего достаточно монет
            if (loser.getCoins() >= 100) {
                winner.setCoins(winner.getCoins() + WIN_REWARD);
                loser.setCoins(loser.getCoins() + LOSS_PENALTY);

                userRepository.save(winner);
                userRepository.save(loser);

                game.setCoinsReward(WIN_REWARD);
            }
        }
    }

    // Отмена поиска
    public void cancelMatchmaking(Long userId) {
        waitingPlayers.remove(userId);
    }

    // Получить все активные игры (для админа)
    public Map<String, GameSession> getActiveGames() {
        return activeGames;
    }

    // Очистить устаревшие сессии
    public void cleanupExpiredSessions() {
        LocalDateTime now = LocalDateTime.now();
        activeGames.entrySet().removeIf(entry ->
                entry.getValue().getEndTime().isBefore(now) &&
                        entry.getValue().getStatus() != GameStatus.FINISHED
        );
    }
}