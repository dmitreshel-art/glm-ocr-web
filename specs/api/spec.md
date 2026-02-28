# API Specification

## ADDED Requirements

### Requirement: OCR Processing Endpoint
Система ДОЛЖНА предоставлять endpoint для загрузки изображения и получения OCR результата.

#### Scenario: Upload image for OCR
**GIVEN** пользователь загружает изображение через веб-интерфейс
**WHEN** POST /api/parse вызывается с файлом
**THEN** система возвращает распознанный текст в формате Markdown и JSON

### Requirement: Batch Processing
Система ДОЛЖНА поддерживать обработку нескольких изображений (PDF страницы или несколько файлов).

#### Scenario: Batch upload
**GIVEN** пользователь загружает несколько файлов
**WHEN** POST /api/parse вызывается с массивом файлов
**THEN** система возвращает результаты для каждого файла

### Requirement: Health Check
Система ДОЛЖНА предоставлять endpoint для проверки статуса.

#### Scenario: Health check
**WHEN** GET /health вызывается
**THEN** система возвращает статус сервиса и доступность модели

### Requirement: Web Interface
Система ДОЛЖНА предоставлять веб-интерфейс для загрузки файлов.

#### Scenario: User opens web interface
**GIVEN** пользователь открывает главную страницу
**WHEN** GET / вызывается
**THEN** система возвращает HTML страницу с формой загрузки

## MODIFIED Requirements

### Requirement: Configuration
**Previous:** Конфигурация через YAML файл
**New:** Конфигурация через environment variables + docker-compose.yml
