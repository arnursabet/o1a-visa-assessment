#!/usr/bin/env python3
"""
Sample client for the O-1A Visa Qualification Assessment API.

This script demonstrates how to use the API to upload a CV and get an assessment.
"""

import argparse
import json
import sys
from pathlib import Path
import requests


def assess_cv(file_path, api_url):
    """
    Upload a CV file to the API and get an assessment.
    
    Args:
        file_path: Path to the CV file
        api_url: URL of the API endpoint
        
    Returns:
        dict: Assessment results
    """
    # Validate file
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if not path.suffix.lower() == '.pdf':
        raise ValueError(f"File must be a PDF: {file_path}")
    
    with open(path, 'rb') as f:
        files = {'file': (path.name, f, 'application/pdf')}
        
        print(f"Uploading {path.name} to {api_url}...")
        response = requests.post(api_url, files=files)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
        return response.json()


def print_assessment(assessment):
    """
    Print the assessment results in a readable format.
    
    Args:
        assessment: Assessment results from the API
    """
    if not assessment:
        return
    
    print("\n" + "=" * 80)
    print(f"O-1A VISA QUALIFICATION ASSESSMENT")
    print("=" * 80)
    
    # Print qualification rating
    rating = assessment.get('qualification_rating', 'unknown')
    print(f"\nQUALIFICATION RATING: {rating.upper()}")
    
    # Print analysis
    analysis = assessment.get('analysis', 'No analysis provided')
    print(f"\nANALYSIS:")
    print("-" * 80)
    print(analysis)
    print("-" * 80)
    
    # Print criteria matches
    criteria_matches = assessment.get('criteria_matches', {})
    print("\nCRITERIA MATCHES:")
    print("-" * 80)
    
    for criterion, matches in criteria_matches.items():
        if matches:
            print(f"\n{criterion.upper()}:")
            for i, match in enumerate(matches, 1):
                text = match.get('text', '')
                explanation = match.get('explanation', '')
                print(f"  {i}. {text}")
                if explanation:
                    print(f"     Explanation: {explanation}")
        else:
            print(f"\n{criterion.upper()}: No matches found")
    
    print("\n" + "=" * 80)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='O-1A Visa Qualification Assessment API Client')
    parser.add_argument('file', help='Path to the CV file (PDF)')
    parser.add_argument('--api-url', default='http://localhost:8000/api/v1/assess', 
                         help='URL of the API endpoint')
    args = parser.parse_args()
    
    try:
        assessment = assess_cv(args.file, args.api_url)
        print_assessment(assessment)
        
        output_file = Path(args.file).stem + '_assessment.json'
        with open(output_file, 'w') as f:
            json.dump(assessment, f, indent=2)
        print(f"\nAssessment saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 