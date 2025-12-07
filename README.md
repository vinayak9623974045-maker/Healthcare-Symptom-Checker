# Healthcare Symptom Checker

Educational demo that accepts symptom text and returns probable conditions and recommendations using an LLM.

## Structure
- backend/: FastAPI app
- frontend/: React + Vite interactive UI

## Run (backend)
1. cd backend
2. pip install -r requirements.txt
3. set OPENAI_API_KEY in environment or .env
4. uvicorn app.main:app --reload --port 8000

## Run (frontend)
1. cd frontend
2. npm install
3. npm run dev
