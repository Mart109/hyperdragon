package com.example.hyperDragon.service;

import com.example.hyperDragon.dto.ReferralResponse;
import com.example.hyperDragon.entity.Users;
import com.example.hyperDragon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class ReferralService {

    @Autowired
    private UserRepository userRepository;

    // Получить реферальную информацию пользователя
    public ReferralResponse getReferralInfo(Long userId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return null;
        }

        Users user = userOpt.get();
        return new ReferralResponse(
                user.getReferralCode(),
                user.getReferralsCount(),
                user.getReferralBonusClaimed()
        );
    }

    // Регистрация с реферальным кодом
    @Transactional
    public String registerWithReferral(String username, String referralCode) {
        // Проверяем существование пользователя
        if (userRepository.findByUsername(username).isPresent()) {
            return "Пользователь с таким именем уже существует";
        }

        Users newUser = new Users(username);

        // Если указан реферальный код, находим пригласившего
        if (referralCode != null && !referralCode.trim().isEmpty()) {
            Optional<Users> referrerOpt = userRepository.findByReferralCode(referralCode);
            if (referrerOpt.isPresent()) {
                Users referrer = referrerOpt.get();

                // Проверяем, что пользователь не приглашает сам себя
                if (!referrer.getUsername().equals(username)) {
                    newUser.setReferrerId(referrer.getId());
                    referrer.addReferral();
                    userRepository.save(referrer);
                }
            } else {
                return "Неверный реферальный код";
            }
        }

        userRepository.save(newUser);
        return "Пользователь " + username + " успешно зарегистрирован" +
                (newUser.getReferrerId() != null ? " по реферальной ссылке" : "");
    }

    // Получить бонус за рефералов
    @Transactional
    public String claimReferralBonus(Long userId) {
        Optional<Users> userOpt = userRepository.findById(userId);
        if (userOpt.isEmpty()) {
            return "Пользователь не найден";
        }

        Users user = userOpt.get();

        if (user.getReferralBonusClaimed()) {
            return "Бонус уже был получен";
        }

        if (user.getReferralsCount() == 0) {
            return "У вас нет рефералов для получения бонуса";
        }

        user.claimReferralBonus();
        userRepository.save(user);

        return "Получен реферальный бонус: " + (user.getReferralsCount() * 10000) + " монет!";
    }

    // Получить пользователя по реферальному коду
    public Optional<Users> getUserByReferralCode(String referralCode) {
        return userRepository.findByReferralCode(referralCode);
    }
}