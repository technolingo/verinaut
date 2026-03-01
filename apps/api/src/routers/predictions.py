from typing import List

from fastapi import status, APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..sqldb import get_session
from ..models import Prediction, PredictionPost

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/", response_model=List[Prediction])
async def list_predictions(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """List all predictions with pagination."""
    result = await session.execute(select(Prediction).offset(skip).limit(limit))
    predictions = result.scalars().all()
    return predictions


@router.get("/{prediction_id}", response_model=Prediction)
async def get_prediction(
    prediction_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a single prediction by ID."""
    prediction = await session.get(Prediction, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.post('/', response_model=Prediction, status_code=status.HTTP_201_CREATED)
async def post_prediction(
    payload: PredictionPost,
    session: AsyncSession = Depends(get_session)
):
    """Create a single prediction object."""
    prediction = Prediction.model_validate(payload)
    session.add(prediction)
    await session.commit()
    await session.refresh(prediction)
    return prediction
