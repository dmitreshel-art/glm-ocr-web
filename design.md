# Technical Design: GLM-OCR Web Interface

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Compose                          │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Frontend   │───▶│  FastAPI     │───▶│  vLLM        │ │
│  │  (Static)    │    │  (API)       │    │  (GLM-OCR)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                             │                                │
│                      ┌──────────────┐                       │
│                      │   Redis       │                       │
│                      │   (Queue)     │                       │
│                      └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. vLLM Service (GPU)
- **Image:** vllm/vllm-openai:latest
- **Model:** zai-org/GLM-OCR
- **Port:** 8000 (internal)
- **Purpose:** Инференс модели

### 2. API Service (Backend)
- **Image:** Python 3.12 + FastAPI
- **Port:** 8001 (external)
- **Dependencies:** vLLM, Redis
- **Purpose:** API логика, валидация, оркестрация

### 3. Frontend (Web UI)
- **Type:** Static HTML/JS
- **Served by:** FastAPI
- **Purpose:** Загрузка файлов, отображение результатов

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Web UI |
| GET | /health | Health check |
| POST | /api/parse | OCR обработка |
| GET | /api/result/{id} | Получить результат |

## Data Flow

1. Пользователь загружает файл через веб-интерфейс
2. Frontend отправляет POST на /api/parse
3. API сохраняет файл, отправляет задачу в Redis
4. Worker забирает задачу, отправляет в vLLM
5. Результат сохраняется, возвращается клиенту

## Environment Variables

```yaml
# docker-compose.yml
services:
  api:
    environment:
      - VLLM_HOST=vllm
      - VLLM_PORT=8000
      - REDIS_HOST=redis
      - REDIS_PORT=6379
```

## Volume Mounts

```yaml
volumes:
  - ./uploads:/app/uploads
  - ./results:/app/results
  - ./models:/models  # кэш модели
```

## GPU Requirements

- CUDA 12.1+
- VRAM: минимум 8GB (рекомендуется 16GB)
- Для 0.9B модели должно хватить

## Security Considerations

- Rate limiting на API endpoints
- Валидация загружаемых файлов (размер, тип)
- Изоляция через Docker network

## Future Enhancements (Out of Scope)

- Аутентификация
- Продвинутый editor результатов
- Экспорт в PDF/DOCX
- Мобильное приложение
