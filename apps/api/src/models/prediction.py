from enum import Enum
from typing import Optional, List
from datetime import date, datetime

from sqlmodel import SQLModel, Field, Relationship


class PredictionStatus(str, Enum):
    DRAFT = "draft"
    RESEARCHING = "researching"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    RESOLVED = "resolved"


class PredictionBase(SQLModel):
    question: str = Field(index=True)
    description: Optional[str] = None
    resolution_date: Optional[date] = None


class Prediction(PredictionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: PredictionStatus = Field(default=PredictionStatus.DRAFT)
    outcome: Optional[bool] = None  # True/False when resolved
    updates: List["PredictionUpdate"] = Relationship(back_populates="prediction")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PredictionUpdate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prediction_id: int = Field(foreign_key="prediction.id", ondelete="CASCADE")
    prediction: Prediction = Relationship(back_populates="updates")
    likelihood: Optional[float] = Field(default=None, ge=0, le=1)
    reasoning: Optional[str] = None
    sources: List["Source"] = Relationship(back_populates="update")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    update_id: int = Field(foreign_key="predictionupdate.id", ondelete="CASCADE")
    update: PredictionUpdate = Relationship(back_populates="sources")
    title: str = Field(index=True)
    url: str = Field(index=True)
    summary: Optional[str] = None
    # how credible is the information (0 = not credible, 1 = very credible)
    credibility: Optional[float] = Field(default=None, ge=0, le=1)
    # how relevant is the information with respect to updating the likelihood of the prediction
    relevance: Optional[float] = Field(default=None, ge=0, le=1)
    reasoning: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
