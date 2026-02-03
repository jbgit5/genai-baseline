import psycopg2
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://genai:genai@localhost:5432/genai"
)

def get_connection():
    return psycopg2.connect(DATABASE_URL)
