package com.example.hyperDragon.repository;

import com.example.hyperDragon.entity.MiniGameResult;
import com.example.hyperDragon.entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MiniGameRepository extends JpaRepository<MiniGameResult, Long> {

    List<MiniGameResult> findByUserOrderByPlayDateDesc(Users user);

    @Query("SELECT COUNT(m) FROM MiniGameResult m WHERE m.user.id = :userId")
    Long countGamesByUserId(@Param("userId") Long userId);

    @Query("SELECT COUNT(m) FROM MiniGameResult m WHERE m.user.id = :userId AND m.won = true")
    Long countWinsByUserId(@Param("userId") Long userId);

    @Query("SELECT MAX(m.pointsDestroyed) FROM MiniGameResult m WHERE m.user.id = :userId")
    Integer findBestScoreByUserId(@Param("userId") Long userId);

    @Query("SELECT COALESCE(SUM(m.pointsDestroyed), 0) FROM MiniGameResult m WHERE m.user.id = :userId")
    Integer getTotalPointsByUserId(@Param("userId") Long userId);

    @Query("SELECT COALESCE(SUM(m.coinsEarned), 0) FROM MiniGameResult m WHERE m.user.id = :userId")
    Integer getTotalCoinsEarnedByUserId(@Param("userId") Long userId);
}