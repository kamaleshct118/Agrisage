# AgriMind: System Configuration & Deployment Guide

This document provides complete technical instructions for building the persistent data layers, initializing the back-end API, and bootstrapping the Vite frontend. 

---

## 1. Environment & Dependencies

### Python Environment (FastAPI + CrewAI Backend)
Ensure you are running Python 3.10+ in a dedicated environment.
```bash
conda create -n agri_env python=3.10
conda activate agri_env
pip install -r requirements.txt
```

### Node Environment (React Frontend)
Ensure Node.js `v18+` is installed.
```bash
cd frontend
npm install
```

---

## 2. Data Pipeline Configuration

Before booting the system, you must construct the localized databases (RAG Vector Store & SQLite) from the raw datasets.

### 2.1 Directory Structure 
Ensure your raw tabular and JSON datasets are placed in the `backend/data/raw/` directory:
- `backend/data/raw/agriculture_data_Rag.json` (Knowledge Base corpus)
- `backend/data/raw/crop_yield.csv` (Historical production yields)
- `backend/data/raw/npk-dataset.csv` (Optimal NPK Baseline Requirements)

### 2.2 Building the SQLite Database
The SQLite artifact must be generated to enable Text-to-SQL capabilities.
```bash
cd backend
python scripts/build_db.py
```
**Outcome**: This instantiates an `agri.db` artifact inside `backend/data/processed/` containing the consolidated relational schemas (`npk_data` & `crop_production`).

### 2.3 Compiling the FAISS Vector Index
The FAISS index requires pre-computing embeddings for the `.json` corpus using `sentence-transformers/all-MiniLM-L6-v2`.
```bash
cd backend
python scripts/build_faiss.py
```
**Outcome**: Creates `faiss_index.bin` (L2 distance tensor vectors) and `metadata.json` (chunk mapping) inside `backend/data/processed/`.

---

## 3. Execution & Deployment

### 3.1 Environment Variables
Create a `.env` file in the `backend/` directory exposing the active LLM provider.
```env
# backend/.env
GROQ_API_KEY="gsk_YourSecureKeyHere"
```

### 3.2 Running the Backend API
The FastAPI ASGI server acts as the central interface for CrewAI interactions mapped over `localhost:8000/api/chat`.
```bash
cd backend
python app.py
```
*Expected console output: `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`*

### 3.3 Running the Frontend Application
The frontend is built on Vite, React, and standard Tailwind constraints.
```bash
cd frontend
npm run dev
```
*Access the UI at `http://localhost:5173`.*

---

## 4. Evaluation 
Unit testing and LLM validation utilize the `Ragas` semantic framework (Faithfulness & Answer Relevancy). Run evaluations using pre-stored test queries against the unified FAISS models.
```bash
cd evaluation
python ragas_eval.py
```
