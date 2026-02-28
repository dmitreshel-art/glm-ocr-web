# Tasks: GLM-OCR Web Interface

## Implementation Checklist

- [x] **1. Create project structure**
  - [x] Dockerfile для API
  - [x] docker-compose.yml
  - [x] .env.example

- [x] **2. Implement FastAPI backend**
  - [x] Main application (main.py)
  - [ ] OCR service wrapper (используем прямые вызовы к vLLM)
  - [x] File upload handler
  - [x] API routes

- [x] **3. Create frontend**
  - [x] HTML template (встроен в main.py)
  - [x] CSS styling
  - [x] JavaScript for API calls
  - [x] Result display

- [x] **4. Configure vLLM**
  - [x] Docker service config
  - [ ] Model loading (автоматически при первом запуске)

- [ ] **5. Test locally**
  - [ ] Build images
  - [ ] Run docker-compose
  - [ ] Test OCR pipeline

- [x] **6. Documentation**
  - [x] README.md
  - [x] Usage instructions

## Progress

**Status:** Planning complete, starting implementation

**Current:** Creating project structure
