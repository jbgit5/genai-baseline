# GenAI Baseline Project – What We Built So Far

## 1. Purpose of This Document
This document exists so that **future-you** can:
- Quickly understand **what this project is**
- Recall **what has already been implemented**
- Know **exactly how to run the project** without re-learning everything
- See **what is pending** as per Module 1 requirements

This is intentionally written in **simple, operational language**, not academic.

---

## 2. Project Goal (High Level)

Build a **learning-focused Retrieval system** using:
- FastAPI (backend)
- PostgreSQL (database)
- pgvector (vector similarity)
- File upload (CV / documents)

⚠️ **Important constraint:**
- NO AI models (OpenAI / HuggingFace / LLMs)
- All logic is deterministic to understand each concept clearly

This aligns with **Module 1: Retrieval / RAG fundamentals**.

---

## 3. Tech Stack Used

- **Backend:** FastAPI
- **Database:** PostgreSQL (Docker)
- **ORM / DB access:** psycopg / SQLAlchemy (light usage)
- **Vector search:** pgvector (to be enabled)
- **Frontend:** Simple browser UI (HTML + fetch)
- **Runtime:** Python 3.12, virtual environment

---

## 4. Project Folder Structure (Current)

```
genai-baseline/
│
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── db.py            # Database connection
│   ├── models.py        # Table definitions (documents)
│   ├── ingest.py        # /ingest endpoint logic
│   ├── search.py        # /search endpoint logic
│
├── static/
│   └── index.html       # Simple browser UI
│
├── requirements.txt
├── docker-compose.yml   # PostgreSQL container
├── venv/                # Python virtual environment
```

---

## 5. What Has Been Implemented (As of Now)

### 5.1 FastAPI Application

- App starts successfully using **uvicorn**
- Endpoints are accessible on `http://localhost:8000`

Command used:
```bash
uvicorn app.main:app --reload
```

---

### 5.2 PostgreSQL via Docker

- PostgreSQL is running in Docker
- Database connection is working
- Tables are being written to

Typical container command:
```bash
docker ps
docker exec -it <postgres_container> psql -U postgres
```

---

### 5.3 /ingest Endpoint (Working)

**What it does:**
- Accepts CV data (currently text-based or extracted text)
- Stores candidate information in database

Example request:
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ravi Kumar",
    "email": "ravi@example.com",
    "cv_text": "Python developer with FastAPI, PostgreSQL, Docker experience"
  }'
```

Example response:
```json
{
  "message": "CV ingested successfully",
  "candidate_id": "uuid"
}
```

✅ Confirms backend + DB write is functional

---

### 5.4 /search Endpoint (Working – Keyword Based)

**What it does:**
- Accepts a search query
- Returns matching candidates based on stored text

Example request:
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{ "query": "FastAPI PostgreSQL" }'
```

Example response:
```json
{
  "results": [
    {
      "name": "Anita Sharma",
      "email": "anita@example.com",
      "rank": 0.09,
      "snippet": "Backend engineer with Python, FastAPI, PostgreSQL"
    }
  ]
}
```

⚠️ This is **NOT vector search yet**. It is text-based ranking.

---

### 5.5 Browser UI (Basic)

- HTML page served from browser
- Allows:
  - Uploading CV
  - Searching candidates
- Uses fetch API to call FastAPI endpoints

Purpose: **manual testing + demo**, not production UI

---

## 6. What Is NOT Implemented Yet (Important)

These are **Module 1 gaps**:

❌ pgvector extension not enabled
❌ No embeddings table
❌ No numeric vectors stored
❌ No chunking logic
❌ No /ask endpoint
❌ No citations
❌ No fallback response when no data

---

## 7. What We Decided (Design Decisions)

### 7.1 No AI Models

Reason:
- Learn fundamentals (embeddings, vectors, retrieval)
- Avoid black-box behavior

We will use:
- Deterministic hashing-based vectors

---

### 7.2 Chunking Strategy (Planned)

- Split documents into **~200-word chunks**
- Each chunk stored separately
- Each chunk gets its own vector

Reason:
- Better retrieval granularity
- Matches real RAG systems

---

### 7.3 Database Design (Planned)

Two tables:

**documents**
- Stores original document

**embeddings**
- Stores chunks + vectors

pgvector will be used for similarity search.

---

## 8. How to Run This Project (Step-by-Step)

### 8.1 Start PostgreSQL

```bash
docker-compose up -d
```

Verify:
```bash
docker ps
```

---

### 8.2 Activate Virtual Environment

```bash
source venv/bin/activate
```

---

### 8.3 Install Dependencies (If Needed)

```bash
pip install -r requirements.txt
```

---

### 8.4 Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

Access:
- API: http://localhost:8000
- UI: http://localhost:8000 (if static mounted)

---

## 9. Next Planned Steps (Module 1 Completion)

1. Enable pgvector extension
2. Create embeddings table
3. Implement chunking logic
4. Implement fake embedding generator
5. Add /ask endpoint
6. Add citations in response
7. Add friendly fallback message
8. Write short design note

---

## 10. Why This Project Matters

By completing this:
- You understand **RAG without hype**
- You understand **why vectors work**
- You can later plug in real LLMs confidently

This is **backend + systems learning**, not copy-paste AI.

---

## 11. Reminder to Future You

If you are lost:
1. Start PostgreSQL
2. Activate venv
3. Run uvicorn
4. Read Section 5 (what already works)
5. Continue from Section 9

You already did the hard part.

