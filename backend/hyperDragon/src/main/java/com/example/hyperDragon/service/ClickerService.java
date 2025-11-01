package com.example.hyperDragon.service;

import com.example.hyperDragon.dto.ClickResponse;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class ClickerService {

    @Autowired
    private UserRepository userRepository;

    // Максимальный уровень и базовая стоимость
    private static final int MAX_LEVEL = 1000;
    private static final int BASE_COINS_PER_LEVEL = 1000;

    @Transactional
    public ClickResponse handleClickById(Long userId) {
        try {
            System.out.println("=== handleClickById called for userId: " + userId);

            Optional<Users> userOpt = userRepository.findById(userId);
            System.out.println("User found: " + userOpt.isPresent());

            if (userOpt.isPresent()) {
                Users user = userOpt.get();
                System.out.println("User before energy restore: " + user);

                restoreEnergy(user);
                System.out.println("User after energy restore: " + user);

                if (user.getEnergy() <= 0) {
                    return createResponse(user, "Недостаточно энергии! Подождите восстановления.");
                }

                user.setEnergy(user.getEnergy() - 1);
                return processClick(user, "Клик успешен!");
            }

            throw new RuntimeException("User not found with id: " + userId);

        } catch (Exception e) {
            System.err.println("ERROR in handleClickById: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    private void restoreEnergy(Users user) {
        try {
            if (user.getLastEnergyUpdate() == null) {
                user.setLastEnergyUpdate(LocalDateTime.now());
                return;
            }

            LocalDateTime now = LocalDateTime.now();
            Duration duration = Duration.between(user.getLastEnergyUpdate(), now);
            long secondsPassed = duration.getSeconds();

            int energyToRestore = (int) (secondsPassed / 1.5);

            if (energyToRestore > 0) {
                int newEnergy = Math.min(user.getEnergy() + energyToRestore, user.getMaxEnergy());
                user.setEnergy(newEnergy);
                user.setLastEnergyUpdate(now);
                System.out.println("Restored " + energyToRestore + " energy. New energy: " + newEnergy);
            }
        } catch (Exception e) {
            System.err.println("ERROR in restoreEnergy: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private ClickResponse processClick(Users user, String message) {
        user.setCoins(user.getCoins() + 1);

        checkAndUpdateLevel(user);

        Users savedUser = userRepository.save(user);
        return createResponse(savedUser, message);
    }

    /**
     * Новая система уровней: каждый уровень требует level * 1000 монет
     * Уровень 1: 1000 монет
     * Уровень 2: 2000 монет
     * Уровень 3: 3000 монет
     * ...
     * Уровень 1000: 1,000,000 монет
     */
    private void checkAndUpdateLevel(Users user) {
        if (user.getLevel() >= MAX_LEVEL) {
            return; // Достигнут максимальный уровень
        }

        int requiredCoins = (user.getLevel() + 1) * BASE_COINS_PER_LEVEL;

        if (user.getCoins() >= requiredCoins) {
            user.setLevel(user.getLevel() + 1);
            System.out.println("🎉 Уровень повышен до " + user.getLevel() + "! Нужно для след. уровня: " + ((user.getLevel() + 1) * BASE_COINS_PER_LEVEL) + " монет");
        }
    }

    public ClickResponse getUserInfo(Long userId) {
        try {
            System.out.println("=== getUserInfo called for userId: " + userId);

            Optional<Users> userOpt = userRepository.findById(userId);

            if (userOpt.isPresent()) {
                Users user = userOpt.get();
                restoreEnergy(user);
                userRepository.save(user);
                return createResponse(user, "Информация о пользователе");
            }

            throw new RuntimeException("User not found with id: " + userId);

        } catch (Exception e) {
            System.err.println("ERROR in getUserInfo: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    @Transactional
    public ClickResponse restoreFullEnergy(Long userId) {
        try {
            System.out.println("=== restoreFullEnergy called for userId: " + userId);

            Optional<Users> userOpt = userRepository.findById(userId);

            if (userOpt.isPresent()) {
                Users user = userOpt.get();
                user.setEnergy(user.getMaxEnergy());
                user.setLastEnergyUpdate(LocalDateTime.now());
                Users savedUser = userRepository.save(user);

                return createResponse(savedUser, "Энергия полностью восстановлена!");
            }

            throw new RuntimeException("User not found with id: " + userId);

        } catch (Exception e) {
            System.err.println("ERROR in restoreFullEnergy: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    private ClickResponse createResponse(Users user, String message) {
        return new ClickResponse(
                user.getUsername(),
                user.getCoins(),
                user.getLevel(),
                user.getId(),
                user.getEnergy(),
                user.getMaxEnergy(),
                message
        );
    }

    // Метод для создания пользователя если не существует
    @Transactional
    public ClickResponse createUserIfNotExists(String username) {
        Optional<Users> userOpt = userRepository.findByUsername(username);

        if (userOpt.isPresent()) {
            Users user = userOpt.get();
            return createResponse(user, "Пользователь уже существует");
        }

        Users newUser = new Users(username);
        Users savedUser = userRepository.save(newUser);
        return createResponse(savedUser, "Пользователь создан");
    }

    /**
     * Вспомогательный метод для получения информации о следующем уровне
     */
    public String getNextLevelInfo(Users user) {
        if (user.getLevel() >= MAX_LEVEL) {
            return "Достигнут максимальный уровень (" + MAX_LEVEL + ")!";
        }

        int currentLevel = user.getLevel();
        int nextLevel = currentLevel + 1;
        int requiredCoins = nextLevel * BASE_COINS_PER_LEVEL;
        int coinsNeeded = requiredCoins - user.getCoins();

        return String.format(
                "Уровень %d → %d: нужно %d монет (осталось: %d)",
                currentLevel, nextLevel, requiredCoins, coinsNeeded
        );
    }
}