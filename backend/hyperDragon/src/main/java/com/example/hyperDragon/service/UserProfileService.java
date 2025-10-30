package com.example.hyperDragon.service;

import com.example.hyperDragon.dto.UserProfileResponse;
import com.example.hyperDragon.entity.Card;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.CardRepository;
import com.example.hyperDragon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserProfileService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CardRepository cardRepository;

    @Autowired
    private ClickerService clickerService; // Если у вас есть сервис для кликов

    public UserProfileResponse getUserProfile(Long userId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return null;
        }

        Users user = userOpt.get();
        List<Card> userCards = cardRepository.findByOwner(user);

        UserProfileResponse response = new UserProfileResponse();

        // Основная информация
        response.setUserId(user.getId());
        response.setUsername(user.getUsername());
        response.setCoins(user.getCoins());
        response.setLevel(user.getLevel());
        response.setEnergy(user.getEnergy());
        response.setMaxEnergy(user.getMaxEnergy());
        response.setLastEnergyUpdate(user.getLastEnergyUpdate());
        response.setLastPassiveIncome(user.getLastPassiveIncome());

        // Опыт (можно рассчитать на основе уровня или кликов)
        response.setExperience(calculateExperience(user));

        // Информация о карточках
        response.setCardsCount(userCards.size());
        response.setTotalPassiveIncome(calculateTotalPassiveIncome(userCards));

        // Реферальная система
        response.setReferralCode(user.getReferralCode());
        response.setReferralsCount(user.getReferralsCount());
        response.setReferralBonus(user.getReferralsCount() * 10000); // 10000 за реферала
        response.setReferralBonusClaimed(user.getReferralBonusClaimed());

        // Статистика (если храните такую информацию)
        response.setTotalClicks(calculateTotalClicks(user)); // Нужно реализовать
        response.setRegisteredAt(user.getLastEnergyUpdate()); // Используем как дату регистрации

        return response;
    }

    private Integer calculateExperience(Users user) {
        // Формула опыта: базовый опыт + опыт за карточки + опыт за уровень
        int baseExp = user.getLevel() * 100;
        int cardsExp = cardRepository.findByOwner(user).size() * 50;
        return baseExp + cardsExp;
    }

    private Integer calculateTotalPassiveIncome(List<Card> cards) {
        return cards.stream()
                .mapToInt(Card::getCurrentIncome)
                .sum();
    }

    private Integer calculateTotalClicks(Users user) {
        // Если у вас есть подсчет кликов, добавьте его здесь
        // Например: return clickerService.getUserClicksCount(user.getId());
        return (user.getLevel() - 1) * 100 + 50; // Примерная формула
    }
}