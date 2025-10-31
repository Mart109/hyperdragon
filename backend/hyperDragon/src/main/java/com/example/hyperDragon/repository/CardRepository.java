package com.example.hyperDragon.repository;

import com.example.hyperDragon.entity.Card;
import com.example.hyperDragon.entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface CardRepository extends JpaRepository<Card, Long> {

    List<Card> findByOwner(Users owner);
    List<Card> findByOwnerAndName(Users owner, String name);

    @Query("SELECT c FROM Card c WHERE c.owner IS NULL AND c.isAvailable = true")
    List<Card> findAvailableTemplates();

    Card findByNameAndOwnerIsNull(String name);
}