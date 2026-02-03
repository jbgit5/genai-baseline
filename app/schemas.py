from pydantic import BaseModel

class IngestRequest(BaseModel):
    name: str
    email: str | None = None
    cv_text: str

class SearchRequest(BaseModel):
    query: str
