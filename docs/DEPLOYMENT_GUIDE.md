# Руководство по развертыванию Hype Drakon

## 1. Способы деплоя
### 1.1 Локальная разработка (Docker)
```bash
# Сборка и запуск
docker-compose up -d --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f app
```

### 1.2 Продакшен (Kubernetes)
```bash
# Развертывание (требуется kubectl)
kubectl apply -f deployments/kubernetes/

# Обновление образа
kubectl set image deployment/hype-drakon app=registry.example.com/hype-drakon:v2.0.0
```

### 1.3 Bare-metal (без Docker)
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python -m hype_drakon --port 8000
```

## 2. Миграции базы данных
```bash
# Применение миграций
alembic upgrade head

# Создание новой миграции
alembic revision --autogenerate -m "Описание изменений"
```

## 3. Переменные окружения
Обязательные переменные:
```ini
DATABASE_URL=postgresql://user:password@host/dbname
TELEGRAM_TOKEN=ваш_токен
REDIS_URL=redis://redis:6379/0
```

## 4. Требования
| Ресурс       | Локально | Продакшен |
|--------------|----------|-----------|
| CPU          | 1 ядро   | 2+ ядра   |
| RAM          | 512 MB   | 2 GB      |
| Диск         | 1 GB     | 10 GB     |

## 5. Частые проблемы
**Проблема:** Не применяются миграции  
**Решение:** Проверить подключение к БД:
```bash
docker-compose exec db psql -U user drakon
```

**Проблема:** Бот не отвечает  
**Решение:** Проверить логи:
```bash
kubectl logs -l app=hype-drakon --tail=50
```