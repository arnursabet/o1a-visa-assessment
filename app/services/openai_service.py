import json
import logging
from typing import Dict, Any

from openai import OpenAI

from app.core.config import settings
from app.models.o1a import (
    O1ACriteria, QualificationRating, CriteriaMatches, 
    AssessmentResult, O1A_CRITERIA_DESCRIPTIONS
)

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI service with the API key from settings."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def _create_extraction_prompt(self, cv_text: str) -> str:
        """
        Create a prompt for extracting achievements from a CV.
        
        Args:
            cv_text: The text content of the CV
            
        Returns:
            str: The formatted prompt for the extraction task
        """
        # Format the criteria descriptions for the prompt
        criteria_descriptions = ""
        for desc in O1A_CRITERIA_DESCRIPTIONS:
            criteria_descriptions += f"\n{desc.name.value.upper()}:\n"
            criteria_descriptions += f"- Description: {desc.description}\n"
            criteria_descriptions += f"- Examples: {', '.join(desc.examples)}\n"
        
        # Create the extraction prompt
        prompt = f"""
You are an experienced immigration attorney specializing in O-1A visa applications. 
Your task is to analyze a CV and extract any information that might satisfy the O-1A visa criteria.

The CV text is provided below, and I need you to identify potential matches for each of the 8 O-1A criteria.

For each criterion, extract relevant text from the CV that might satisfy it. For each match, provide:
1. The exact text from the CV
2. A brief explanation of why it matches the criterion

Here are the 8 O-1A criteria:
{criteria_descriptions}

Please format your response as a JSON object with this structure:
{{
  "criteria_matches": {{
    "awards": [
      {{ "text": "Award description from CV", "explanation": "Why this matches the awards criterion" }}
    ],
    "membership": [
      {{ "text": "Membership description from CV", "explanation": "Why this matches the membership criterion" }}
    ],
    // ... other criteria
  }}
}}

If no matches are found for a criterion, provide an empty array.

CV TEXT:
{cv_text}
"""
        return prompt
    
    def _create_evaluation_prompt(self, criteria_matches: CriteriaMatches) -> str:
        """
        Create a prompt for evaluating O-1A qualification based on extracted criteria matches.
        
        Args:
            criteria_matches: The matches for each O-1A criterion
            
        Returns:
            str: The formatted prompt for the evaluation task
        """
        # Convert criteria_matches to JSON string
        matches_json = json.dumps(criteria_matches.dict(), indent=2)
        
        prompt = f"""
You are an experienced immigration attorney specializing in O-1A visa applications.
Your task is to assess a candidate's qualification for an O-1A visa based on the extracted criteria matches from their CV.

Below are the matches found for each of the 8 O-1A criteria:

{matches_json}

Please evaluate the candidate's qualification for an O-1A visa as follows:

1. Analyze the strength of evidence for each criterion. According to USCIS, the applicant must satisfy at least 3 out of the 8 criteria.
2. Consider both the quantity and quality of evidence for each criterion.
3. Assign an overall qualification rating: "low", "medium", or "high".
   - LOW: Meets fewer than 3 criteria, or meets exactly 3 criteria but with weak evidence.
   - MEDIUM: Meets 3-4 criteria with moderate evidence, or 5+ criteria with weak evidence.
   - HIGH: Meets 5+ criteria with strong evidence, or has exceptionally strong evidence in 3-4 criteria.
4. Provide an analysis explaining your rating.

Format your response as a JSON object with this structure:
{{
  "qualification_rating": "low|medium|high",
  "analysis": "Detailed explanation of the qualification assessment"
}}
"""
        return prompt
    
    async def extract_criteria_matches(self, cv_text: str) -> CriteriaMatches:
        """
        Extract matches for O-1A criteria from CV text.
        
        Args:
            cv_text: The text content of the CV
            
        Returns:
            CriteriaMatches: The extracted matches for each criterion
            
        Raises:
            Exception: If there's an error extracting matches
        """
        try:
            prompt = self._create_extraction_prompt(cv_text)
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_EXTRACTION_MODEL,
                messages=[
                    {"role": "system", "content": "You are a specialist in analyzing CVs for O-1A visa qualification."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            results = json.loads(content)
            
            criteria_matches = CriteriaMatches(**results.get("criteria_matches", {}))
            
            logger.info(f"Extracted {sum(len(getattr(criteria_matches, c.value)) for c in O1ACriteria)} matches across all criteria")
            return criteria_matches
            
        except Exception as e:
            logger.error(f"Error extracting criteria matches: {e}")
            raise
    
    async def evaluate_qualification(self, criteria_matches: CriteriaMatches) -> Dict[str, Any]:
        """
        Evaluate O-1A qualification based on extracted criteria matches.
        
        Args:
            criteria_matches: The matches for each O-1A criterion
            
        Returns:
            Dict: The qualification rating and analysis
            
        Raises:
            Exception: If there's an error evaluating qualification
        """
        try:
            prompt = self._create_evaluation_prompt(criteria_matches)
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_EVALUATION_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert immigration attorney specializing in O-1A visas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            results = json.loads(content)
            
            logger.info(f"Qualification evaluation completed with rating: {results.get('qualification_rating')}")
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating qualification: {e}")
            raise
    
    async def assess_cv(self, cv_text: str) -> AssessmentResult:
        """
        Assess a CV for O-1A visa qualification.
        
        Args:
            cv_text: The text content of the CV
            
        Returns:
            AssessmentResult: The assessment result with criteria matches and qualification rating
            
        Raises:
            Exception: If there's an error assessing the CV
        """
        criteria_matches = await self.extract_criteria_matches(cv_text)
        
        evaluation = await self.evaluate_qualification(criteria_matches)
        
        assessment_result = AssessmentResult(
            criteria_matches=criteria_matches,
            qualification_rating=evaluation.get("qualification_rating", QualificationRating.LOW),
            analysis=evaluation.get("analysis", "No analysis provided")
        )
        
        return assessment_result 