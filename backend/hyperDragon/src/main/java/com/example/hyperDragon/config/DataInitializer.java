package com.example.hyperDragon.config;

import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.UserRepository;
import com.example.hyperDragon.service.CardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private CardService cardService;

    @Autowired
    private UserRepository userRepository;

    @Override
    public void run(String... args) throws Exception {
        // Инициализация карточек
        cardService.initializeCardTemplates();
        System.out.println("Карточки инициализированы");

        // Генерация реферальных кодов для существующих пользователей
        generateReferralCodesForExistingUsers();
        System.out.println("Реферальные коды сгенерированы");
    }

    private void generateReferralCodesForExistingUsers() {
        List<Users> users = userRepository.findAll();
        boolean needsUpdate = false;

        for (Users user : users) {
            if (user.getReferralCode() == null) {
                // Создаем реферальный код используя рефлексию или сеттер
                String referralCode = generateReferralCode(user);

                // Устанавливаем реферальный код через рефлексию
                try {
                    java.lang.reflect.Field field = Users.class.getDeclaredField("referralCode");
                    field.setAccessible(true);
                    field.set(user, referralCode);
                    needsUpdate = true;
                } catch (Exception e) {
                    System.err.println("Ошибка при установке реферального кода для пользователя " + user.getId() + ": " + e.getMessage());
                }
            }
        }

        if (needsUpdate) {
            userRepository.saveAll(users);
            System.out.println("Реферальные коды созданы для " + users.size() + " пользователей");
        }
    }

    private String generateReferralCode(Users user) {
        // Генерируем код на основе ID пользователя и случайных символов
        String base = "USER" + user.getId() + "REF";
        return base + java.util.UUID.randomUUID().toString().substring(0, 4).toUpperCase();
    }
}