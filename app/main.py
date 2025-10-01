from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import init_db
from app.routers import auth, complaints, kb, rag

app = FastAPI(
    title="Hostel Complaint Assistant API",
    description="API for managing complaints, knowledge base, and retrieval-augmented generation",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}