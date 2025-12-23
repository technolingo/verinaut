# pylint: disable=not-callable

from enum import Enum
from typing import Optional, List
from datetime import date, datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import SQLModel, Field, Relationship


class PredictionStatus(str, Enum):
    DRAFT = "draft"
    RESEARCHING = "researching"
    PENDING_REVIEW = "pending_review"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str = Field(index=True)
    description: Optional[str] = None
    status: PredictionStatus = Field(default=PredictionStatus.DRAFT)
    outcome: Optional[bool] = None  # True/False when resolved
    known_date: date
    require_review: bool = Field(default=False)
    updates: List["PredictionUpdate"] = Relationship(back_populates="prediction")
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )


class PredictionUpdate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prediction_id: int = Field(foreign_key="prediction.id", ondelete="CASCADE")
    prediction: Prediction = Relationship(back_populates="updates")
    likelihood: float = Field(default=None, ge=0, le=1)
    reasoning: str
    sources: List["Source"] = Relationship(back_populates="update")
    review: Optional["HumanReview"] = Relationship(
        sa_relationship=RelationshipProperty(
            "HumanReview", back_populates="update", uselist=False
        )  # one-to-one relationship
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )


class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    update_id: int = Field(foreign_key="predictionupdate.id", ondelete="CASCADE")
    update: PredictionUpdate = Relationship(back_populates="sources")
    title: str = Field(index=True)
    url: str = Field(index=True)
    summary: str
    # how credible is the information (0 = not credible, 1 = very credible)
    credibility: float = Field(default=None, ge=0, le=1)
    # how relevant is the information with respect to updating the likelihood of the prediction
    relevance: float = Field(default=None, ge=0, le=1)
    reasoning: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )


class ReviewDecision(str, Enum):
    ACCEPT = "accept"
    CHALLENGE = "challenge"
    REJECT = "reject"


class HumanReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    update_id: int = Field(foreign_key="predictionupdate.id", ondelete="CASCADE")
    update: PredictionUpdate = Relationship(back_populates="review")
    name: str = Field(default="Zilong")
    decision: ReviewDecision = Field(default=ReviewDecision.CHALLENGE)
    feedback: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now())
    )
