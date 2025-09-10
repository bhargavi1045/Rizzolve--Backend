from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(20), default="student")
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    complaints = relationship("Complaint", back_populates="user")

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=True)
    priority = Column(String(20), default="normal")
    status = Column(String(20), default="pending")
    description = Column(Text, nullable=False)
    assigned_to = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="complaints")

class KBSource(Base):
    __tablename__ = "kb_sources"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chunks = relationship("KBChunk", back_populates="source", cascade="all, delete-orphan")

class KBChunk(Base):
    __tablename__ = "kb_chunks"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("kb_sources.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    source = relationship("KBSource", back_populates="chunks")
