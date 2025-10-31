package com.example.hyperDragon.dto;

import lombok.Data;

@Data
public class ReferralResponse {
    private String referralCode;
    private Integer referralsCount;
    private Integer totalBonus;
    private Boolean bonusClaimed;

    public ReferralResponse(String referralCode, Integer referralsCount, Boolean bonusClaimed) {
        this.referralCode = referralCode;
        this.referralsCount = referralsCount;
        this.totalBonus = referralsCount * 10000;
        this.bonusClaimed = bonusClaimed;
    }
}