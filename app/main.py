"""
GLM-OCR Web Interface - FastAPI Backend
"""
import os
import uuid
import aiofiles
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))
RESULT_DIR = Path(os.getenv("RESULT_DIR", "/app/results"))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "50")) * 1024 * 1024

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="GLM-OCR API",
    description="Web Interface for GLM-OCR Document Recognition",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OCRRequest(BaseModel):
    """OCR Request model"""
    image_url: Optional[str] = None


class OCRResponse(BaseModel):
    """OCR Response model"""
    task_id: str
    status: str
    markdown: Optional[str] = None
    json_result: Optional[dict] = None
    error: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the web interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GLM-OCR Web Interface</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #fff; text-align: center; margin-bottom: 30px; }
            .card {
                background: rgba(255,255,255,0.1);
                border-radius: 16px;
                padding: 30px;
                backdrop-filter: blur(10px);
            }
            .upload-area {
                border: 2px dashed rgba(255,255,255,0.3);
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s;
            }
            .upload-area:hover { border-color: #4facfe; background: rgba(79,172,254,0.1); }
            .upload-area input { display: none; }
            .upload-icon { font-size: 48px; margin-bottom: 15px; }
            .btn {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: #fff;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
            }
            .btn:disabled { opacity: 0.5; cursor: not-allowed; }
            .result { margin-top: 30px; }
            .result textarea {
                width: 100%;
                min-height: 300px;
                background: rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                color: #fff;
                padding: 15px;
                font-family: monospace;
                font-size: 14px;
            }
            .loading { 
                display: none; 
                text-align: center; 
                color: #4facfe;
                margin: 20px 0;
            }
            .spinner {
                border: 3px solid rgba(79,172,254,0.3);
                border-top: 3px solid #4facfe;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .error { color: #ff6b6b; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 GLM-OCR Web Interface</h1>
            <div class="card">
                <div class="upload-area" onclick="document.getElementById('file').click()">
                    <div class="upload-icon">📁</div>
                    <p style="color: rgba(255,255,255,0.7);">Click to upload or drag and drop</p>
                    <p style="color: rgba(255,255,255,0.5); font-size: 14px; margin-top: 10px;">
                        Supported: PNG, JPG, JPEG, PDF
                    </p>
                    <input type="file" id="file" name="file" accept="image/*,.pdf" onchange="handleFile(this)">
                </div>
                <button class="btn" onclick="processOCR()" id="submitBtn">Process OCR</button>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing document with GLM-OCR...</p>
                </div>
                
                <div class="error" id="error"></div>
                
                <div class="result" id="result" style="display: none;">
                    <h3 style="color: #fff; margin-bottom: 15px;">Recognition Result:</h3>
                    <textarea id="output" readonly></textarea>
                </div>
            </div>
        </div>
        
        <script>
            let currentFile = null;
            
            function handleFile(input) {
                if (input.files && input.files[0]) {
                    currentFile = input.files[0];
                    document.getElementById('error').textContent = '';
                }
            }
            
            async function processOCR() {
                if (!currentFile) {
                    document.getElementById('error').textContent = 'Please select a file first';
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', currentFile);
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
                document.getElementById('error').textContent = '';
                document.getElementById('submitBtn').disabled = true;
                
                try {
                    const response = await fetch('/api/parse', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'OCR processing failed');
                    }
                    
                    const data = await response.json();
                    
                    document.getElementById('output').value = data.markdown || JSON.stringify(data.json_result, null, 2);
                    document.getElementById('result').style.display = 'block';
                } catch (err) {
                    document.getElementById('error').textContent = err.message;
                } finally {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('submitBtn').disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check Ollama availability
    ollama_available = False
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/tags", timeout=5.0)
            ollama_available = response.status_code == 200
    except Exception:
        pass
    
    return {
        "status": "healthy" if ollama_available else "degraded",
        "service": "glm-ocr-api",
        "version": "1.0.0",
        "ollama_available": ollama_available,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/parse")
async def parse_document(file: UploadFile = File(...)):
    """
    Process uploaded document with GLM-OCR
    
    Args:
        file: Uploaded image/PDF file
        
    Returns:
        OCR result in Markdown and JSON format
    """
    # Validate file
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB")
    
    # Save uploaded file
    task_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix.lower()
    file_path = UPLOAD_DIR / f"{task_id}{file_ext}"
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Call vLLM API
    try:
        # Convert to base64 for API call
        import base64
        with open(file_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Call Ollama API
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat",
                json={
                    "model": "glm-ocr",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "image", "image": f"data:image/{file_ext[1:]};base64,{image_base64}"},
                                {"type": "text", "text": "Extract all text from this document. Return the result in markdown format."}
                            ]
                        }
                    ],
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.text}")
            
            result = response.json()
            markdown_text = result['message']['content']
            
    except Exception as e:
        # Return error but keep file for debugging
        return JSONResponse(
            status_code=500,
            content={
                "task_id": task_id,
                "status": "error",
                "error": str(e)
            }
        )
    
    # Save result
    result_data = {
        "task_id": task_id,
        "status": "completed",
        "filename": file.filename,
        "markdown": markdown_text,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    result_path = RESULT_DIR / f"{task_id}.json"
    import json
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    return result_data


@app.get("/api/result/{task_id}")
async def get_result(task_id: str):
    """Get OCR result by task ID"""
    result_path = RESULT_DIR / f"{task_id}.json"
    
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Result not found")
    
    import json
    with open(result_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
