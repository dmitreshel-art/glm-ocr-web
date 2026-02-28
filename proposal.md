# Proposal: GLM-OCR Web Interface

## Overview

Создание Docker-приложения с веб-интерфейсом для распознавания документов на базе GLM-OCR.

## Problem Statement

Нужно простое разворачиваемое решение для OCR документов с веб-интерфейсом. GLM-OCR предоставляет мощный OCR движок, но требует Docker-упаковки для удобного деплоя.

## Scope

### In Scope
- Docker-compose с GLM-OCR (vLLM/SGLang)
- Веб-интерфейс для загрузки изображений
- REST API для интеграций
- Поддержка GPU

### Out of Scope
- Облачная версия (только локальная)
- Аутентификация/авторизация (первая версия)

## Approach

1. Использовать vLLM для запуска GLM-OCR модели
2. Flask/FastAPI backend для API
3. Простой HTML/JS frontend
4. Docker-compose для оркестрации

## Risks

- Требуется GPU для inference
- Размер образа может быть большим

## Priority

High — практическая задача

## Tags

- docker
- ocr
- document-processing
- web-interface
