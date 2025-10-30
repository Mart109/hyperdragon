package com.example.hyperDragon.service;

import com.example.hyperDragon.dto.CardResponse;
import com.example.hyperDragon.entity.Card;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.CardRepository;
import com.example.hyperDragon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class CardService {

    @Autowired
    private CardRepository cardRepository;

    @Autowired
    private UserRepository userRepository;

    // Методы для DTO
    public List<CardResponse> getAvailableCards() {
        List<Card> cards = cardRepository.findAvailableTemplates();
        return cards.stream()
                .map(this::toCardResponse)
                .collect(Collectors.toList());
    }

    public List<CardResponse> getUserCards(Long userId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return List.of();
        }

        List<Card> cards = cardRepository.findByOwner(userOpt.get());
        return cards.stream()
                .map(this::toCardResponse)
                .collect(Collectors.toList());
    }

    // Метод преобразования Entity в DTO
    private CardResponse toCardResponse(Card card) {
        if (card == null) return null;

        CardResponse response = new CardResponse();
        response.setId(card.getId());
        response.setName(card.getName());
        response.setDisplayName(card.getDisplayName());
        response.setDescription(card.getDescription());
        response.setLevel(card.getLevel());
        response.setBaseIncome(card.getBaseIncome());
        response.setUpgradeCost(card.getUpgradeCost());
        response.setIncomePerLevel(card.getIncomePerLevel());
        response.setIsAvailable(card.getIsAvailable());
        response.setNextUpgradeCost(card.getNextUpgradeCost());
        response.setCurrentIncome(card.getCurrentIncome());

        if (card.getOwner() != null) {
            response.setOwnerId(card.getOwner().getId());
            response.setOwnerUsername(card.getOwner().getUsername());
        }

        return response;
    }

    // Остальные методы остаются без изменений
    @Transactional
    public void initializeCardTemplates() {
        long cardCount = cardRepository.count();
        if (cardCount == 0) {
            List<Card> templates = List.of(
                    new Card("golden_dragon", "3 Golden Dragons", "Три золотых дракона приносят удачу", 50, 100, 25),
                    new Card("sport_dragon", "Sport Dragon", "Спортивный дракон полон энергии", 100, 200, 50),
                    new Card("dragon_lamba", "Dragon Lamba", "Дракон Ламба - символ скорости", 300, 500, 100),
                    new Card("dragon", "Dragon", "Могучий дракон - источник силы", 600, 1000, 200)
            );

            cardRepository.saveAll(templates);
            System.out.println("Создано " + templates.size() + " шаблонов карточек");
        }
    }

    @Transactional
    public String buyCard(Long userId, String cardName) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return "Пользователь не найден";
        }

        Users user = userOpt.get();

        List<Card> existingCards = cardRepository.findByOwnerAndName(user, cardName);
        if (!existingCards.isEmpty()) {
            return "У вас уже есть эта карточка";
        }

        Card template = cardRepository.findByNameAndOwnerIsNull(cardName);
        if (template == null) {
            return "Карточка не найдена";
        }

        if (user.getCoins() < template.getUpgradeCost()) {
            return "Недостаточно монет для покупки";
        }

        Card userCard = new Card();
        userCard.setName(template.getName());
        userCard.setDisplayName(template.getDisplayName());
        userCard.setDescription(template.getDescription());
        userCard.setBaseIncome(template.getBaseIncome());
        userCard.setUpgradeCost(template.getUpgradeCost());
        userCard.setIncomePerLevel(template.getIncomePerLevel());
        userCard.setLevel(1);
        userCard.setOwner(user);

        user.setCoins(user.getCoins() - template.getUpgradeCost());
        cardRepository.save(userCard);
        userRepository.save(user);

        return "Карточка '" + template.getDisplayName() + "' успешно куплена!";
    }

    @Transactional
    public String upgradeCard(Long userId, Long cardId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        Optional<Card> cardOpt = cardRepository.findById(cardId);

        if (userOpt.isEmpty() || cardOpt.isEmpty()) {
            return "Пользователь или карточка не найдены";
        }

        Users user = userOpt.get();
        Card card = cardOpt.get();

        if (!card.getOwner().getId().equals(userId)) {
            return "Эта карточка вам не принадлежит";
        }

        int upgradeCost = card.getNextUpgradeCost();

        if (user.getCoins() < upgradeCost) {
            return "Недостаточно монет для улучшения";
        }

        user.setCoins(user.getCoins() - upgradeCost);
        card.setLevel(card.getLevel() + 1);

        cardRepository.save(card);
        userRepository.save(user);

        return "Карточка '" + card.getDisplayName() + "' улучшена до уровня " + card.getLevel() + "!";
    }

    @Transactional
    public Integer collectPassiveIncome(Long userId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return 0;
        }

        Users user = userOpt.get();
        List<Card> userCards = cardRepository.findByOwner(user);

        if (userCards.isEmpty()) {
            return 0;
        }

        LocalDateTime now = LocalDateTime.now();
        if (user.getLastPassiveIncome() == null) {
            user.setLastPassiveIncome(now);
            userRepository.save(user);
            return 0;
        }

        Duration duration = Duration.between(user.getLastPassiveIncome(), now);
        long minutesPassed = duration.toMinutes();

        if (minutesPassed < 1) {
            return 0;
        }

        int totalIncome = 0;
        for (Card card : userCards) {
            totalIncome += card.getCurrentIncome() * minutesPassed;
        }

        user.setCoins(user.getCoins() + totalIncome);
        user.setLastPassiveIncome(now);
        userRepository.save(user);

        return totalIncome;
    }
}