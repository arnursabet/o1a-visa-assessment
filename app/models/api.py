from typing import Dict, List
from pydantic import BaseModel, Field

from app.models.o1a import CriteriaMatches, QualificationRating


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error description")


class AssessmentResponse(BaseModel):
    """Response model for CV assessment endpoint."""
    criteria_matches: Dict[str, List[Dict[str, str]]] = Field(
        ..., 
        description="Matches for each O-1A criterion category"
    )
    qualification_rating: QualificationRating = Field(
        ..., 
        description="Overall qualification rating (low, medium, high)"
    )
    analysis: str = Field(
        ..., 
        description="Detailed analysis of the qualification assessment"
    ) 