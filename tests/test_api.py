import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.models.o1a import QualificationRating, CriteriaMatches, AssessmentResult


@pytest.fixture
def test_client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_pdf_content():
    """Mock PDF content fixture."""
    return io.BytesIO(b"%PDF-1.5\nMock PDF content for testing")


@pytest.fixture
def mock_assessment_result():
    """Mock assessment result fixture."""
    criteria_matches = CriteriaMatches()
    return AssessmentResult(
        criteria_matches=criteria_matches,
        qualification_rating=QualificationRating.MEDIUM,
        analysis="This is a mock analysis of the qualification assessment."
    )


def test_root_endpoint(test_client):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "O-1A Visa Qualification Assessment API" in response.json()["message"]


@patch("app.api.endpoints.assessment.process_cv_file")
@patch("app.api.endpoints.assessment.get_openai_service")
def test_assess_cv_endpoint(mock_get_openai_service, mock_process_cv_file, test_client, mock_pdf_content, mock_assessment_result):
    """Test the assess_cv endpoint."""
    # Mock dependencies
    mock_openai_service = MagicMock()
    mock_openai_service.assess_cv.return_value = mock_assessment_result
    mock_get_openai_service.return_value = mock_openai_service
    mock_process_cv_file.return_value = "Extracted text from CV"
    
    # Create test file
    files = {"file": ("test.pdf", mock_pdf_content, "application/pdf")}
    
    # Make request
    response = test_client.post("/api/v1/assess", files=files)
    
    # Assert response
    assert response.status_code == 200
    result = response.json()
    assert "criteria_matches" in result
    assert "qualification_rating" in result
    assert result["qualification_rating"] == QualificationRating.MEDIUM
    assert "analysis" in result
    
    # Verify mocks were called
    mock_process_cv_file.assert_called_once()
    mock_openai_service.assess_cv.assert_called_once_with("Extracted text from CV")


@patch("app.api.endpoints.assessment.process_cv_file")
def test_assess_cv_endpoint_error(mock_process_cv_file, test_client, mock_pdf_content):
    """Test the assess_cv endpoint with error."""
    # Mock error
    mock_process_cv_file.side_effect = Exception("Test error")
    
    # Create test file
    files = {"file": ("test.pdf", mock_pdf_content, "application/pdf")}
    
    # Make request
    response = test_client.post("/api/v1/assess", files=files)
    
    # Assert response
    assert response.status_code == 500
    result = response.json()
    assert "detail" in result
    assert "Error" in result["detail"] 