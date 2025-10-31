package com.example.hyperDragon.controllers;

import com.example.hyperDragon.dto.ReferralResponse;
import com.example.hyperDragon.service.ReferralService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/referral")
public class ReferralController {

    @Autowired
    private ReferralService referralService;

    // Получить реферальную информацию
    @GetMapping("/info")
    public ResponseEntity<ReferralResponse> getReferralInfo(@RequestHeader("X-User-Id") Long userId) {
        ReferralResponse info = referralService.getReferralInfo(userId);
        if (info == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(info);
    }

    // Получить бонус за рефералов
    @PostMapping("/claim-bonus")
    public ResponseEntity<String> claimReferralBonus(@RequestHeader("X-User-Id") Long userId) {
        String result = referralService.claimReferralBonus(userId);
        return ResponseEntity.ok(result);
    }

    // Создать пользователя с реферальным кодом (альтернатива стандартному созданию)
    @PostMapping("/register")
    public ResponseEntity<String> registerWithReferral(
            @RequestParam String username,
            @RequestParam(required = false) String referralCode) {
        String result = referralService.registerWithReferral(username, referralCode);
        return ResponseEntity.ok(result);
    }
}