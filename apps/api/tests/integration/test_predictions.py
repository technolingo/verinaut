import pytest
from httpx import AsyncClient


class TestPredictionsAPI:
    """Integration tests for predictions API endpoints."""

    @pytest.mark.asyncio
    async def test_get_predictions_empty(self, client: AsyncClient):
        """Test GET /predictions with empty database."""
        response = await client.get("/predictions/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_get_predictions_with_data(
        self, client: AsyncClient, sample_predictions
    ):
        """Test GET /predictions with sample data."""
        response = await client.get("/predictions/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

        # Check that we have the expected predictions
        questions = {pred["question"] for pred in data}
        expected_questions = {
            "Will AI surpass human intelligence by 2030?",
            "Will renewable energy exceed 50% of US electricity by 2025?",
        }
        assert questions == expected_questions

        # Verify data structure
        for pred in data:
            assert "id" in pred
            assert "question" in pred
            assert "status" in pred
            assert "created_at" in pred
            assert "updated_at" in pred
            assert pred["status"] in [
                "draft",
                "researching",
                "pending_review",
                "approved",
                "resolved",
            ]

    @pytest.mark.asyncio
    async def test_get_predictions_pagination(
        self, client: AsyncClient, sample_predictions
    ):
        """Test GET /predictions with pagination."""
        # Test limit
        response = await client.get("/predictions/?limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        # Test skip
        response = await client.get("/predictions/?skip=1&limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        # Ensure different results
        response1 = await client.get("/predictions/?limit=1")
        response2 = await client.get("/predictions/?skip=1&limit=1")
        data1 = response1.json()
        data2 = response2.json()
        assert data1[0]["id"] != data2[0]["id"]

    @pytest.mark.asyncio
    async def test_get_predictions_with_json_fixtures(
        self, client: AsyncClient, load_test_data
    ):
        """Test GET /predictions with JSON fixture data."""
        response = await client.get("/predictions/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # Based on our fixtures

        # Check specific predictions from fixtures
        ai_predictions = [
            p for p in data if "AI surpass human intelligence" in p["question"]
        ]
        assert len(ai_predictions) == 1
        assert ai_predictions[0]["status"] == "approved"

        resolved_predictions = [p for p in data if p["outcome"] is not None]
        assert len(resolved_predictions) == 1
        assert resolved_predictions[0]["outcome"] is False

    @pytest.mark.asyncio
    async def test_get_single_prediction(self, client: AsyncClient, sample_predictions):
        """Test GET /predictions/{id} endpoint."""
        # Get the AI prediction ID
        ai_pred = sample_predictions["ai_prediction"]

        response = await client.get(f"/predictions/{ai_pred.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == ai_pred.id
        assert data["question"] == ai_pred.question
        assert data["status"] == ai_pred.status

    @pytest.mark.asyncio
    async def test_get_single_prediction_not_found(self, client: AsyncClient):
        """Test GET /predictions/{id} with non-existent ID."""
        response = await client.get("/predictions/999")
        assert response.status_code == 404
        assert "Prediction not found" in response.json()["detail"]
