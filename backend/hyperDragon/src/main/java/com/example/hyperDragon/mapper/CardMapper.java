package com.example.hyperDragon.mapper;

import com.example.hyperDragon.dto.CardResponse;
import com.example.hyperDragon.entity.Card;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface CardMapper {
    CardMapper INSTANCE = Mappers.getMapper(CardMapper.class);

    @Mapping(source = "owner.id", target = "ownerId")
    @Mapping(source = "owner.username", target = "ownerUsername")
    CardResponse toCardResponse(Card card);
}