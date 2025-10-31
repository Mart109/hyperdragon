package com.example.hyperDragon.controllers;

import com.example.hyperDragon.dto.UserProfileResponse;
import com.example.hyperDragon.service.UserProfileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/profile")
public class ProfileController {

    @Autowired
    private UserProfileService userProfileService;

    // Получить полную информацию о пользователе для фронтенда
    @GetMapping
    public ResponseEntity<UserProfileResponse> getUserProfile(@RequestHeader("X-User-Id") Long userId) {
        UserProfileResponse profile = userProfileService.getUserProfile(userId);
        if (profile == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(profile);
    }

    // Получить краткую информацию (только основные поля)
    @GetMapping("/short")
    public ResponseEntity<?> getShortProfile(@RequestHeader("X-User-Id") Long userId) {
        UserProfileResponse profile = userProfileService.getUserProfile(userId);
        if (profile == null) {
            return ResponseEntity.notFound().build();
        }

        // Возвращаем только основные поля
        return ResponseEntity.ok().body(new Object() {
            public final Long userId = profile.getUserId();
            public final String username = profile.getUsername();
            public final Integer coins = profile.getCoins();
            public final Integer level = profile.getLevel();
            public final Integer experience = profile.getExperience();
            public final Integer energy = profile.getEnergy();
            public final Integer maxEnergy = profile.getMaxEnergy();
        });
    }
}