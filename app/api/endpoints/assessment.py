import logging
from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.models.api import AssessmentResponse, ErrorResponse
from app.services.openai_service import OpenAIService
from app.utils.file_utils import process_cv_file

logger = logging.getLogger(__name__)

router = APIRouter()


def get_openai_service() -> OpenAIService:
    """Dependency to get the OpenAI service."""
    return OpenAIService()


@router.post(
    "/assess",
    response_model=AssessmentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "File processing error"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Assess CV for O-1A visa qualification",
    description="Upload a CV file (PDF) to assess qualification for an O-1A visa",
)
async def assess_cv(
    file: UploadFile = File(..., description="CV file in PDF format"),
    openai_service: OpenAIService = Depends(get_openai_service)
) -> Any:
    """
    Assess a CV for O-1A visa qualification.
    
    Args:
        file: The uploaded CV file
        openai_service: The OpenAI service dependency
        
    Returns:
        AssessmentResponse: The assessment results
        
    Raises:
        HTTPException: If there's an error processing the CV or performing the assessment
    """
    try:
        logger.info(f"Processing CV assessment for file: {file.filename}")
        
        cv_text = await process_cv_file(file)
        
        assessment_result = await openai_service.assess_cv(cv_text)
        
        response = {
            "criteria_matches": assessment_result.criteria_matches.model_dump(),
            "qualification_rating": assessment_result.qualification_rating,
            "analysis": assessment_result.analysis
        }
        
        logger.info(f"Completed CV assessment with rating: {assessment_result.qualification_rating}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assessing CV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assessing CV: {str(e)}"
        ) 