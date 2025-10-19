# Система мониторинга Hype Drakon

## 1. Основные метрики
Доступны на `:8000/metrics`:
- **Игровая активность**:
  - `players_online` - текущие игроки
  - `battles_active` - активные бои

- **Производительность**:
  - `request_duration_seconds` - время ответа API
  - `database_query_time` - запросы к БД

## 2. Настройка оповещений
Пример для Prometheus Alertmanager:
```yaml
rules:
- alert: HighLoad
  expr: rate(http_requests_total[5m]) > 1000
  labels:
    severity: critical
  annotations:
    summary: "Высокая нагрузка на сервер"
```

## 3. Дашборды Grafana
Импортируйте готовый дашборд:
```json
{
  "title": "Hype Drakon Stats",
  "panels": [
    {
      "title": "Online Players",
      "type": "graph",
      "targets": [{
        "expr": "sum(players_online)"
      }]
    }
  ]
}
```

## 4. Логирование
Уровни логирования:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 5. Полезные команды
```bash
# Поиск ошибок в логах
kubectl logs -l app=hype-drakon | grep -i error

# Проверка нагрузки
kubectl top pods
```