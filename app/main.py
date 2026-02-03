from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.db import get_connection
from app.chunking import chunk_text
from app.embedding import fake_embedding

import shutil
import pdfplumber
import docx
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SIMILARITY_THRESHOLD = 0.05  # low threshold for sparse fake embeddings (single-word queries)


# -------------------------------------------------
# Home Page (UI)
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------
# Ingest CV (UI – Browser only)
# -------------------------------------------------
@app.post("/ingest", response_class=HTMLResponse)
async def ingest_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # -------- Extract text --------
    cv_text = ""

    try:
        if file.filename.lower().endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        cv_text += text + "\n"

        elif file.filename.lower().endswith(".docx"):
            doc = docx.Document(file_path)
            cv_text = "\n".join(p.text for p in doc.paragraphs)

        else:
            raise ValueError("Unsupported file type")

        if not cv_text.strip():
            raise ValueError("No text could be extracted")

        chunks = chunk_text(cv_text)

        conn = get_connection()
        cur = conn.cursor()

        # -------- Insert document --------
        cur.execute(
            """
            INSERT INTO documents (source, content)
            VALUES (%s, %s)
            RETURNING id
            """,
            (f"{name} ({email})", cv_text),
        )
        document_id = cur.fetchone()[0]

        # -------- Insert embeddings --------
        for chunk in chunks:
            vec = fake_embedding(chunk)
            cur.execute(
                """
                INSERT INTO embeddings (document_id, chunk_text, embedding)
                VALUES (%s, %s, %s)
                """,
                (document_id, chunk, vec),
            )

        conn.commit()
        message = f"CV uploaded successfully for {name}"

    except Exception as e:
        conn.rollback()
        message = f"Error: {e}"

    finally:
        cur.close()
        conn.close()
        os.remove(file_path)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": message},
    )


# -------------------------------------------------
# Search – UI (Browser)
# -------------------------------------------------
@app.post("/ask-ui", response_class=HTMLResponse)
async def ask_ui(request: Request, query: str = Form(...)):
    query_vec = fake_embedding(query)

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT
                d.source,
                e.chunk_text,
                1 - (e.embedding <=> %s::vector) AS similarity
            FROM embeddings e
            JOIN documents d ON d.id = e.document_id
            ORDER BY similarity DESC
            LIMIT 5
            """,
            (query_vec,),
        )

        rows = cur.fetchall()

        results = [
            {
                "source": r[0],
                "content": r[1],
                "similarity": float(r[2]),
            }
            for r in rows
            if r[2] >= SIMILARITY_THRESHOLD
        ]

        if not results:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "message": "I don’t have enough information to answer that.",
                },
            )

    finally:
        cur.close()
        conn.close()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results, "query": query},
    )


# -------------------------------------------------
# Search – API (Postman / JSON)
# -------------------------------------------------
@app.post("/ask")
async def ask_api(payload: dict):
    query = payload.get("query")

    if not query:
        return JSONResponse(
            status_code=400,
            content={"error": "query field is required"},
        )

    query_vec = fake_embedding(query)

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT
                e.chunk_text,
                1 - (e.embedding <=> %s::vector) AS similarity
            FROM embeddings e
            ORDER BY similarity DESC
            LIMIT 5
            """,
            (query_vec,),
        )

        rows = cur.fetchall()

        results = [
            {
                "content": r[0],
                "similarity": float(r[1]),
            }
            for r in rows
            if r[1] >= SIMILARITY_THRESHOLD
        ]

        if not results:
            return {
                "query": query,
                "answer": "I don’t have enough information to answer that.",
                "sources": [],
            }

        return {
            "query": query,
            "sources": results,
        }

    finally:
        cur.close()
        conn.close()
