"""
مدل‌های SQLAlchemy برای پروژه خبری.
5 جدول: categories, fields, models, prompts, main
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Index,)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from py.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fields = relationship("Field", back_populates="category")
    mains = relationship("MainRecord", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="fields")
    mains = relationship("MainRecord", back_populates="field")

    def __repr__(self):
        return f"<Field {self.name}>"


class ModelInfo(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    provider = Column(String(100), nullable=False)
    version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mains = relationship("MainRecord", back_populates="model")

    def __repr__(self):
        return f"<ModelInfo {self.provider}/{self.name}>"


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    version = Column(String(20), nullable=False)
    system_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mains = relationship("MainRecord", back_populates="prompt")

    def __repr__(self):
        return f"<Prompt {self.version}>"


class MainRecord(Base):
    __tablename__ = "main"

    id = Column(Integer, primary_key=True)

    username = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    abstract = Column(Text, nullable=False)
    university = Column(String(200), nullable=False)
    table_of_contents = Column(Text, nullable=False)
    author = Column(String(200), nullable=False)
    supervisor = Column(String(200), nullable=False)

    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=True)

    status = Column(String(50), nullable=False, default="ready", index=True)
    output_json = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    field = relationship("Field", back_populates="mains")
    category = relationship("Category", back_populates="mains")
    model = relationship("ModelInfo", back_populates="mains")
    prompt = relationship("Prompt", back_populates="mains")

    def __repr__(self):
        return f"<MainRecord id={self.id} status={self.status}>"


Index("idx_main_status_created", MainRecord.status, MainRecord.created_at)
