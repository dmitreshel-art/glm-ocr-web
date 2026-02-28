# GLM-OCR Web Interface

Docker-приложение с веб-интерфейсом для распознавания документов на базе GLM-OCR с Ollama.

## Требования

- Docker
- Docker Compose
- **GPU:** рекомендуется 8GB+ VRAM
- **CPU:** работает, но медленно (~минуты на страницу)

## Быстрый старт

### 1. Запуск

```bash
cd glm-ocr-web
docker-compose up -d
```

### 2. Загрузка модели

После первого запуска нужно загрузить модель:

```bash
docker exec glm-ocr-ollama ollama pull glm-ocr
```

### 3. Использование

- **Веб-интерфейс:** http://localhost:80
- **API:** http://localhost:8001
- **Health check:** http://localhost:8001/health
- **Ollama:** http://localhost:11434

## CPU-only режим

Для запуска без GPU:

```bash
# Раскомментируй в docker-compose.yml:
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
#           count: 0
#           capabilities: [gpu]
```

Или используй `docker-compose.cpu.yml`:

```bash
docker-compose -f docker-compose.cpu.yml up -d
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Веб-интерфейс |
| GET | /health | Проверка статуса |
| POST | /api/parse | Обработка OCR |
| GET | /api/result/{id} | Получить результат |

## Остановка

```bash
docker-compose down
```

## Устранение неполадок

### Модель не загружена
```bash
docker exec glm-ocr-ollama ollama list
```

### GPU не обнаружена
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi
```

## Лицензия

Apache 2.0 (GLM-OCR + PaddleOCR компоненты)
