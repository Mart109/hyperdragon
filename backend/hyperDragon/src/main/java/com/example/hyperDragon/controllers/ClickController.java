package com.example.hyperDragon.controllers;

import com.example.hyperDragon.dto.ClickResponse;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.UserRepository;
import com.example.hyperDragon.service.ClickerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/clicker")
public class ClickController {

    @Autowired
    private ClickerService clickerService;

    @Autowired
    private UserRepository userRepository;

    // Универсальный эндпоинт для создания/входа пользователя
    @PostMapping("/create-user")
    public ClickResponse createOrLoginUser(@RequestParam String username) {
        Optional<Users> userOpt = userRepository.findByUsername(username);

        if (userOpt.isPresent()) {
            // Пользователь существует - возвращаем его данные (автоматический вход)
            Users user = userOpt.get();
            return new ClickResponse(
                    user.getUsername(),
                    user.getCoins(),
                    user.getLevel(),
                    user.getId(),
                    user.getEnergy(),
                    user.getMaxEnergy(),
                    "Вход выполнен"
            );
        } else {
            // Создаем нового пользователя (регистрация)
            Users newUser = new Users(username);
            Users savedUser = userRepository.save(newUser);
            return new ClickResponse(
                    savedUser.getUsername(),
                    savedUser.getCoins(),
                    savedUser.getLevel(),
                    savedUser.getId(),
                    savedUser.getEnergy(),
                    savedUser.getMaxEnergy(),
                    "Пользователь создан"
            );
        }
    }

    // Клик по ID с проверкой энергии
    @PostMapping("/click-by-id")
    public ClickResponse handleClickById(@RequestHeader("X-User-Id") Long userId) {
        return clickerService.handleClickById(userId);
    }

    // Получить информацию о пользователе
    @GetMapping("/user-info")
    public ClickResponse getUserInfo(@RequestHeader("X-User-Id") Long userId) {
        return clickerService.getUserInfo(userId);
    }

    // Восстановить всю энергию (для тестов)
    @PostMapping("/restore-energy")
    public ClickResponse restoreEnergy(@RequestHeader("X-User-Id") Long userId) {
        return clickerService.restoreFullEnergy(userId);
    }

    // Получить всех пользователей (для отладки)
    @GetMapping("/all-users")
    public List<Users> getAllUsers() {
        return userRepository.findAll();
    }
}