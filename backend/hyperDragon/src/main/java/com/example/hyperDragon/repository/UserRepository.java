package com.example.hyperDragon.repository;

import com.example.hyperDragon.entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<Users, Long> {
    Optional<Users> findByUsername(String username);

    // Новый метод для поиска по реферальному коду
    Optional<Users> findByReferralCode(String referralCode);

    // Метод для получения количества рефералов
    @Query("SELECT COUNT(u) FROM Users u WHERE u.referrerId = :userId")
    Long countReferralsByUserId(@Param("userId") Long userId);
}