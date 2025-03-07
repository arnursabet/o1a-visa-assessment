from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class QualificationRating(str, Enum):
    """Enum for O-1A qualification ratings."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class O1ACriteria(str, Enum):
    """Enum for O-1A visa criteria categories."""
    AWARDS = "awards"
    MEMBERSHIP = "membership"
    PRESS = "press"
    JUDGING = "judging"
    ORIGINAL_CONTRIBUTION = "original_contribution"
    SCHOLARLY_ARTICLES = "scholarly_articles"
    CRITICAL_EMPLOYMENT = "critical_employment"
    HIGH_REMUNERATION = "high_remuneration"


class CriteriaDescription(BaseModel):
    """Description of an O-1A criterion with examples."""
    name: O1ACriteria
    description: str
    examples: List[str]


class CriteriaMatch(BaseModel):
    """A match from the CV for a specific criterion."""
    text: str = Field(..., description="The exact text from the CV that matches the criterion")
    explanation: Optional[str] = Field(None, description="Explanation of why this text matches the criterion")


class CriteriaMatches(BaseModel):
    """Collection of matches for each O-1A criterion."""
    awards: List[CriteriaMatch] = Field(default_factory=list)
    membership: List[CriteriaMatch] = Field(default_factory=list)
    press: List[CriteriaMatch] = Field(default_factory=list)
    judging: List[CriteriaMatch] = Field(default_factory=list)
    original_contribution: List[CriteriaMatch] = Field(default_factory=list)
    scholarly_articles: List[CriteriaMatch] = Field(default_factory=list)
    critical_employment: List[CriteriaMatch] = Field(default_factory=list)
    high_remuneration: List[CriteriaMatch] = Field(default_factory=list)


class AssessmentResult(BaseModel):
    """Result of an O-1A visa qualification assessment."""
    criteria_matches: CriteriaMatches
    qualification_rating: QualificationRating
    analysis: str = Field(..., description="Explanation of the qualification rating")
    
    @property
    def met_criteria_count(self) -> int:
        """Count how many criteria have at least one match."""
        count = 0
        for criteria_list in self.criteria_matches.dict().values():
            if criteria_list:
                count += 1
        return count


O1A_CRITERIA_DESCRIPTIONS = [
    CriteriaDescription(
        name=O1ACriteria.AWARDS,
        description="Receipt of nationally or internationally recognized prizes or awards for excellence in the field",
        examples=[
            "Nobel Prize",
            "Academy Award",
            "Fields Medal",
            "Pulitzer Prize",
            "Industry-specific prestigious awards"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.MEMBERSHIP,
        description="Membership in associations that require outstanding achievements of their members",
        examples=[
            "National Academy of Sciences",
            "Royal Society",
            "Association requiring peer review or exceptional achievement for admission"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.PRESS,
        description="Published material in professional or major trade publications or major media about the person",
        examples=[
            "Feature articles in major newspapers",
            "Coverage in industry publications",
            "Interviews or profiles in respected media"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.JUDGING,
        description="Participation as a judge of the work of others in the same or a related field",
        examples=[
            "Peer reviewer for journals",
            "Grant proposal evaluator",
            "Competition judge",
            "Thesis committee member"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.ORIGINAL_CONTRIBUTION,
        description="Original scientific, scholarly, or business-related contributions of major significance",
        examples=[
            "Patents",
            "Groundbreaking research",
            "Innovative business methods",
            "Novel artistic techniques"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.SCHOLARLY_ARTICLES,
        description="Authorship of scholarly articles in the field, in professional journals, or other major media",
        examples=[
            "Peer-reviewed journal publications",
            "Technical white papers",
            "Book chapters",
            "Conference proceedings"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.CRITICAL_EMPLOYMENT,
        description="Employment in a critical or essential capacity at an organization with a distinguished reputation",
        examples=[
            "Leading role at renowned institution",
            "Key researcher at prestigious laboratory",
            "Essential team member at industry-leading company"
        ]
    ),
    CriteriaDescription(
        name=O1ACriteria.HIGH_REMUNERATION,
        description="Command of a high salary or other remuneration for services, as evidenced by contracts",
        examples=[
            "Salary significantly above industry average",
            "Substantial consulting fees",
            "Lucrative contracts",
            "High-value stock options or compensation packages"
        ]
    )
] 