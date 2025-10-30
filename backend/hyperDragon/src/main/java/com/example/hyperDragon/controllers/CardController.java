package com.example.hyperDragon.controllers;

import com.example.hyperDragon.dto.CardResponse;
import com.example.hyperDragon.service.CardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cards")
public class CardController {

    @Autowired
    private CardService cardService;

    // Получить доступные для покупки карточки (возвращает DTO)
    @GetMapping("/available")
    public ResponseEntity<List<CardResponse>> getAvailableCards() {
        List<CardResponse> cards = cardService.getAvailableCards();
        return ResponseEntity.ok(cards);
    }

    // Получить карточки пользователя (возвращает DTO)
    @GetMapping("/my-cards")
    public ResponseEntity<List<CardResponse>> getUserCards(@RequestHeader("X-User-Id") Long userId) {
        List<CardResponse> cards = cardService.getUserCards(userId);
        return ResponseEntity.ok(cards);
    }

    // Купить карточку
    @PostMapping("/buy")
    public ResponseEntity<String> buyCard(@RequestHeader("X-User-Id") Long userId,
                                          @RequestParam String cardName) {
        String result = cardService.buyCard(userId, cardName);
        return ResponseEntity.ok(result);
    }

    // Улучшить карточку
    @PostMapping("/upgrade")
    public ResponseEntity<String> upgradeCard(@RequestHeader("X-User-Id") Long userId,
                                              @RequestParam Long cardId) {
        String result = cardService.upgradeCard(userId, cardId);
        return ResponseEntity.ok(result);
    }

    // Собрать пассивный доход
    @PostMapping("/collect-income")
    public ResponseEntity<String> collectPassiveIncome(@RequestHeader("X-User-Id") Long userId) {
        int income = cardService.collectPassiveIncome(userId);
        if (income > 0) {
            return ResponseEntity.ok("Собрано пассивного дохода: " + income + " монет!");
        } else {
            return ResponseEntity.ok("Доход еще не накопился");
        }
    }
}