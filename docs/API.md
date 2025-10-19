# Hype Drakon API Documentation

## Base URL
`https://api.drakon.example.com/v1`

## Authentication
```http
Authorization: Bearer <bot_token>
```

## Endpoints

### Game State
`GET /game/state`
```json
{
  "player_id": "uuid",
  "coins": 1500,
  "dragons": [
    {
      "id": 1,
      "type": "fire",
      "level": 3,
      "damage": 45
    }
  ]
}
```

### PvP Matchmaking
`POST /pvp/queue`
Request:
```json
{
  "player_id": "uuid",
  "dragon_id": 1
}
```

Response:
```json
{
  "battle_id": "uuid",
  "opponent": "username",
  "timeout": 30
}
```

### Error Responses
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

## Webhooks

### Battle Results
```json
{
  "event": "pvp_result",
  "battle_id": "uuid",
  "winner": "player_id",
  "reward": 250
}
```